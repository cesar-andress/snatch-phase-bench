"""Load evaluation settings from the benchmark manifest."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from snatch_phase_bench.ontology.loader import load_benchmark_manifest, load_label_mapping, load_ontology


@dataclass(frozen=True)
class EvaluationConfig:
    version: str
    segment_interval_convention: str
    segment_iou_thresholds: tuple[float, ...]
    boundary_tolerances_frames: tuple[int, ...]
    ignored_label_names: tuple[str, ...]
    fps_policy: str
    aggregation_policy: dict[str, str]
    ontology_path: Path
    mapping_b0_path: Path | None


def load_evaluation_config(manifest_path: Path | None = None) -> EvaluationConfig:
    manifest = load_benchmark_manifest(manifest_path)
    evaluation = manifest["evaluation"]
    ontology_block = manifest["ontology"]
    return EvaluationConfig(
        version=str(evaluation["version"]),
        segment_interval_convention=str(evaluation.get("segment_interval_convention", "half_open")),
        segment_iou_thresholds=tuple(float(v) for v in evaluation["segment_iou_thresholds"]),
        boundary_tolerances_frames=tuple(int(v) for v in evaluation["boundary_tolerances_frames"]),
        ignored_label_names=tuple(str(v) for v in evaluation.get("ignored_label_names", ["unlabeled"])),
        fps_policy=str(evaluation.get("fps_policy", "explicit_required_for_ms")),
        aggregation_policy=dict(evaluation.get("aggregation_policy", {})),
        ontology_path=Path(str(ontology_block["canonical"])),
        mapping_b0_path=Path(str(ontology_block["mapping_b0"]))
        if ontology_block.get("mapping_b0")
        else None,
    )


def ignored_label_ids(ontology_path: Path, ignored_names: tuple[str, ...]) -> tuple[int, ...]:
    ontology = load_ontology(ontology_path)
    ids: list[int] = []
    for name in ignored_names:
        if name not in ontology.name_to_id:
            raise KeyError(f"Ignored label {name!r} not in ontology {ontology.ontology_id}")
        ids.append(ontology.name_to_id[name])
    return tuple(ids)


def load_evaluation_artifacts(config: EvaluationConfig) -> dict[str, Any]:
    ontology = load_ontology(config.ontology_path)
    mapping = load_label_mapping(config.mapping_b0_path) if config.mapping_b0_path else None
    ignore_ids = ignored_label_ids(config.ontology_path, config.ignored_label_names)
    return {
        "ontology": ontology,
        "mapping_b0": mapping,
        "ignore_label_ids": ignore_ids,
    }
