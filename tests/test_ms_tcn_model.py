"""Unit tests for MS-TCN architecture."""

from __future__ import annotations

import torch

from snatch_phase_bench.models.ms_tcn import MSTCNModel
from snatch_phase_bench.models.registry import build_model


def test_ms_tcn_instantiates_from_registry() -> None:
    model = build_model("ms_tcn", input_size=99, num_classes=8)
    assert isinstance(model, MSTCNModel)
    assert model.input_layout == "frame_sequence"
    assert model.output_layout == "frame_sequence"


def test_ms_tcn_forward_shape() -> None:
    model = MSTCNModel(input_size=99, num_classes=8, num_stages=2, num_layers=4, num_f_maps=32)
    x = torch.randn(2, 40, 99)
    output = model(x)
    assert output.logits.shape == (2, 40, 8)
    assert output.extras is not None
    assert output.extras["stage_logits"].shape[0] == 2


def test_ms_tcn_stage_logits_match_num_stages() -> None:
    model = MSTCNModel(input_size=16, num_classes=5, num_stages=4, num_layers=3, num_f_maps=16)
    x = torch.randn(1, 25, 16)
    stages = model.forward_stages(x)
    assert stages.shape == (4, 1, 5, 25)


def test_ms_tcn_predict_classes() -> None:
    model = MSTCNModel(input_size=8, num_classes=4, num_stages=2, num_layers=2, num_f_maps=8)
    x = torch.randn(1, 10, 8)
    pred = model.predict_classes(x)
    assert pred.shape == (1, 10)
    assert pred.dtype == torch.int64
