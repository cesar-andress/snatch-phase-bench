"""Tests for MS-TCN inference helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.evaluation.results import validate_result_schema
from snatch_phase_bench.evaluation.tas_hooks import evaluate_and_write
from snatch_phase_bench.models.ms_tcn.inference import (
    build_records_from_paths,
    evaluate_checkpoint_on_records,
    load_ms_tcn_from_checkpoint,
    predict_videos,
)
from snatch_phase_bench.models.ms_tcn.model import MSTCNModel
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer


def test_load_ms_tcn_from_checkpoint(
    trained_ms_tcn_checkpoint: Path,
) -> None:
    model, payload = load_ms_tcn_from_checkpoint(
        trained_ms_tcn_checkpoint / "best_model.pt",
        input_size=99,
        num_classes=8,
        num_stages=2,
        num_layers=4,
        num_f_maps=32,
        dropout=0.0,
    )
    assert isinstance(model, MSTCNModel)
    assert "model_state_dict" in payload


def test_predict_videos_returns_all_keys(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
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
    assert set(preds) == {record.video_relpath for record in train}
    for record in train:
        assert len(preds[record.video_relpath]) == record.num_frames


def test_evaluate_checkpoint_on_records(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
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
    preds = predict_videos(train[:1], model=model, mean=mean, std=std, device="cpu")
    result = evaluate_checkpoint_on_records(
        train[:1],
        preds,
        model_identifier="ms_tcn_test",
    )
    assert result.model_identifier == "ms_tcn_test"
    assert len(result.per_video) == 1


def test_build_records_from_paths_filters_videos(
    synthetic_ms_tcn_dataset: tuple[Path, Path, object],
) -> None:
    labels_csv, keypoints_dir, _ = synthetic_ms_tcn_dataset
    all_records = build_records_from_paths(labels_csv=labels_csv, keypoints_dir=keypoints_dir)
    filtered = build_records_from_paths(
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
        video_relpaths=["athlete_a/clip0.mp4"],
    )
    assert len(filtered) == 1
    assert len(all_records) == 4


def test_evaluate_and_write_validates_schema(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
    trained_ms_tcn_checkpoint: Path,
    tmp_path: Path,
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
    preds = predict_videos(train[:1], model=model, mean=mean, std=std, device="cpu")
    out_path = tmp_path / "eval.json"
    result = evaluate_and_write(train[:1], preds, out_path, model_identifier="ms_tcn_schema_test")
    assert out_path.exists()
    validate_result_schema(result.to_dict())


def test_predictions_perfect_match_high_metrics(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
) -> None:
    train, _ = synthetic_train_val_records
    record = train[0]
    preds = {record.video_relpath: record.phase_ids.copy()}
    result = evaluate_checkpoint_on_records([record], preds, model_identifier="perfect")
    seg = result.per_video[record.video_relpath].segment["aggregate"]
    assert seg["segmental_f1_at_50"] == pytest.approx(1.0)
    assert seg["edit_score"] == pytest.approx(1.0)
