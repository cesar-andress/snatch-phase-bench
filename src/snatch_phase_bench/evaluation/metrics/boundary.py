"""Boundary timing metrics for temporal phase segmentation."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, median, pstdev
from typing import Iterable

import numpy as np

from snatch_phase_bench.evaluation.boundaries import (
    Boundary,
    BoundaryMatchingResult,
    allowed_transition_keys,
    extract_boundaries_from_labels,
    group_boundaries_by_transition,
    match_boundaries_monotonic,
)
from snatch_phase_bench.ontology.loader import load_label_mapping, load_ontology
from snatch_phase_bench.ontology.phase_ontology import LabelMapping, PhaseOntology


class FpsRequiredError(ValueError):
    """Raised when millisecond metrics are requested without explicit FPS."""


def frames_to_milliseconds(frame_error: float, fps: float) -> float:
    if fps <= 0:
        raise ValueError(f"fps must be positive, got {fps}")
    return frame_error * 1000.0 / fps


def require_fps(fps: float | None, *, context: str) -> float:
    if fps is None:
        raise FpsRequiredError(
            f"Millisecond metrics require an explicit fps value ({context}). "
            "Native video FPS is not yet verified for this dataset."
        )
    return fps


@dataclass(frozen=True)
class FpsProvenance:
    source: str
    value: float


@dataclass
class BoundaryToleranceMetrics:
    tolerance_frames: int
    hit_rate: float
    hits: int
    matched: int
    tolerance_ms: float | None = None


@dataclass
class BoundaryTransitionMetrics:
    transition_key: str
    num_matched: int = 0
    num_missed: int = 0
    num_extra: int = 0
    mae_frames: float | None = None
    median_ae_frames: float | None = None
    std_ae_frames: float | None = None
    max_ae_frames: int | None = None
    mae_ms: float | None = None
    median_ae_ms: float | None = None
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    tolerance_metrics: list[BoundaryToleranceMetrics] = field(default_factory=list)
    duplicate_predicted: int = 0
    invalid_order_predicted: int = 0
    warnings: list[str] = field(default_factory=list)


@dataclass
class BoundaryMetricsResult:
    ontology_id: str
    ontology_version: str
    mapping_id: str | None
    mapping_version: str | None
    per_transition: dict[str, BoundaryTransitionMetrics] = field(default_factory=dict)
    aggregate_macro: dict[str, float] = field(default_factory=dict)
    aggregate_micro: dict[str, float] = field(default_factory=dict)
    fps_provenance: FpsProvenance | None = None
    warnings: list[str] = field(default_factory=list)


def _safe_mean(values: list[float]) -> float | None:
    return float(mean(values)) if values else None


def _safe_median(values: list[float]) -> float | None:
    return float(median(values)) if values else None


def _safe_std(values: list[float]) -> float | None:
    return float(pstdev(values)) if len(values) > 1 else (0.0 if len(values) == 1 else None)


def compute_transition_boundary_metrics(
    matching: BoundaryMatchingResult,
    *,
    tolerances_frames: Iterable[int] = (1, 2, 3),
    fps: float | None = None,
    fps_source: str | None = None,
) -> BoundaryTransitionMetrics:
    errors = [match.abs_error_frames for match in matching.matches]
    metrics = BoundaryTransitionMetrics(
        transition_key=matching.transition_key,
        num_matched=matching.num_matched,
        num_missed=matching.num_missed,
        num_extra=matching.num_extra,
        duplicate_predicted=len(matching.duplicate_predicted),
        invalid_order_predicted=len(matching.invalid_order_predicted),
    )

    predicted_total = matching.num_matched + matching.num_extra
    metrics.precision = (
        matching.num_matched / predicted_total if predicted_total else 0.0
    )
    metrics.recall = (
        matching.num_matched / (matching.num_matched + matching.num_missed)
        if (matching.num_matched + matching.num_missed)
        else 0.0
    )
    if metrics.precision + metrics.recall == 0:
        metrics.f1 = 0.0
    else:
        metrics.f1 = 2 * metrics.precision * metrics.recall / (metrics.precision + metrics.recall)

    if errors:
        metrics.mae_frames = _safe_mean([float(value) for value in errors])
        metrics.median_ae_frames = _safe_median([float(value) for value in errors])
        metrics.std_ae_frames = _safe_std([float(value) for value in errors])
        metrics.max_ae_frames = max(errors)

    if fps is not None:
        require_fps(fps, context=f"transition {matching.transition_key}")
        if metrics.mae_frames is not None:
            metrics.mae_ms = frames_to_milliseconds(metrics.mae_frames, fps)
        if metrics.median_ae_frames is not None:
            metrics.median_ae_ms = frames_to_milliseconds(metrics.median_ae_frames, fps)

    for tolerance in tolerances_frames:
        hits = sum(1 for match in matching.matches if match.abs_error_frames <= tolerance)
        hit_rate = hits / len(matching.matches) if matching.matches else 0.0
        tolerance_ms = None
        if fps is not None:
            tolerance_ms = frames_to_milliseconds(float(tolerance), fps)
        metrics.tolerance_metrics.append(
            BoundaryToleranceMetrics(
                tolerance_frames=tolerance,
                hit_rate=hit_rate,
                hits=hits,
                matched=len(matching.matches),
                tolerance_ms=tolerance_ms,
            )
        )

    if fps is not None and fps_source is None:
        metrics.warnings.append("fps provided without provenance source")

    return metrics


def compute_boundary_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    video_id: str,
    ontology: PhaseOntology,
    ignore_labels: Iterable[int] | None = (0,),
    tolerances_frames: Iterable[int] = (1, 2, 3),
    fps: float | None = None,
    fps_source: str | None = None,
    label_mapping: LabelMapping | None = None,
) -> BoundaryMetricsResult:
    """
    Compute ontology-aware boundary metrics for one video.

    If ``label_mapping`` is supplied, labels are mapped for evaluation only;
    input arrays are not modified.
    """
    gt = np.asarray(y_true, dtype=np.int64).copy()
    pred = np.asarray(y_pred, dtype=np.int64).copy()
    mapping_id = None
    mapping_version = None
    if label_mapping is not None:
        gt = label_mapping.map_labels(gt)
        pred = label_mapping.map_labels(pred)
        ontology = label_mapping.target
        mapping_id = label_mapping.mapping_id
        mapping_version = label_mapping.version

    gt_boundaries, gt_warnings = extract_boundaries_from_labels(
        gt, video_id=video_id, ontology=ontology, ignore_labels=ignore_labels
    )
    pred_boundaries, pred_warnings = extract_boundaries_from_labels(
        pred, video_id=video_id, ontology=ontology, ignore_labels=ignore_labels
    )

    gt_grouped = group_boundaries_by_transition(gt_boundaries)
    pred_grouped = group_boundaries_by_transition(pred_boundaries)
    transition_keys = sorted(set(gt_grouped) | set(pred_grouped) | allowed_transition_keys(ontology))

    result = BoundaryMetricsResult(
        ontology_id=ontology.ontology_id,
        ontology_version=ontology.version,
        mapping_id=mapping_id,
        mapping_version=mapping_version,
        warnings=gt_warnings + pred_warnings,
    )
    if fps is not None and fps_source:
        result.fps_provenance = FpsProvenance(source=fps_source, value=fps)

    per_transition: dict[str, BoundaryTransitionMetrics] = {}
    macro_mae: list[float] = []
    micro_errors: list[int] = []
    micro_matched = 0
    micro_missed = 0
    micro_extra = 0

    for key in transition_keys:
        matching = match_boundaries_monotonic(
            gt_grouped.get(key, []),
            pred_grouped.get(key, []),
            transition_key=key,
        )
        transition_metrics = compute_transition_boundary_metrics(
            matching,
            tolerances_frames=tolerances_frames,
            fps=fps,
            fps_source=fps_source,
        )
        per_transition[key] = transition_metrics
        if transition_metrics.mae_frames is not None:
            macro_mae.append(transition_metrics.mae_frames)
        micro_errors.extend(match.abs_error_frames for match in matching.matches)
        micro_matched += transition_metrics.num_matched
        micro_missed += transition_metrics.num_missed
        micro_extra += transition_metrics.num_extra

    result.per_transition = per_transition
    if macro_mae:
        result.aggregate_macro["boundary_mae_frames"] = float(mean(macro_mae))
    if micro_errors:
        result.aggregate_micro["boundary_mae_frames"] = float(mean(micro_errors))
    result.aggregate_micro["boundary_matched"] = float(micro_matched)
    result.aggregate_micro["boundary_missed"] = float(micro_missed)
    result.aggregate_micro["boundary_extra"] = float(micro_extra)

    predicted_total = micro_matched + micro_extra
    recall_den = micro_matched + micro_missed
    result.aggregate_micro["boundary_precision"] = (
        micro_matched / predicted_total if predicted_total else 0.0
    )
    result.aggregate_micro["boundary_recall"] = (
        micro_matched / recall_den if recall_den else 0.0
    )
    p = result.aggregate_micro["boundary_precision"]
    r = result.aggregate_micro["boundary_recall"]
    result.aggregate_micro["boundary_f1"] = (
        2 * p * r / (p + r) if (p + r) else 0.0
    )

    if fps is not None:
        fps_value = require_fps(fps, context=f"video {video_id}")
        if "boundary_mae_frames" in result.aggregate_micro:
            result.aggregate_micro["boundary_mae_ms"] = frames_to_milliseconds(
                result.aggregate_micro["boundary_mae_frames"],
                fps_value,
            )
        if "boundary_mae_frames" in result.aggregate_macro:
            result.aggregate_macro["boundary_mae_ms"] = frames_to_milliseconds(
                result.aggregate_macro["boundary_mae_frames"],
                fps_value,
            )

    return result


def load_default_ontology() -> PhaseOntology:
    return load_ontology()


def load_default_b0_mapping() -> LabelMapping:
    return load_label_mapping()
