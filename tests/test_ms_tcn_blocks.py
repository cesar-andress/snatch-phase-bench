"""Tests for MS-TCN building blocks."""

from __future__ import annotations

import torch

from snatch_phase_bench.models.ms_tcn.blocks import DilatedResidualLayer, SingleStageModel


def test_dilated_residual_layer_preserves_time_length() -> None:
    layer = DilatedResidualLayer(dilation=4, channels=16, kernel_size=3, dropout=0.0)
    x = torch.randn(2, 16, 50)
    mask = torch.ones(2, 1, 50)
    out = layer(x, mask)
    assert out.shape == x.shape


def test_dilated_residual_layer_zero_mask_zeros_output() -> None:
    layer = DilatedResidualLayer(dilation=2, channels=8, kernel_size=3, dropout=0.0)
    x = torch.randn(1, 8, 20)
    mask = torch.zeros(1, 1, 20)
    out = layer(x, mask)
    assert torch.allclose(out, torch.zeros_like(out))


def test_dilated_residual_layer_dilation_values() -> None:
    stage = SingleStageModel(
        in_channels=4,
        out_channels=3,
        num_layers=5,
        num_f_maps=8,
        kernel_size=3,
        dropout=0.0,
    )
    expected = [1, 2, 4, 8, 16]
    actual = [layer.conv_dilated.dilation[0] for layer in stage.layers]
    assert actual == expected


def test_single_stage_model_output_shape() -> None:
    stage = SingleStageModel(
        in_channels=99,
        out_channels=8,
        num_layers=3,
        num_f_maps=16,
        kernel_size=3,
        dropout=0.0,
    )
    x = torch.randn(1, 99, 30)
    mask = torch.ones(1, 1, 30)
    logits = stage(x, mask)
    assert logits.shape == (1, 8, 30)


def test_single_stage_model_respects_partial_mask() -> None:
    stage = SingleStageModel(
        in_channels=8,
        out_channels=4,
        num_layers=2,
        num_f_maps=8,
        kernel_size=3,
        dropout=0.0,
    )
    x = torch.randn(1, 8, 10)
    mask = torch.ones(1, 1, 10)
    mask[:, :, 5:] = 0.0
    logits = stage(x, mask)
    assert torch.allclose(logits[:, :, 5:], torch.zeros(1, 4, 5))


def test_single_stage_model_supports_probability_input() -> None:
    """Later stages consume num_classes channels (softmax probabilities)."""
    stage = SingleStageModel(
        in_channels=5,
        out_channels=5,
        num_layers=2,
        num_f_maps=8,
        kernel_size=3,
        dropout=0.0,
    )
    probs = torch.softmax(torch.randn(1, 5, 15), dim=1)
    mask = torch.ones(1, 1, 15)
    out = stage(probs, mask)
    assert out.shape == (1, 5, 15)


def test_dilated_residual_layer_gradients_flow() -> None:
    layer = DilatedResidualLayer(dilation=1, channels=4, kernel_size=3, dropout=0.0)
    x = torch.randn(1, 4, 8, requires_grad=True)
    mask = torch.ones(1, 1, 8)
    out = layer(x, mask)
    out.sum().backward()
    assert x.grad is not None
    assert torch.isfinite(x.grad).all()
