"""Extended unit tests for MSTCNModel adapter."""

from __future__ import annotations

import pytest
import torch

from snatch_phase_bench.models.base import TemporalSegmentationModel
from snatch_phase_bench.models.ms_tcn import MSTCNModel
from snatch_phase_bench.models.registry import build_model, get_model_factory


def test_ms_tcn_is_temporal_segmentation_model() -> None:
    model = MSTCNModel(input_size=99, num_classes=8)
    assert isinstance(model, TemporalSegmentationModel)


def test_ms_tcn_wrong_feature_dim_raises() -> None:
    model = MSTCNModel(input_size=99, num_classes=8, num_stages=1, num_layers=2, num_f_maps=8)
    with pytest.raises(ValueError, match="feature dim"):
        model(torch.randn(1, 10, 50))


def test_ms_tcn_wrong_input_rank_raises() -> None:
    model = MSTCNModel(input_size=99, num_classes=8)
    with pytest.raises(ValueError, match="batch, time, features"):
        model(torch.randn(99, 10))


def test_ms_tcn_num_parameters_positive() -> None:
    model = MSTCNModel(input_size=99, num_classes=8, num_stages=2, num_layers=3, num_f_maps=16)
    assert model.num_parameters() > 0


def test_ms_tcn_more_stages_increases_parameters() -> None:
    small = MSTCNModel(input_size=32, num_classes=4, num_stages=1, num_layers=2, num_f_maps=16)
    large = MSTCNModel(input_size=32, num_classes=4, num_stages=4, num_layers=2, num_f_maps=16)
    assert large.num_parameters() > small.num_parameters()


def test_ms_tcn_custom_mask_shape_2d() -> None:
    model = MSTCNModel(input_size=8, num_classes=4, num_stages=1, num_layers=2, num_f_maps=8, dropout=0.0)
    x = torch.randn(1, 12, 8)
    mask = torch.ones(1, 12)
    out = model(x, mask=mask)
    assert out.logits.shape == (1, 12, 4)


def test_ms_tcn_eval_mode_no_dropout_noise() -> None:
    model = MSTCNModel(input_size=8, num_classes=4, num_stages=2, num_layers=2, num_f_maps=8, dropout=0.5)
    model.eval()
    x = torch.randn(1, 20, 8)
    out_a = model.predict_classes(x)
    out_b = model.predict_classes(x)
    assert torch.equal(out_a, out_b)


def test_ms_tcn_factory_kwargs() -> None:
    factory = get_model_factory("ms_tcn")
    model = factory(input_size=10, num_classes=3, num_stages=1, num_layers=2, num_f_maps=8)
    assert model.input_size == 10
    assert model.num_classes == 3


def test_ms_tcn_paper_defaults_build() -> None:
    model = build_model(
        "ms_tcn",
        input_size=99,
        num_classes=8,
        num_stages=4,
        num_layers=10,
        num_f_maps=64,
        kernel_size=3,
        dropout=0.5,
    )
    x = torch.randn(1, 100, 99)
    output = model(x)
    assert output.logits.shape == (1, 100, 8)
