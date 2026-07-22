"""ASFormer model adapter for SnatchPhaseBench."""

from __future__ import annotations

import torch

from snatch_phase_bench.models.asformer.core import ASFormerCore
from snatch_phase_bench.models.base import ModelOutput, TemporalSegmentationModel


class ASFormerModel(TemporalSegmentationModel):
    """ASFormer (Yi, Wen, Jiang, BMVC 2021) on frame-wise pose sequences."""

    name = "asformer"

    def __init__(
        self,
        input_size: int,
        num_classes: int,
        num_decoders: int = 3,
        num_layers: int = 10,
        num_f_maps: int = 64,
        r1: int = 2,
        r2: int = 2,
        channel_masking_rate: float = 0.3,
        att_type: str = "sliding_att",
        **kwargs: object,
    ) -> None:
        super().__init__()
        # Accept unused kwargs (e.g. kernel_size/dropout from shared builders) without effect.
        _ = kwargs
        self.input_size = int(input_size)
        self.num_classes = int(num_classes)
        self.num_decoders = int(num_decoders)
        self.num_layers = int(num_layers)
        self.num_f_maps = int(num_f_maps)
        self.r1 = int(r1)
        self.r2 = int(r2)
        self.channel_masking_rate = float(channel_masking_rate)
        self.att_type = str(att_type)
        self._core = ASFormerCore(
            num_decoders=self.num_decoders,
            num_layers=self.num_layers,
            r1=self.r1,
            r2=self.r2,
            num_f_maps=self.num_f_maps,
            input_dim=self.input_size,
            num_classes=self.num_classes,
            channel_masking_rate=self.channel_masking_rate,
            att_type=self.att_type,
        )

    @property
    def input_layout(self) -> str:
        return "frame_sequence"

    @property
    def core(self) -> ASFormerCore:
        return self._core

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> ModelOutput:
        """
        Args:
            x: ``(batch, time, features)``
            mask: optional ``(batch, time)`` or ``(batch, 1, time)``
        """
        if x.ndim != 3:
            raise ValueError(f"Expected input shape (batch, time, features); got {tuple(x.shape)}")
        batch_size, seq_len, feature_dim = x.shape
        if feature_dim != self.input_size:
            raise ValueError(f"Expected feature dim {self.input_size}, got {feature_dim}")

        conv_input = x.transpose(1, 2)
        if mask is None:
            mask_tensor = torch.ones(batch_size, 1, seq_len, device=x.device, dtype=x.dtype)
        elif mask.ndim == 2:
            mask_tensor = mask.unsqueeze(1).to(dtype=x.dtype)
        else:
            mask_tensor = mask.to(dtype=x.dtype)

        stage_logits = self._core(conv_input, mask_tensor)
        final_logits = stage_logits[-1].transpose(1, 2)
        return ModelOutput(
            logits=final_logits,
            extras={
                "stage_logits": stage_logits,
                "mask": mask_tensor,
            },
        )

    def forward_stages(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """Return all stage logits ``(num_stages, batch, num_classes, time)``."""
        output = self.forward(x, mask=mask)
        assert output.extras is not None
        return output.extras["stage_logits"]

    def num_parameters(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters() if parameter.requires_grad)
