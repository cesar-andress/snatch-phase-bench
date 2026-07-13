"""MS-TCN loss (classification + truncated smoothing)."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def truncated_log_smoothing_loss(
    logits: torch.Tensor,
    *,
    mask: torch.Tensor,
    tau: float,
) -> torch.Tensor:
    """
    Truncated mean squared error over frame-wise log-probabilities (paper Eq. 8-10).

    Matches the author release convention: clamp squared log-softmax differences to ``tau**2``.
    """
    log_probs = F.log_softmax(logits, dim=1)
    current = log_probs[:, :, 1:]
    previous = log_probs[:, :, :-1].detach()
    delta_sq = (current - previous).pow(2)
    truncated = torch.clamp(delta_sq, max=float(tau) ** 2)
    valid = mask[:, :, 1:]
    if valid.sum() == 0:
        return logits.new_tensor(0.0)
    return (truncated * valid).sum() / valid.sum()


def compute_mstcn_loss(
    stage_logits: torch.Tensor,
    targets: torch.Tensor,
    *,
    mask: torch.Tensor,
    ce_loss: nn.Module,
    tmse_weight: float,
    tmse_truncate_tau: float,
) -> tuple[torch.Tensor, dict[str, float]]:
    """
    Sum per-stage classification and smoothing losses (paper Eq. 12-13).

    Args:
        stage_logits: ``(num_stages, batch, num_classes, time)``
        targets: ``(batch, time)`` integer class ids
        mask: ``(batch, 1, time)``
    """
    total = stage_logits.new_tensor(0.0)
    cls_values: list[float] = []
    tmse_values: list[float] = []

    num_stages = int(stage_logits.shape[0])
    for stage_idx in range(num_stages):
        logits = stage_logits[stage_idx]
        batch_size, num_classes, seq_len = logits.shape
        cls = ce_loss(
            logits.permute(0, 2, 1).reshape(batch_size * seq_len, num_classes),
            targets.reshape(batch_size * seq_len),
        )
        tmse = truncated_log_smoothing_loss(logits, mask=mask, tau=tmse_truncate_tau)
        total = total + cls + float(tmse_weight) * tmse
        cls_values.append(float(cls.item()))
        tmse_values.append(float(tmse.item()))

    metrics = {
        "loss_total": float(total.item()),
        "loss_cls_mean": float(sum(cls_values) / len(cls_values)),
        "loss_tmse_mean": float(sum(tmse_values) / len(tmse_values)),
    }
    return total, metrics
