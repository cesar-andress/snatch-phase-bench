"""Machine-readable evaluation result schema."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from snatch_phase_bench.evaluation.metrics.boundary import BoundaryMetricsResult
from snatch_phase_bench.evaluation.metrics.segment import SegmentMetricsResult


SCHEMA_VERSION = "1.0.0"


@dataclass
class VideoEvaluationRecord:
    video_id: str
    athlete_id: str | None
    fps: float | None
    fps_source: str | None
    segment: dict[str, Any]
    boundary: dict[str, Any]
    warnings: list[str] = field(default_factory=list)


@dataclass
class BenchmarkEvaluationResult:
    schema_version: str
    created_at: str
    dataset_version: str
    split_version: str
    ontology_id: str
    ontology_version: str
    mapping_id: str | None
    mapping_version: str | None
    metric_implementation_version: str
    model_identifier: str
    config_hash: str
    evaluation_derived: bool
    fps_policy: str
    per_video: dict[str, VideoEvaluationRecord]
    per_transition: dict[str, dict[str, Any]]
    aggregate: dict[str, Any]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["per_video"] = {
            key: asdict(value) if isinstance(value, VideoEvaluationRecord) else value
            for key, value in self.per_video.items()
        }
        return payload

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def hash_config(config: dict[str, Any]) -> str:
    encoded = json.dumps(config, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def serialize_segment_metrics(result: SegmentMetricsResult) -> dict[str, Any]:
    return {
        "edit_score": result.edit.normalized_score,
        "edit_levenshtein_distance": result.edit.levenshtein_distance,
        "aggregate": result.aggregate,
        "per_class": {str(class_id): metrics for class_id, metrics in result.per_class.items()},
    }


def serialize_boundary_metrics(result: BoundaryMetricsResult) -> dict[str, Any]:
    per_transition = {
        key: {
            "transition_key": item.transition_key,
            "num_matched": item.num_matched,
            "num_missed": item.num_missed,
            "num_extra": item.num_extra,
            "mae_frames": item.mae_frames,
            "median_ae_frames": item.median_ae_frames,
            "std_ae_frames": item.std_ae_frames,
            "max_ae_frames": item.max_ae_frames,
            "mae_ms": item.mae_ms,
            "median_ae_ms": item.median_ae_ms,
            "precision": item.precision,
            "recall": item.recall,
            "f1": item.f1,
            "tolerance_metrics": [asdict(t) for t in item.tolerance_metrics],
            "duplicate_predicted": item.duplicate_predicted,
            "invalid_order_predicted": item.invalid_order_predicted,
            "warnings": item.warnings,
        }
        for key, item in result.per_transition.items()
    }
    return {
        "ontology_id": result.ontology_id,
        "ontology_version": result.ontology_version,
        "mapping_id": result.mapping_id,
        "mapping_version": result.mapping_version,
        "per_transition": per_transition,
        "aggregate_macro": result.aggregate_macro,
        "aggregate_micro": result.aggregate_micro,
        "fps_provenance": asdict(result.fps_provenance) if result.fps_provenance else None,
        "warnings": result.warnings,
    }


def validate_result_schema(payload: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "dataset_version",
        "split_version",
        "ontology_id",
        "metric_implementation_version",
        "model_identifier",
        "config_hash",
        "per_video",
        "aggregate",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"Evaluation result schema missing keys: {sorted(missing)}")


def write_evaluation_result(path: Path, result: BenchmarkEvaluationResult) -> None:
    payload = result.to_dict()
    validate_result_schema(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.to_json(), encoding="utf-8")


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()
