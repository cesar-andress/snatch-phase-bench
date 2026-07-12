"""Model registry for configuration-driven experiments."""

from __future__ import annotations

from typing import Callable, TypeVar

from snatch_phase_bench.models.base import TemporalSegmentationModel
from snatch_phase_bench.models.lstm_baseline import LSTMBaselineModel

T = TypeVar("T", bound=TemporalSegmentationModel)

ModelFactory = Callable[..., TemporalSegmentationModel]

_REGISTRY: dict[str, ModelFactory] = {
    "lstm_baseline": LSTMBaselineModel,
    # Future: "gru", "tcn", "ms_tcn", "st_gcn", "transformer"
}


def register_model(name: str, factory: ModelFactory) -> None:
    """Register a model factory under ``name``."""
    if name in _REGISTRY:
        raise ValueError(f"Model '{name}' is already registered.")
    _REGISTRY[name] = factory


def get_model_factory(name: str) -> ModelFactory:
    """Return factory for ``name``."""
    if name not in _REGISTRY:
        supported = ", ".join(sorted(_REGISTRY))
        raise KeyError(f"Unknown model '{name}'. Supported: {supported}")
    return _REGISTRY[name]


def build_model(name: str, **kwargs: object) -> TemporalSegmentationModel:
    """Instantiate a registered model."""
    return get_model_factory(name)(**kwargs)


def list_models() -> list[str]:
    """Return registered model names."""
    return sorted(_REGISTRY.keys())
