"""MS-TCN model adapter for SnatchPhaseBench."""

from __future__ import annotations

import torch

from snatch_phase_bench.models.base import ModelOutput, TemporalSegmentationModel
from snatch_phase_bench.models.ms_tcn.core import MultiStageTCN


class MSTCNModel(TemporalSegmentationModel):
    """Multi-Stage Temporal Convolutional Network (Farha & Gall, CVPR 2019)."""

    name = "ms_tcn"

    def __init__(
        self,
        input_size: int,
        num_classes: int,
        num_stages: int = 4,
        num_layers: int = 10,
        num_f_maps: int = 64,
        kernel_size: int = 3,
        dropout: float = 0.5,
    ) -> None:
        super().__init__()
        self.input_size = input_size
        self.num_classes = num_classes
        self.num_stages = num_stages
        self.num_layers = num_layers
        self.num_f_maps = num_f_maps
        self.kernel_size = kernel_size
        self.dropout = dropout
        self._core = MultiStageTCN(
            input_dim=input_size,
            num_classes=num_classes,
            num_stages=num_stages,
            num_layers=num_layers,
            num_f_maps=num_f_maps,
            kernel_size=kernel_size,
            dropout=dropout,
        )

    @property
    def input_layout(self) -> str:
        return "frame_sequence"

    @property
    def core(self) -> MultiStageTCN:
        return self._core

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> ModelOutput:
        """
        Args:
            x: ``(batch, time, features)`` pose sequence
            mask: optional ``(batch, time)`` or ``(batch, 1, time)`` validity mask
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
