"""ASFormer core modules (Yi, Wen, Jiang, BMVC 2021).

Faithful port of ChinaYi/ASFormer ``model.py`` with documented fixes:
- sliding-window mask indexing (author-recommended; GitHub issue #2)
- device taken from input tensors (no process-global CUDA device)
"""

from __future__ import annotations

import copy
import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def exponential_decrease(idx_decoder: int, p: float = 3.0) -> float:
    """Decoder residual scale α = exp(-p * decoder_index)."""
    return math.exp(-p * idx_decoder)


class AttentionHelper(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.softmax = nn.Softmax(dim=-1)

    def scalar_dot_att(
        self,
        proj_query: torch.Tensor,
        proj_key: torch.Tensor,
        proj_val: torch.Tensor,
        padding_mask: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            proj_query/key/val: ``(B, C, L)``
            padding_mask: ``(B, 1, L)`` or broadcastable attention mask
        """
        _, c1, _ = proj_query.shape
        energy = torch.bmm(proj_query.permute(0, 2, 1), proj_key)
        attention = energy / np.sqrt(c1)
        attention = attention + torch.log(padding_mask + 1e-6)
        attention = self.softmax(attention)
        attention = attention * padding_mask
        attention = attention.permute(0, 2, 1)
        out = torch.bmm(proj_val, attention)
        return out, attention


class AttLayer(nn.Module):
    def __init__(
        self,
        q_dim: int,
        k_dim: int,
        v_dim: int,
        r1: int,
        r2: int,
        r3: int,
        bl: int,
        stage: str,
        att_type: str,
    ) -> None:
        super().__init__()
        self.query_conv = nn.Conv1d(q_dim, q_dim // r1, kernel_size=1)
        self.key_conv = nn.Conv1d(k_dim, k_dim // r2, kernel_size=1)
        self.value_conv = nn.Conv1d(v_dim, v_dim // r3, kernel_size=1)
        self.conv_out = nn.Conv1d(v_dim // r3, v_dim, kernel_size=1)
        self.bl = int(bl)
        self.stage = stage
        self.att_type = att_type
        if self.att_type not in {"normal_att", "block_att", "sliding_att"}:
            raise ValueError(f"Unknown att_type={att_type}")
        if self.stage not in {"encoder", "decoder"}:
            raise ValueError(f"Unknown stage={stage}")
        self.att_helper = AttentionHelper()

    def _construct_window_mask(self, device: torch.device, dtype: torch.dtype) -> torch.Tensor:
        """Sliding-window mask with author-recommended indexing fix (issue #2)."""
        width = self.bl + 2 * (self.bl // 2)
        window_mask = torch.zeros((1, self.bl, width), device=device, dtype=dtype)
        for i in range(self.bl):
            window_mask[:, i, i : i + self.bl] = 1
        return window_mask

    def forward(
        self,
        x1: torch.Tensor,
        x2: torch.Tensor | None,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        query = self.query_conv(x1)
        key = self.key_conv(x1)
        if self.stage == "decoder":
            if x2 is None:
                raise ValueError("Decoder AttLayer requires encoder/previous features.")
            value = self.value_conv(x2)
        else:
            value = self.value_conv(x1)

        if self.att_type == "normal_att":
            return self._normal_self_att(query, key, value, mask)
        if self.att_type == "block_att":
            return self._block_wise_self_att(query, key, value, mask)
        return self._sliding_window_self_att(query, key, value, mask)

    def _normal_self_att(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        m_batchsize, _, length = q.size()
        padding_mask = torch.ones((m_batchsize, 1, length), device=q.device, dtype=q.dtype) * mask[:, 0:1, :]
        output, _ = self.att_helper.scalar_dot_att(q, k, v, padding_mask)
        output = self.conv_out(F.relu(output))
        return output[:, :, 0:length] * mask[:, 0:1, :]

    def _block_wise_self_att(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        m_batchsize, c1, length = q.size()
        _, c2, _ = k.size()
        _, c3, _ = v.size()
        nb = length // self.bl
        if length % self.bl != 0:
            pad = self.bl - length % self.bl
            q = torch.cat([q, torch.zeros((m_batchsize, c1, pad), device=q.device, dtype=q.dtype)], dim=-1)
            k = torch.cat([k, torch.zeros((m_batchsize, c2, pad), device=k.device, dtype=k.dtype)], dim=-1)
            v = torch.cat([v, torch.zeros((m_batchsize, c3, pad), device=v.device, dtype=v.dtype)], dim=-1)
            nb += 1
        padding_mask = torch.cat(
            [
                torch.ones((m_batchsize, 1, length), device=q.device, dtype=q.dtype) * mask[:, 0:1, :],
                torch.zeros((m_batchsize, 1, self.bl * nb - length), device=q.device, dtype=q.dtype),
            ],
            dim=-1,
        )
        q = q.reshape(m_batchsize, c1, nb, self.bl).permute(0, 2, 1, 3).reshape(m_batchsize * nb, c1, self.bl)
        padding_mask = (
            padding_mask.reshape(m_batchsize, 1, nb, self.bl)
            .permute(0, 2, 1, 3)
            .reshape(m_batchsize * nb, 1, self.bl)
        )
        k = k.reshape(m_batchsize, c2, nb, self.bl).permute(0, 2, 1, 3).reshape(m_batchsize * nb, c2, self.bl)
        v = v.reshape(m_batchsize, c3, nb, self.bl).permute(0, 2, 1, 3).reshape(m_batchsize * nb, c3, self.bl)
        output, _ = self.att_helper.scalar_dot_att(q, k, v, padding_mask)
        output = self.conv_out(F.relu(output))
        output = output.reshape(m_batchsize, nb, c3, self.bl).permute(0, 2, 1, 3).reshape(
            m_batchsize, c3, nb * self.bl
        )
        return output[:, :, 0:length] * mask[:, 0:1, :]

    def _sliding_window_self_att(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        m_batchsize, c1, length = q.size()
        _, c2, _ = k.size()
        _, c3, _ = v.size()
        if m_batchsize != 1:
            raise ValueError("ASFormer sliding_att currently requires batch_size=1 (author release).")

        nb = length // self.bl
        if length % self.bl != 0:
            pad = self.bl - length % self.bl
            q = torch.cat([q, torch.zeros((m_batchsize, c1, pad), device=q.device, dtype=q.dtype)], dim=-1)
            k = torch.cat([k, torch.zeros((m_batchsize, c2, pad), device=k.device, dtype=k.dtype)], dim=-1)
            v = torch.cat([v, torch.zeros((m_batchsize, c3, pad), device=v.device, dtype=v.dtype)], dim=-1)
            nb += 1

        padding_mask = torch.cat(
            [
                torch.ones((m_batchsize, 1, length), device=q.device, dtype=q.dtype) * mask[:, 0:1, :],
                torch.zeros((m_batchsize, 1, self.bl * nb - length), device=q.device, dtype=q.dtype),
            ],
            dim=-1,
        )
        q = q.reshape(m_batchsize, c1, nb, self.bl).permute(0, 2, 1, 3).reshape(m_batchsize * nb, c1, self.bl)

        half = self.bl // 2
        k = torch.cat(
            [
                torch.zeros(m_batchsize, c2, half, device=k.device, dtype=k.dtype),
                k,
                torch.zeros(m_batchsize, c2, half, device=k.device, dtype=k.dtype),
            ],
            dim=-1,
        )
        v = torch.cat(
            [
                torch.zeros(m_batchsize, c3, half, device=v.device, dtype=v.dtype),
                v,
                torch.zeros(m_batchsize, c3, half, device=v.device, dtype=v.dtype),
            ],
            dim=-1,
        )
        padding_mask = torch.cat(
            [
                torch.zeros(m_batchsize, 1, half, device=q.device, dtype=q.dtype),
                padding_mask,
                torch.zeros(m_batchsize, 1, half, device=q.device, dtype=q.dtype),
            ],
            dim=-1,
        )

        k = torch.cat([k[:, :, i * self.bl : (i + 1) * self.bl + half * 2] for i in range(nb)], dim=0)
        v = torch.cat([v[:, :, i * self.bl : (i + 1) * self.bl + half * 2] for i in range(nb)], dim=0)
        padding_mask = torch.cat(
            [padding_mask[:, :, i * self.bl : (i + 1) * self.bl + half * 2] for i in range(nb)],
            dim=0,
        )
        window_mask = self._construct_window_mask(q.device, q.dtype)
        final_mask = window_mask.repeat(m_batchsize * nb, 1, 1) * padding_mask

        output, _ = self.att_helper.scalar_dot_att(q, k, v, final_mask)
        output = self.conv_out(F.relu(output))
        output = output.reshape(m_batchsize, nb, -1, self.bl).permute(0, 2, 1, 3).reshape(
            m_batchsize, -1, nb * self.bl
        )
        return output[:, :, 0:length] * mask[:, 0:1, :]


class ConvFeedForward(nn.Module):
    def __init__(self, dilation: int, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.layer = nn.Sequential(
            nn.Conv1d(in_channels, out_channels, 3, padding=dilation, dilation=dilation),
            nn.ReLU(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer(x)


class AttModule(nn.Module):
    def __init__(
        self,
        dilation: int,
        in_channels: int,
        out_channels: int,
        r1: int,
        r2: int,
        att_type: str,
        stage: str,
        alpha: float,
    ) -> None:
        super().__init__()
        self.feed_forward = ConvFeedForward(dilation, in_channels, out_channels)
        self.instance_norm = nn.InstanceNorm1d(in_channels, track_running_stats=False)
        # Author release passes dilation as the attention window size ``bl``.
        self.att_layer = AttLayer(
            in_channels,
            in_channels,
            out_channels,
            r1,
            r1,
            r2,
            dilation,
            att_type=att_type,
            stage=stage,
        )
        self.conv_1x1 = nn.Conv1d(out_channels, out_channels, 1)
        self.dropout = nn.Dropout()
        self.alpha = float(alpha)

    def forward(self, x: torch.Tensor, f: torch.Tensor | None, mask: torch.Tensor) -> torch.Tensor:
        out = self.feed_forward(x)
        out = self.alpha * self.att_layer(self.instance_norm(out), f, mask) + out
        out = self.conv_1x1(out)
        out = self.dropout(out)
        return (x + out) * mask[:, 0:1, :]


class Encoder(nn.Module):
    def __init__(
        self,
        num_layers: int,
        r1: int,
        r2: int,
        num_f_maps: int,
        input_dim: int,
        num_classes: int,
        channel_masking_rate: float,
        att_type: str,
        alpha: float,
    ) -> None:
        super().__init__()
        self.conv_1x1 = nn.Conv1d(input_dim, num_f_maps, 1)
        self.layers = nn.ModuleList(
            [
                AttModule(2**i, num_f_maps, num_f_maps, r1, r2, att_type, "encoder", alpha)
                for i in range(num_layers)
            ]
        )
        self.conv_out = nn.Conv1d(num_f_maps, num_classes, 1)
        self.dropout = nn.Dropout2d(p=channel_masking_rate)
        self.channel_masking_rate = float(channel_masking_rate)

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        if self.channel_masking_rate > 0:
            x = x.unsqueeze(2)
            x = self.dropout(x)
            x = x.squeeze(2)
        feature = self.conv_1x1(x)
        for layer in self.layers:
            feature = layer(feature, None, mask)
        out = self.conv_out(feature) * mask[:, 0:1, :]
        return out, feature


class Decoder(nn.Module):
    def __init__(
        self,
        num_layers: int,
        r1: int,
        r2: int,
        num_f_maps: int,
        input_dim: int,
        num_classes: int,
        att_type: str,
        alpha: float,
    ) -> None:
        super().__init__()
        self.conv_1x1 = nn.Conv1d(input_dim, num_f_maps, 1)
        self.layers = nn.ModuleList(
            [
                AttModule(2**i, num_f_maps, num_f_maps, r1, r2, att_type, "decoder", alpha)
                for i in range(num_layers)
            ]
        )
        self.conv_out = nn.Conv1d(num_f_maps, num_classes, 1)

    def forward(
        self,
        x: torch.Tensor,
        fencoder: torch.Tensor,
        mask: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        feature = self.conv_1x1(x)
        for layer in self.layers:
            feature = layer(feature, fencoder, mask)
        out = self.conv_out(feature) * mask[:, 0:1, :]
        return out, feature


class ASFormerCore(nn.Module):
    """Official ``MyTransformer``: 1 encoder + ``num_decoders`` refinement stages."""

    def __init__(
        self,
        num_decoders: int,
        num_layers: int,
        r1: int,
        r2: int,
        num_f_maps: int,
        input_dim: int,
        num_classes: int,
        channel_masking_rate: float,
        att_type: str = "sliding_att",
    ) -> None:
        super().__init__()
        self.encoder = Encoder(
            num_layers,
            r1,
            r2,
            num_f_maps,
            input_dim,
            num_classes,
            channel_masking_rate,
            att_type=att_type,
            alpha=1.0,
        )
        self.decoders = nn.ModuleList(
            [
                copy.deepcopy(
                    Decoder(
                        num_layers,
                        r1,
                        r2,
                        num_f_maps,
                        num_classes,
                        num_classes,
                        att_type=att_type,
                        alpha=exponential_decrease(stage_idx),
                    )
                )
                for stage_idx in range(num_decoders)
            ]
        )

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: ``(batch, channels, time)``
            mask: ``(batch, 1, time)``
        Returns:
            stage logits ``(1 + num_decoders, batch, num_classes, time)``
        """
        out, feature = self.encoder(x, mask)
        outputs = out.unsqueeze(0)
        for decoder in self.decoders:
            out, feature = decoder(F.softmax(out, dim=1) * mask[:, 0:1, :], feature * mask[:, 0:1, :], mask)
            outputs = torch.cat((outputs, out.unsqueeze(0)), dim=0)
        return outputs
