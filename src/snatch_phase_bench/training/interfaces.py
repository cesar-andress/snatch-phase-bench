"""Training interfaces for learned temporal segmenters (TAS)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

import numpy as np
import torch

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.models.base import TemporalSegmentationModel


@dataclass(frozen=True)
class TrainingRunContext:
    """Immutable metadata attached to a training or evaluation run."""

    model_id: str
    registry_name: str
    config_path: Path
    seed: int
    split_version: str
    dataset_version: str
    output_dir: Path
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TrainerConfig:
    """Common training hyperparameters for frame-wise TAS models."""

    batch_size: int = 1
    epochs: int = 120
    learning_rate: float = 5e-4
    weight_decay: float = 1e-5
    device: str = "auto"
    early_stopping_monitor: str = "val_macro_f1"
    early_stopping_patience: int = 15
    class_weighting: bool = True
    standardize: str = "train_only"
    ignore_label_id: int = 0


class FramePredictor(Protocol):
    """Minimal inference contract for evaluation hooks."""

    def predict_frame_labels(self, features: np.ndarray) -> np.ndarray:
        """Return per-frame phase ids for ``features`` with shape ``(T, D)``."""


class TemporalSegmentationTrainer(ABC):
    """
    Training pipeline interface for frame-wise temporal segmenters.

    Concrete implementations (e.g. MS-TCN) plug in here without modifying the
    frozen LSTM trainer.
    """

    @abstractmethod
    def fit(
        self,
        train_records: list[FrameSequenceRecord],
        val_records: list[FrameSequenceRecord],
        *,
        model: TemporalSegmentationModel,
        config: TrainerConfig,
        context: TrainingRunContext,
    ) -> TemporalSegmentationModel:
        """Train ``model`` and return the best checkpoint."""

    @abstractmethod
    def predict_records(
        self,
        records: list[FrameSequenceRecord],
        *,
        model: TemporalSegmentationModel,
        device: torch.device,
    ) -> dict[str, np.ndarray]:
        """Return ``video_relpath -> predicted phase ids``."""

    @abstractmethod
    def save_checkpoint(
        self,
        model: TemporalSegmentationModel,
        path: Path,
        *,
        context: TrainingRunContext,
        metrics: dict[str, Any] | None = None,
    ) -> None:
        """Persist model weights and run metadata."""

    @abstractmethod
    def load_checkpoint(
        self,
        path: Path,
        *,
        model: TemporalSegmentationModel,
    ) -> TemporalSegmentationModel:
        """Restore model weights from ``path``."""
