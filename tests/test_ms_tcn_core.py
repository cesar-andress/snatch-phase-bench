"""Tests for multi-stage MS-TCN core."""

from __future__ import annotations

import pytest
import torch
import torch.nn.functional as F

from snatch_phase_bench.models.ms_tcn.core import MultiStageTCN


def test_multi_stage_tcn_requires_at_least_one_stage() -> None:
    with pytest.raises(ValueError, match="num_stages"):
        MultiStageTCN(
            input_dim=8,
            num_classes=4,
            num_stages=0,
            num_layers=2,
            num_f_maps=8,
            kernel_size=3,
            dropout=0.0,
        )


def test_multi_stage_tcn_output_stage_dimension() -> None:
    model = MultiStageTCN(
        input_dim=16,
        num_classes=5,
        num_stages=4,
        num_layers=3,
        num_f_maps=16,
        kernel_size=3,
        dropout=0.0,
    )
    x = torch.randn(2, 16, 20)
    mask = torch.ones(2, 1, 20)
    outputs = model(x, mask)
    assert outputs.shape == (4, 2, 5, 20)


def test_multi_stage_tcn_single_stage() -> None:
    model = MultiStageTCN(
        input_dim=8,
        num_classes=3,
        num_stages=1,
        num_layers=2,
        num_f_maps=8,
        kernel_size=3,
        dropout=0.0,
    )
    x = torch.randn(1, 8, 12)
    mask = torch.ones(1, 1, 12)
    outputs = model(x, mask)
    assert outputs.shape[0] == 1


def test_multi_stage_tcn_later_stages_receive_softmax() -> None:
    """Stage 2+ input must be softmax probabilities (paper Eq. 6)."""
    model = MultiStageTCN(
        input_dim=4,
        num_classes=3,
        num_stages=2,
        num_layers=2,
        num_f_maps=8,
        kernel_size=3,
        dropout=0.0,
    )
    x = torch.randn(1, 4, 10)
    mask = torch.ones(1, 1, 10)
    outputs = model(x, mask)
    stage1_probs = F.softmax(outputs[0], dim=1)
    assert torch.allclose(stage1_probs.sum(dim=1), torch.ones(1, 10), atol=1e-5)


def test_multi_stage_tcn_paper_default_layer_count() -> None:
    model = MultiStageTCN(
        input_dim=99,
        num_classes=8,
        num_stages=4,
        num_layers=10,
        num_f_maps=64,
        kernel_size=3,
        dropout=0.5,
    )
    assert len(model.stage1.layers) == 10
    assert len(model.stages) == 3
    for stage in model.stages:
        assert len(stage.layers) == 10


def test_multi_stage_tcn_eval_mode_deterministic() -> None:
    model = MultiStageTCN(
        input_dim=8,
        num_classes=4,
        num_stages=2,
        num_layers=2,
        num_f_maps=8,
        kernel_size=3,
        dropout=0.0,
    )
    model.eval()
    x = torch.randn(1, 8, 16)
    mask = torch.ones(1, 1, 16)
    out1 = model(x, mask)
    out2 = model(x, mask)
    assert torch.equal(out1, out2)
