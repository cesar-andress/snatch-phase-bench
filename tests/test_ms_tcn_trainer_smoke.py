"""Smoke tests for MS-TCN training on synthetic frame sequences."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from snatch_phase_bench.data.frame_sequence import build_frame_sequence, load_frame_sequences
from snatch_phase_bench.data.splits import AthleteSplit
from snatch_phase_bench.models.ms_tcn.model import MSTCNModel
from snatch_phase_bench.training.interfaces import TrainerConfig, TrainingRunContext
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer


def test_build_frame_sequence_smoke(
    synthetic_ms_tcn_dataset: tuple[Path, Path, AthleteSplit],
) -> None:
    labels_csv, keypoints_dir, _split = synthetic_ms_tcn_dataset
    record = build_frame_sequence("athlete_a/clip0.mp4", labels_csv=labels_csv, keypoints_dir=keypoints_dir)
    assert record.num_frames == 10
    assert record.feature_dim == 99


def test_ms_tcn_training_loss_decreases(
    synthetic_ms_tcn_dataset: tuple[Path, Path, AthleteSplit],
) -> None:
    labels_csv, keypoints_dir, split = synthetic_ms_tcn_dataset
    train_records = load_frame_sequences(
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
        athlete_split=split,
        split_filter="train",
    )
    val_records = load_frame_sequences(
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
        athlete_split=split,
        split_filter="val",
    )

    model = MSTCNModel(
        input_size=99,
        num_classes=8,
        num_stages=2,
        num_layers=4,
        num_f_maps=32,
        dropout=0.0,
    )
    trainer = MSTCNTrainer(num_classes=8)
    output_dir = labels_csv.parent / "outputs"
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name="ms_tcn",
        config_path=labels_csv,
        seed=42,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=output_dir,
    )
    config = TrainerConfig(batch_size=1, epochs=3, early_stopping_patience=10, learning_rate=1e-3)
    trained = trainer.fit(train_records, val_records, model=model, config=config, context=context)

    parsed = json.loads((output_dir / "history.json").read_text(encoding="utf-8"))
    assert len(parsed) >= 2
    assert parsed[-1]["train"]["loss_total"] <= parsed[0]["train"]["loss_total"]
    assert (output_dir / "best_model.pt").exists()

    payload = torch.load(output_dir / "best_model.pt", map_location="cpu", weights_only=False)
    assert "model_state_dict" in payload
    assert isinstance(trained, MSTCNModel)


def test_ms_tcn_checkpoint_load_and_predict(
    synthetic_ms_tcn_dataset: tuple[Path, Path, AthleteSplit],
) -> None:
    labels_csv, keypoints_dir, split = synthetic_ms_tcn_dataset
    train_records = load_frame_sequences(
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
        athlete_split=split,
        split_filter="train",
    )
    model = MSTCNModel(input_size=99, num_classes=8, num_stages=2, num_layers=3, num_f_maps=16, dropout=0.0)
    trainer = MSTCNTrainer(num_classes=8)
    output_dir = labels_csv.parent / "predict_outputs"
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name="ms_tcn",
        config_path=labels_csv,
        seed=7,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=output_dir,
    )
    config = TrainerConfig(batch_size=1, epochs=1, early_stopping_patience=1)
    trainer.fit(train_records, train_records[:1], model=model, config=config, context=context)

    mean, std = MSTCNTrainer.load_standardization(output_dir)
    loaded = MSTCNModel(input_size=99, num_classes=8, num_stages=2, num_layers=3, num_f_maps=16, dropout=0.0)
    trainer.load_checkpoint(output_dir / "best_model.pt", model=loaded)
    preds = trainer.predict_records(train_records[:1], model=loaded, device=torch.device("cpu"), mean=mean, std=std)
    assert train_records[0].video_relpath in preds
    assert len(preds[train_records[0].video_relpath]) == train_records[0].num_frames
