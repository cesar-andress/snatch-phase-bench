"""Unit tests for MS-TCN loss."""

from __future__ import annotations

import torch
import torch.nn as nn

from snatch_phase_bench.models.ms_tcn.loss import compute_mstcn_loss, truncated_log_smoothing_loss


def test_truncated_smoothing_loss_is_non_negative() -> None:
    logits = torch.randn(1, 4, 20)
    mask = torch.ones(1, 1, 20)
    loss = truncated_log_smoothing_loss(logits, mask=mask, tau=4.0)
    assert float(loss.item()) >= 0.0


def test_compute_mstcn_loss_sums_stages() -> None:
    stage_logits = torch.randn(3, 1, 5, 12)
    targets = torch.randint(1, 5, (1, 12))
    mask = torch.ones(1, 1, 12)
    ce = nn.CrossEntropyLoss(ignore_index=0)
    loss, metrics = compute_mstcn_loss(
        stage_logits,
        targets,
        mask=mask,
        ce_loss=ce,
        tmse_weight=0.15,
        tmse_truncate_tau=4.0,
    )
    assert loss.ndim == 0
    assert metrics["loss_total"] >= 0.0
