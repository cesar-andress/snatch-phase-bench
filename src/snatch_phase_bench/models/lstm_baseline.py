"""LSTM baseline adapter — wraps frozen ``LSTMClassifier`` without modifying it."""

from __future__ import annotations

import torch

from snatch_phase_bench.models.base import ModelOutput, TemporalSegmentationModel
from snatch_phase_bench.models.lstm_classifier import LSTMClassifier


class LSTMBaselineModel(TemporalSegmentationModel):
    """Adapter exposing the thesis LSTM through ``TemporalSegmentationModel``."""

    name = "lstm_baseline"

    def __init__(
        self,
        input_size: int,
        hidden_size: int = 128,
        num_layers: int = 1,
        num_classes: int = 7,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self._core = LSTMClassifier(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            num_classes=num_classes,
            dropout=dropout,
        )

    @property
    def core(self) -> LSTMClassifier:
        """Access underlying frozen-architecture module (e.g. for checkpoint load)."""
        return self._core

    def forward(self, x: torch.Tensor) -> ModelOutput:
        return ModelOutput(logits=self._core(x))

    def num_parameters(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters() if parameter.requires_grad)
