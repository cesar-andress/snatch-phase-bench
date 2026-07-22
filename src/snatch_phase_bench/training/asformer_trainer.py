"""Deterministic ASFormer trainer (reuses MS-TCN training loop + multi-stage loss)."""

from __future__ import annotations

import numpy as np
import torch

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.evaluation.tas_hooks import evaluate_frame_predictions
from snatch_phase_bench.models.asformer.model import ASFormerModel
from snatch_phase_bench.models.base import TemporalSegmentationModel
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer, _macro_f1_supervised

CHECKPOINT_VERSION = "asformer-v1"


class ASFormerTrainer(MSTCNTrainer):
    """ASFormer training with the frozen B2 evaluation / early-stopping protocol."""

    checkpoint_version: str = CHECKPOINT_VERSION
    required_model_type: type = ASFormerModel

    def predict_records(
        self,
        records: list[FrameSequenceRecord],
        *,
        model: TemporalSegmentationModel,
        device: torch.device,
        mean: np.ndarray | None = None,
        std: np.ndarray | None = None,
    ) -> dict[str, np.ndarray]:
        if not isinstance(model, ASFormerModel):
            raise TypeError("ASFormerTrainer requires ASFormerModel.")
        model = model.to(device)
        model.eval()

        if mean is None or std is None:
            mean = np.zeros(records[0].feature_dim, dtype=np.float32)
            std = np.ones(records[0].feature_dim, dtype=np.float32)

        predictions: dict[str, np.ndarray] = {}
        with torch.no_grad():
            for record in records:
                features = ((record.features - mean) / std).astype(np.float32)
                tensor = torch.from_numpy(features).unsqueeze(0).to(device)
                pred = model.predict_classes(tensor).squeeze(0).cpu().numpy().astype(np.int64)
                predictions[record.video_relpath] = pred
        return predictions

    def predict_video(
        self,
        features: np.ndarray,
        *,
        model: ASFormerModel,
        device: torch.device,
        mean: np.ndarray,
        std: np.ndarray,
    ) -> np.ndarray:
        model = model.to(device)
        standardized = ((features - mean) / std).astype(np.float32)
        tensor = torch.from_numpy(standardized).unsqueeze(0).to(device)
        model.eval()
        with torch.no_grad():
            return model.predict_classes(tensor).squeeze(0).cpu().numpy().astype(np.int64)

    def _compute_segment_validation_metrics(
        self,
        model: TemporalSegmentationModel,
        val_records: list[FrameSequenceRecord],
        *,
        device: torch.device,
        mean: np.ndarray,
        std: np.ndarray,
        ignore_label_id: int,
    ) -> dict[str, float]:
        predictions = self.predict_records(
            val_records,
            model=model,
            device=device,
            mean=mean,
            std=std,
        )
        result = evaluate_frame_predictions(
            val_records,
            predictions,
            model_identifier="asformer_val_selection",
        )
        segment_agg = result.aggregate.get("segment_macro_over_videos", {})
        boundary_micro = result.aggregate.get("boundary_mae_frames_micro_over_videos")
        metrics = {
            "segmental_f1_at_50": float(segment_agg.get("segmental_f1_at_50", 0.0)),
            "segmental_f1_at_25": float(segment_agg.get("segmental_f1_at_25", 0.0)),
            "segmental_f1_at_10": float(segment_agg.get("segmental_f1_at_10", 0.0)),
            "edit_score": float(segment_agg.get("edit_score", 0.0)),
        }
        if boundary_micro is not None:
            metrics["boundary_mae_frames"] = float(boundary_micro)
        y_true_all: list[int] = []
        y_pred_all: list[int] = []
        for record in val_records:
            pred = predictions[record.video_relpath]
            mask = record.phase_ids != ignore_label_id
            y_true_all.extend(record.phase_ids[mask].tolist())
            y_pred_all.extend(pred[mask].tolist())
        if y_true_all:
            metrics["macro_f1_frame"] = _macro_f1_supervised(
                np.asarray(y_true_all, dtype=np.int64),
                np.asarray(y_pred_all, dtype=np.int64),
                ignore_label_id,
            )
        return metrics
