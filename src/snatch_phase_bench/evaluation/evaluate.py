"""Canonical per-video and dataset-level metric evaluation."""

from __future__ import annotations

from statistics import mean
from typing import Any

import numpy as np

from snatch_phase_bench.evaluation.metric_config import EvaluationConfig, load_evaluation_artifacts
from snatch_phase_bench.evaluation.metrics.boundary import BoundaryMetricsResult, compute_boundary_metrics
from snatch_phase_bench.evaluation.metrics.segment import SegmentMetricsResult, compute_segment_metrics_with_ontology
from snatch_phase_bench.evaluation.results import (
    BenchmarkEvaluationResult,
    VideoEvaluationRecord,
    hash_config,
    serialize_boundary_metrics,
    serialize_segment_metrics,
    utc_now_iso,
    SCHEMA_VERSION,
)
from snatch_phase_bench.ontology.loader import load_benchmark_manifest
from snatch_phase_bench.ontology.phase_ontology import LabelMapping, PhaseOntology


def evaluate_video(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    video_id: str,
    ontology: PhaseOntology,
    config: EvaluationConfig,
    ignore_label_ids: tuple[int, ...],
    fps: float | None = None,
    fps_source: str | None = None,
    label_mapping: LabelMapping | None = None,
    athlete_id: str | None = None,
) -> VideoEvaluationRecord:
    gt = np.asarray(y_true, dtype=np.int64)
    pred = np.asarray(y_pred, dtype=np.int64)
    eval_ontology = ontology
    if label_mapping is not None:
        gt = label_mapping.map_labels(gt)
        pred = label_mapping.map_labels(pred)
        eval_ontology = label_mapping.target

    segment = compute_segment_metrics_with_ontology(
        gt,
        pred,
        video_id=video_id,
        ontology=eval_ontology,
        iou_thresholds=config.segment_iou_thresholds,
        ignore_labels=ignore_label_ids,
    )
    boundary = compute_boundary_metrics(
        gt,
        pred,
        video_id=video_id,
        ontology=eval_ontology,
        ignore_labels=ignore_label_ids,
        tolerances_frames=config.boundary_tolerances_frames,
        fps=fps,
        fps_source=fps_source,
    )

    warnings = list(boundary.warnings)
    return VideoEvaluationRecord(
        video_id=video_id,
        athlete_id=athlete_id,
        fps=fps,
        fps_source=fps_source,
        segment=serialize_segment_metrics(segment),
        boundary=serialize_boundary_metrics(boundary),
        warnings=warnings,
    )


def aggregate_segment_metrics(records: dict[str, VideoEvaluationRecord]) -> dict[str, float]:
    if not records:
        return {}
    keys = next(iter(records.values())).segment["aggregate"].keys()
    return {
        key: float(mean([record.segment["aggregate"][key] for record in records.values()]))
        for key in keys
    }


def aggregate_boundary_metrics(
    records: dict[str, VideoEvaluationRecord],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    per_transition: dict[str, list[dict[str, Any]]] = {}
    micro_mae: list[float] = []
    macro_mae: list[float] = []
    warnings: list[str] = []

    for record in records.values():
        boundary = record.boundary
        warnings.extend(boundary.get("warnings", []))
        micro = boundary.get("aggregate_micro", {})
        if "boundary_mae_frames" in micro:
            micro_mae.append(float(micro["boundary_mae_frames"]))
        macro = boundary.get("aggregate_macro", {})
        if "boundary_mae_frames" in macro:
            macro_mae.append(float(macro["boundary_mae_frames"]))
        for key, payload in boundary.get("per_transition", {}).items():
            per_transition.setdefault(key, []).append(payload)

    transition_aggregate: dict[str, dict[str, Any]] = {}
    for key, items in per_transition.items():
        mae_values = [item["mae_frames"] for item in items if item["mae_frames"] is not None]
        transition_aggregate[key] = {
            "boundary_mae_frames_macro_over_videos": float(mean(mae_values)) if mae_values else None,
            "num_matched": int(sum(item["num_matched"] for item in items)),
            "num_missed": int(sum(item["num_missed"] for item in items)),
            "num_extra": int(sum(item["num_extra"] for item in items)),
        }

    aggregate = {
        "segment_macro_over_videos": aggregate_segment_metrics(records),
        "boundary_mae_frames_micro_over_videos": float(mean(micro_mae)) if micro_mae else None,
        "boundary_mae_frames_macro_over_videos": float(mean(macro_mae)) if macro_mae else None,
    }
    return aggregate, transition_aggregate


def evaluate_dataset_videos(
    videos: dict[str, dict[str, Any]],
    *,
    model_identifier: str,
    config: EvaluationConfig | None = None,
    label_mapping: LabelMapping | None = None,
    use_b0_mapping: bool = False,
) -> BenchmarkEvaluationResult:
    """
    Evaluate multiple videos.

    Each entry in ``videos`` must provide ``y_true``, ``y_pred``, and optional
    ``fps``, ``fps_source``, ``athlete_id``.
    """
    from snatch_phase_bench.evaluation.metric_config import load_evaluation_config

    manifest = load_benchmark_manifest()
    config = config or load_evaluation_config()
    artifacts = load_evaluation_artifacts(config)
    ontology: PhaseOntology = artifacts["ontology"]
    ignore_ids: tuple[int, ...] = artifacts["ignore_label_ids"]
    mapping = label_mapping
    if mapping is None and use_b0_mapping:
        mapping = artifacts["mapping_b0"]
    derived = mapping is not None

    per_video: dict[str, VideoEvaluationRecord] = {}
    for video_id, payload in videos.items():
        per_video[video_id] = evaluate_video(
            np.asarray(payload["y_true"], dtype=np.int64),
            np.asarray(payload["y_pred"], dtype=np.int64),
            video_id=video_id,
            ontology=ontology,
            config=config,
            ignore_label_ids=ignore_ids,
            fps=payload.get("fps"),
            fps_source=payload.get("fps_source"),
            label_mapping=mapping,
            athlete_id=payload.get("athlete_id"),
        )

    aggregate, per_transition = aggregate_boundary_metrics(per_video)
    config_payload = {
        "evaluation_version": config.version,
        "ontology_id": ontology.ontology_id,
        "mapping_id": mapping.mapping_id if mapping else None,
        "model_identifier": model_identifier,
    }

    return BenchmarkEvaluationResult(
        schema_version=SCHEMA_VERSION,
        created_at=utc_now_iso(),
        dataset_version=str(manifest["dataset"]["version"]),
        split_version=str(manifest["split"]["version"]),
        ontology_id=ontology.ontology_id,
        ontology_version=ontology.version,
        mapping_id=mapping.mapping_id if mapping else None,
        mapping_version=mapping.version if mapping else None,
        metric_implementation_version=config.version,
        model_identifier=model_identifier,
        config_hash=hash_config(config_payload),
        evaluation_derived=derived,
        fps_policy=config.fps_policy,
        per_video=per_video,
        per_transition=per_transition,
        aggregate=aggregate,
    )
