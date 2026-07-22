"""Benchmark model registration and manifest helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml

from snatch_phase_bench.ontology.loader import PROJECT_ROOT, load_benchmark_manifest

ModelStatus = Literal[
    "verified",
    "infrastructure_ready",
    "planned",
    "frozen_exploratory_reference",
]


@dataclass(frozen=True)
class BenchmarkModelSpec:
    """One registered benchmark model or reference tier."""

    model_id: str
    tier_id: str
    status: ModelStatus
    config_path: Path | None
    registry_name: str | None
    ontology: str | None
    input_layout: str | None
    role: str | None = None
    policy_doc: str | None = None

    @property
    def is_implementable(self) -> bool:
        return self.status in {"verified", "infrastructure_ready"}

    @property
    def is_primary_comparator(self) -> bool:
        return self.tier_id == "B2" and self.status != "planned"


@dataclass(frozen=True)
class BenchmarkRegistry:
    """Resolved view of ``configs/benchmark.yaml`` model entries."""

    manifest_path: Path
    models: tuple[BenchmarkModelSpec, ...]

    def get(self, model_id: str) -> BenchmarkModelSpec:
        for spec in self.models:
            if spec.model_id == model_id:
                return spec
        supported = ", ".join(spec.model_id for spec in self.models)
        raise KeyError(f"Unknown benchmark model '{model_id}'. Known: {supported}")

    def by_tier(self, tier_id: str) -> tuple[BenchmarkModelSpec, ...]:
        return tuple(spec for spec in self.models if spec.tier_id == tier_id)

    def primary_comparators(self) -> tuple[BenchmarkModelSpec, ...]:
        return tuple(spec for spec in self.models if spec.is_primary_comparator)


def _resolve_config_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def _tier_roles(raw: dict[str, Any]) -> dict[str, str]:
    roles: dict[str, str] = {}
    for entry in raw.get("tiers", []):
        if isinstance(entry, dict) and "id" in entry:
            roles[str(entry["id"])] = str(entry.get("role", ""))
    return roles


def load_benchmark_registry(manifest_path: Path | None = None) -> BenchmarkRegistry:
    """Load benchmark model registry from the canonical manifest."""
    manifest = load_benchmark_manifest(manifest_path)
    path = Path(str(manifest["_manifest_path"]))
    tier_roles = _tier_roles(manifest)

    specs: list[BenchmarkModelSpec] = []

    baselines = manifest.get("baselines", {})
    if isinstance(baselines, dict):
        for model_id, entry in baselines.items():
            if not isinstance(entry, dict):
                continue
            specs.append(
                BenchmarkModelSpec(
                    model_id=str(model_id),
                    tier_id=str(model_id),
                    status=str(entry.get("status", "planned")),  # type: ignore[arg-type]
                    config_path=_resolve_config_path(entry.get("config")),
                    registry_name=None,
                    ontology=str(entry.get("ontology")) if entry.get("ontology") else None,
                    input_layout=str(entry.get("input_layout")) if entry.get("input_layout") else None,
                    role=entry.get("role") or tier_roles.get(str(model_id)),
                    policy_doc=str(entry.get("policy")) if entry.get("policy") else None,
                )
            )

    learned = manifest.get("learned_models", {})
    if isinstance(learned, dict):
        for model_id, entry in learned.items():
            if not isinstance(entry, dict):
                continue
            specs.append(
                BenchmarkModelSpec(
                    model_id=str(model_id),
                    tier_id=str(entry.get("tier", "B2")),
                    status=str(entry.get("status", "planned")),  # type: ignore[arg-type]
                    config_path=_resolve_config_path(entry.get("config")),
                    registry_name=str(entry.get("registry_name")) if entry.get("registry_name") else None,
                    ontology=str(entry.get("ontology")) if entry.get("ontology") else None,
                    input_layout=str(entry.get("input_layout")) if entry.get("input_layout") else None,
                    role=tier_roles.get(str(entry.get("tier", "B2"))),
                )
            )

    return BenchmarkRegistry(manifest_path=path, models=tuple(specs))


def load_model_experiment_config(config_path: Path) -> dict[str, Any]:
    """Load a benchmark model YAML experiment config."""
    config_path = config_path.resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Model config not found: {config_path}")
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid model config: {config_path}")
    payload = dict(raw)
    payload["config_path"] = str(config_path)
    return payload
