"""MS-TCN inference helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord, load_frame_sequences
from snatch_phase_bench.evaluation.tas_hooks import evaluate_frame_predictions
from snatch_phase_bench.evaluation.results import BenchmarkEvaluationResult
from snatch_phase_bench.models.ms_tcn.model import MSTCNModel
from snatch_phase_bench.models.registry import build_model
from snatch_phase_bench.training.lstm_trainer import resolve_device
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer


def load_ms_tcn_from_checkpoint(
    checkpoint_path: Path,
    *,
    input_size: int = 99,
    num_classes: int = 8,
    num_stages: int = 4,
    num_layers: int = 10,
    num_f_maps: int = 64,
    kernel_size: int = 3,
    dropout: float = 0.5,
) -> tuple[MSTCNModel, dict]:
    """Load ``MSTCNModel`` weights and checkpoint metadata."""
    model = build_model(
        "ms_tcn",
        input_size=input_size,
        num_classes=num_classes,
        num_stages=num_stages,
        num_layers=num_layers,
        num_f_maps=num_f_maps,
        kernel_size=kernel_size,
        dropout=dropout,
    )
    payload = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    if not isinstance(model, MSTCNModel):
        raise TypeError("Expected MSTCNModel from registry.")
    model.load_state_dict(payload["model_state_dict"])
    return model, payload


def predict_videos(
    records: list[FrameSequenceRecord],
    *,
    model: MSTCNModel,
    mean: np.ndarray,
    std: np.ndarray,
    device: str = "auto",
) -> dict[str, np.ndarray]:
    """Run deterministic inference for multiple videos."""
    trainer = MSTCNTrainer()
    return trainer.predict_records(
        records,
        model=model,
        device=resolve_device(device),
        mean=mean,
        std=std,
    )


def evaluate_checkpoint_on_records(
    records: list[FrameSequenceRecord],
    predictions: dict[str, np.ndarray],
    *,
    model_identifier: str,
) -> BenchmarkEvaluationResult:
    """Evaluate predictions with the canonical benchmark evaluator."""
    return evaluate_frame_predictions(records, predictions, model_identifier=model_identifier)


def build_records_from_paths(
    *,
    labels_csv: Path,
    keypoints_dir: Path,
    video_relpaths: list[str] | None = None,
    use_z: bool = True,
) -> list[FrameSequenceRecord]:
    """Load frame records for inference/evaluation."""
    all_records = load_frame_sequences(labels_csv=labels_csv, keypoints_dir=keypoints_dir, use_z=use_z)
    if video_relpaths is None:
        return all_records
    wanted = set(video_relpaths)
    return [record for record in all_records if record.video_relpath in wanted]
