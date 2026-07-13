"""Tests for model registry and LSTM adapter."""

from __future__ import annotations

import torch

from snatch_phase_bench.models.base import TemporalSegmentationModel
from snatch_phase_bench.models.lstm_baseline import LSTMBaselineModel
from snatch_phase_bench.models.registry import build_model, list_models


def test_lstm_baseline_implements_interface() -> None:
    model = LSTMBaselineModel(input_size=99, num_classes=7)
    assert isinstance(model, TemporalSegmentationModel)
    x = torch.randn(4, 31, 99)
    out = model(x)
    assert out.logits.shape == (4, 7)


def test_registry_build_lstm() -> None:
    model = build_model("lstm_baseline", input_size=99, num_classes=7)
    assert model.name == "lstm_baseline"
    assert "lstm_baseline" in list_models()


def test_registry_build_ms_tcn() -> None:
    model = build_model("ms_tcn", input_size=99, num_classes=8, num_stages=2, num_layers=3, num_f_maps=16)
    assert model.name == "ms_tcn"
    assert "ms_tcn" in list_models()
