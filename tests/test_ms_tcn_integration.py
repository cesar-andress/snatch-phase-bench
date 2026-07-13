"""End-to-end MS-TCN pipeline integration tests."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from snatch_phase_bench.benchmark.registry import load_model_experiment_config
from snatch_phase_bench.data.frame_sequence import load_frame_sequences
from snatch_phase_bench.evaluation.tas_hooks import evaluate_frame_predictions
from snatch_phase_bench.experiments.config_loader import get_section
from snatch_phase_bench.models.ms_tcn.inference import load_ms_tcn_from_checkpoint, predict_videos
from snatch_phase_bench.models.registry import build_model
from snatch_phase_bench.training.interfaces import TrainerConfig, TrainingRunContext
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_full_train_predict_eval_pipeline(
    synthetic_ms_tcn_dataset: tuple[Path, Path, object],
    tmp_path: Path,
) -> None:
    labels_csv, keypoints_dir, split = synthetic_ms_tcn_dataset
    config = load_model_experiment_config(PROJECT_ROOT / "configs/benchmark/ms_tcn.yaml")
    model_cfg = get_section(config, "model")
    ontology_cfg = get_section(config, "ontology")
    loss_cfg = get_section(config, "loss")

    train = load_frame_sequences(
        labels_csv=labels_csv, keypoints_dir=keypoints_dir, athlete_split=split, split_filter="train"
    )
    val = load_frame_sequences(
        labels_csv=labels_csv, keypoints_dir=keypoints_dir, athlete_split=split, split_filter="val"
    )

    num_classes = int(ontology_cfg["ignore_label_id"]) + int(ontology_cfg["num_supervised_classes"])
    model = build_model(
        "ms_tcn",
        input_size=99,
        num_classes=num_classes,
        num_stages=2,
        num_layers=3,
        num_f_maps=16,
        kernel_size=int(model_cfg["kernel_size"]),
        dropout=0.0,
    )
    trainer = MSTCNTrainer(
        num_classes=num_classes,
        tmse_weight=float(loss_cfg["tmse_weight"]),
        tmse_truncate_tau=float(loss_cfg["tmse_truncate_tau"]),
    )
    output_dir = tmp_path / "pipeline"
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name="ms_tcn",
        config_path=PROJECT_ROOT / "configs/benchmark/ms_tcn.yaml",
        seed=42,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=output_dir,
    )
    trainer.fit(
        train,
        val,
        model=model,
        config=TrainerConfig(epochs=2, early_stopping_patience=5, learning_rate=1e-3),
        context=context,
    )

    loaded, _ = load_ms_tcn_from_checkpoint(
        output_dir / "best_model.pt",
        input_size=99,
        num_classes=num_classes,
        num_stages=2,
        num_layers=3,
        num_f_maps=16,
        kernel_size=3,
        dropout=0.0,
    )
    mean, std = MSTCNTrainer.load_standardization(output_dir)
    preds = predict_videos(val, model=loaded, mean=mean, std=std, device="cpu")
    result = evaluate_frame_predictions(val, preds, model_identifier="ms_tcn_pipeline_test")

    assert len(result.per_video) == len(val)
    assert "segment_macro_over_videos" in result.aggregate
    assert result.ontology_id == "seven_phase_v1"


def test_config_model_params_instantiate(
    synthetic_ms_tcn_dataset: tuple[Path, Path, object],
) -> None:
    config = load_model_experiment_config(PROJECT_ROOT / "configs/benchmark/ms_tcn.yaml")
    model_cfg = get_section(config, "model")
    ontology_cfg = get_section(config, "ontology")
    num_classes = int(ontology_cfg["ignore_label_id"]) + int(ontology_cfg["num_supervised_classes"])
    model = build_model(
        "ms_tcn",
        input_size=99,
        num_classes=num_classes,
        num_stages=int(model_cfg["num_stages"]),
        num_layers=int(model_cfg["num_layers"]),
        num_f_maps=int(model_cfg["num_f_maps"]),
        kernel_size=int(model_cfg["kernel_size"]),
        dropout=float(model_cfg["dropout"]),
    )
    import torch

    out = model(torch.randn(1, 50, 99))
    assert out.logits.shape == (1, 50, num_classes)


def test_history_json_is_valid(
    trained_ms_tcn_checkpoint: Path,
) -> None:
    history = json.loads((trained_ms_tcn_checkpoint / "history.json").read_text(encoding="utf-8"))
    assert isinstance(history, list)
    assert "train" in history[0]
    assert "val" in history[0]
    assert "loss_total" in history[0]["train"]


def test_standardization_numpy_arrays_finite(
    trained_ms_tcn_checkpoint: Path,
) -> None:
    mean, std = MSTCNTrainer.load_standardization(trained_ms_tcn_checkpoint)
    assert np.isfinite(mean).all()
    assert np.isfinite(std).all()
    assert (std > 0).all()


def test_prediction_length_matches_labels(
    synthetic_train_val_records: tuple[list, list],
    trained_ms_tcn_checkpoint: Path,
) -> None:
    train, _ = synthetic_train_val_records
    mean, std = MSTCNTrainer.load_standardization(trained_ms_tcn_checkpoint)
    model, _ = load_ms_tcn_from_checkpoint(
        trained_ms_tcn_checkpoint / "best_model.pt",
        input_size=99,
        num_classes=8,
        num_stages=2,
        num_layers=4,
        num_f_maps=32,
        dropout=0.0,
    )
    preds = predict_videos(train, model=model, mean=mean, std=std, device="cpu")
    for record in train:
        assert len(preds[record.video_relpath]) == len(record.phase_ids)
