"""Extended tests for MS-TCN loss functions."""

from __future__ import annotations

import pytest
import torch
import torch.nn as nn

from snatch_phase_bench.models.ms_tcn.loss import compute_mstcn_loss, truncated_log_smoothing_loss


def test_truncated_smoothing_zero_for_constant_predictions() -> None:
    logits = torch.zeros(1, 3, 10)
    logits[:, 0, :] = 5.0
    mask = torch.ones(1, 1, 10)
    loss = truncated_log_smoothing_loss(logits, mask=mask, tau=4.0)
    assert float(loss.item()) == pytest.approx(0.0, abs=1e-6)


def test_truncated_smoothing_respects_tau_cap() -> None:
    logits = torch.randn(1, 4, 6)
    mask = torch.ones(1, 1, 6)
    loss_tau4 = truncated_log_smoothing_loss(logits, mask=mask, tau=4.0)
    loss_tau1 = truncated_log_smoothing_loss(logits, mask=mask, tau=1.0)
    assert float(loss_tau1.item()) <= float(loss_tau4.item())


def test_compute_mstcn_loss_increases_with_more_stages() -> None:
    targets = torch.tensor([[1, 2, 3, 4, 5]])
    mask = torch.ones(1, 1, 5)
    ce = nn.CrossEntropyLoss(ignore_index=0)
    one_stage = torch.randn(1, 1, 6, 5)
    three_stages = torch.randn(3, 1, 6, 5)
    loss_one, _ = compute_mstcn_loss(one_stage, targets, mask=mask, ce_loss=ce, tmse_weight=0.15, tmse_truncate_tau=4.0)
    loss_three, _ = compute_mstcn_loss(
        three_stages, targets, mask=mask, ce_loss=ce, tmse_weight=0.15, tmse_truncate_tau=4.0
    )
    assert float(loss_three.item()) > float(loss_one.item())


def test_compute_mstcn_loss_tmse_weight_zero_classification_only() -> None:
    stage_logits = torch.randn(2, 1, 5, 8)
    targets = torch.randint(1, 5, (1, 8))
    mask = torch.ones(1, 1, 8)
    ce = nn.CrossEntropyLoss(ignore_index=0)
    loss_with, metrics_with = compute_mstcn_loss(
        stage_logits, targets, mask=mask, ce_loss=ce, tmse_weight=0.15, tmse_truncate_tau=4.0
    )
    loss_without, metrics_without = compute_mstcn_loss(
        stage_logits, targets, mask=mask, ce_loss=ce, tmse_weight=0.0, tmse_truncate_tau=4.0
    )
    assert float(loss_without.item()) < float(loss_with.item())
    assert metrics_without["loss_tmse_mean"] >= 0.0


def test_compute_mstcn_loss_ignore_unlabeled_in_ce() -> None:
    stage_logits = torch.randn(1, 1, 4, 6)
    stage_logits[0, 0, 1, :] = 10.0
    targets = torch.tensor([[0, 0, 2, 2, 3, 3]])
    mask = torch.ones(1, 1, 6)
    ce = nn.CrossEntropyLoss(ignore_index=0)
    loss, _ = compute_mstcn_loss(
        stage_logits, targets, mask=mask, ce_loss=ce, tmse_weight=0.0, tmse_truncate_tau=4.0
    )
    assert torch.isfinite(loss)


def test_compute_mstcn_loss_metrics_keys() -> None:
    stage_logits = torch.randn(2, 1, 4, 5)
    targets = torch.randint(1, 4, (1, 5))
    mask = torch.ones(1, 1, 5)
    ce = nn.CrossEntropyLoss(ignore_index=0)
    _, metrics = compute_mstcn_loss(
        stage_logits, targets, mask=mask, ce_loss=ce, tmse_weight=0.15, tmse_truncate_tau=4.0
    )
    assert {"loss_total", "loss_cls_mean", "loss_tmse_mean"} <= set(metrics.keys())
