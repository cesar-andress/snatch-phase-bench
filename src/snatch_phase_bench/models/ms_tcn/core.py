"""Multi-stage MS-TCN core network."""

from __future__ import annotations

import copy

import torch
import torch.nn as nn
import torch.nn.functional as F

from snatch_phase_bench.models.ms_tcn.blocks import SingleStageModel


class MultiStageTCN(nn.Module):
    """Multi-stage temporal convolutional network (paper Sec. 3.2)."""

    def __init__(
        self,
        input_dim: int,
        num_classes: int,
        num_stages: int,
        num_layers: int,
        num_f_maps: int,
        kernel_size: int,
        dropout: float,
    ) -> None:
        super().__init__()
        if num_stages < 1:
            raise ValueError("num_stages must be >= 1")

        self.stage1 = SingleStageModel(
            input_dim,
            num_classes,
            num_layers,
            num_f_maps,
            kernel_size,
            dropout,
        )
        self.stages = nn.ModuleList(
            [
                copy.deepcopy(
                    SingleStageModel(
                        num_classes,
                        num_classes,
                        num_layers,
                        num_f_maps,
                        kernel_size,
                        dropout,
                    )
                )
                for _ in range(num_stages - 1)
            ]
        )

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: ``(batch, input_dim, time)``
            mask: ``(batch, 1, time)`` binary mask

        Returns:
            Stage logits stacked as ``(num_stages, batch, num_classes, time)``.
        """
        out = self.stage1(x, mask)
        outputs = out.unsqueeze(0)
        for stage in self.stages:
            out = stage(F.softmax(out, dim=1) * mask[:, 0:1, :], mask)
            outputs = torch.cat((outputs, out.unsqueeze(0)), dim=0)
        return outputs
