"""Model interfaces for temporal phase segmentation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import torch
import torch.nn as nn


@dataclass(frozen=True)
class ModelOutput:
    """Standard forward pass output."""

    logits: torch.Tensor
    """
    Class logits.

    - ``window_sequence`` models: ``(batch, num_classes)``
    - ``frame_sequence`` models: ``(batch, time, num_classes)``
    """

    extras: dict[str, Any] | None = None


class TemporalSegmentationModel(ABC, nn.Module):
    """
    Pluggable interface for temporal segmentation models.

    Window-based models (LSTM, GRU) consume ``(batch, time, features)`` and emit
    one label per window. Frame-wise TAS models consume the same input layout but
    emit one label per input frame via ``output_layout='frame_sequence'``.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Short registry identifier."""

    @property
    def input_layout(self) -> str:
        """One of ``window_sequence``, ``frame_sequence``, ``graph_sequence``."""
        return "window_sequence"

    @property
    def output_layout(self) -> str:
        """One of ``window_label``, ``frame_sequence``."""
        if self.input_layout == "frame_sequence":
            return "frame_sequence"
        return "window_label"

    @abstractmethod
    def forward(self, x: torch.Tensor) -> ModelOutput:
        """Run forward pass and return logits."""

    @abstractmethod
    def num_parameters(self) -> int:
        """Return trainable parameter count."""

    def predict_classes(self, x: torch.Tensor) -> torch.Tensor:
        """Argmax over class dimension."""
        logits = self.forward(x).logits
        if self.output_layout == "frame_sequence":
            return torch.argmax(logits, dim=-1)
        return torch.argmax(logits, dim=-1)
