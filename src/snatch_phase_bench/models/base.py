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
    """Shape ``(batch, num_classes)`` for window classifiers."""

    extras: dict[str, Any] | None = None


class TemporalSegmentationModel(ABC, nn.Module):
    """
    Pluggable interface for temporal segmentation models.

    Window-based models (LSTM, GRU) consume ``(batch, time, features)``.
    Future frame-wise or graph models may override ``input_layout`` and ``forward``.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Short registry identifier."""

    @property
    def input_layout(self) -> str:
        """One of ``window_sequence``, ``frame_sequence``, ``graph_sequence``."""
        return "window_sequence"

    @abstractmethod
    def forward(self, x: torch.Tensor) -> ModelOutput:
        """Run forward pass and return logits."""

    @abstractmethod
    def num_parameters(self) -> int:
        """Return trainable parameter count."""

    def predict_classes(self, x: torch.Tensor) -> torch.Tensor:
        """Argmax over class dimension."""
        return torch.argmax(self.forward(x).logits, dim=-1)
