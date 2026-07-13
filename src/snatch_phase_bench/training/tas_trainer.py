"""TAS trainer stub — architecture-specific trainers register here later."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import torch

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.models.base import TemporalSegmentationModel
from snatch_phase_bench.training.interfaces import (
    TemporalSegmentationTrainer,
    TrainerConfig,
    TrainingRunContext,
)


class TASTrainerNotImplemented(TemporalSegmentationTrainer):
    """
    Placeholder trainer documenting the integration contract.

    MS-TCN and related architectures will provide concrete implementations.
    """

    def fit(
        self,
        train_records: list[FrameSequenceRecord],
        val_records: list[FrameSequenceRecord],
        *,
        model: TemporalSegmentationModel,
        config: TrainerConfig,
        context: TrainingRunContext,
    ) -> TemporalSegmentationModel:
        raise NotImplementedError(
            "TAS training is not enabled yet. Implement a concrete trainer for the "
            f"registered model '{context.registry_name}' before calling fit()."
        )

    def predict_records(
        self,
        records: list[FrameSequenceRecord],
        *,
        model: TemporalSegmentationModel,
        device: torch.device,
    ) -> dict[str, np.ndarray]:
        raise NotImplementedError(
            "TAS inference is not enabled yet. Implement predict_records() for the "
            f"model '{model.name}' before generating benchmark predictions."
        )

    def save_checkpoint(
        self,
        model: TemporalSegmentationModel,
        path: Path,
        *,
        context: TrainingRunContext,
        metrics: dict[str, Any] | None = None,
    ) -> None:
        raise NotImplementedError("TAS checkpoint saving is not enabled yet.")

    def load_checkpoint(
        self,
        path: Path,
        *,
        model: TemporalSegmentationModel,
    ) -> TemporalSegmentationModel:
        raise NotImplementedError("TAS checkpoint loading is not enabled yet.")
