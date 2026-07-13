"""Dilated residual blocks and single-stage TCN for MS-TCN."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class DilatedResidualLayer(nn.Module):
    """Dilated residual layer (paper Eq. 1-2; author release padding)."""

    def __init__(self, dilation: int, channels: int, kernel_size: int, dropout: float) -> None:
        super().__init__()
        self.conv_dilated = nn.Conv1d(
            channels,
            channels,
            kernel_size,
            padding=dilation,
            dilation=dilation,
        )
        self.conv_1x1 = nn.Conv1d(channels, channels, 1)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        out = F.relu(self.conv_dilated(x))
        out = self.conv_1x1(out)
        out = self.dropout(out)
        return (x + out) * mask[:, 0:1, :]


class SingleStageModel(nn.Module):
    """Single-stage temporal convolutional network (paper Sec. 3.1)."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        num_layers: int,
        num_f_maps: int,
        kernel_size: int,
        dropout: float,
    ) -> None:
        super().__init__()
        self.conv_1x1_in = nn.Conv1d(in_channels, num_f_maps, 1)
        self.layers = nn.ModuleList(
            [
                DilatedResidualLayer(2**layer_idx, num_f_maps, kernel_size, dropout)
                for layer_idx in range(num_layers)
            ]
        )
        self.conv_out = nn.Conv1d(num_f_maps, out_channels, 1)

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        out = self.conv_1x1_in(x)
        for layer in self.layers:
            out = layer(out, mask)
        out = self.conv_out(out) * mask[:, 0:1, :]
        return out
