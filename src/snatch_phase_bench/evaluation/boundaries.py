"""Boundary extraction and monotonic transition-aware matching."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np

from snatch_phase_bench.evaluation.segments import labels_to_canonical_segments, validate_label_sequence
from snatch_phase_bench.ontology.phase_ontology import PhaseOntology


@dataclass(frozen=True)
class Boundary:
    """Phase transition at ``frame_index`` (first frame of the destination phase)."""

    video_id: str
    from_phase: str
    to_phase: str
    frame_index: int
    ontology_id: str
    ontology_version: str

    @property
    def transition_key(self) -> str:
        return f"{self.from_phase}->{self.to_phase}"


@dataclass
class BoundaryMatch:
    ground_truth: Boundary
    predicted: Boundary
    abs_error_frames: int


@dataclass
class BoundaryMatchingResult:
    transition_key: str
    matches: list[BoundaryMatch] = field(default_factory=list)
    unmatched_ground_truth: list[Boundary] = field(default_factory=list)
    unmatched_predicted: list[Boundary] = field(default_factory=list)
    duplicate_predicted: list[Boundary] = field(default_factory=list)
    invalid_order_predicted: list[Boundary] = field(default_factory=list)

    @property
    def num_matched(self) -> int:
        return len(self.matches)

    @property
    def num_missed(self) -> int:
        return len(self.unmatched_ground_truth)

    @property
    def num_extra(self) -> int:
        return len(self.unmatched_predicted)


def allowed_transition_keys(ontology: PhaseOntology) -> set[str]:
    return {f"{item.from_phase}->{item.to_phase}" for item in ontology.transitions}


def extract_boundaries_from_labels(
    labels: np.ndarray,
    *,
    video_id: str,
    ontology: PhaseOntology,
    ignore_labels: Iterable[int] | None = (0,),
    report_invalid: bool = True,
) -> tuple[list[Boundary], list[str]]:
    """
    Extract boundaries from a frame label sequence using ontology transitions.

    Returns boundaries and warning messages for invalid transitions.
    """
    ignore = set(ignore_labels or ())
    array = np.asarray(labels, dtype=np.int64).ravel()
    validate_label_sequence(array, ontology, ignore_labels=ignore_labels)
    allowed = allowed_transition_keys(ontology)
    warnings: list[str] = []

    boundaries: list[Boundary] = []
    if len(array) <= 1:
        return boundaries, warnings

    id_to_name = ontology.id_to_name
    previous_label: int | None = None
    for index, value in enumerate(array):
        label = int(value)
        if label in ignore:
            previous_label = None
            continue
        if previous_label is None:
            previous_label = label
            continue
        if label == previous_label:
            continue
        from_name = id_to_name[previous_label]
        to_name = id_to_name[label]
        key = f"{from_name}->{to_name}"
        if key not in allowed:
            message = (
                f"Invalid transition {key} at frame {index} in video {video_id} "
                f"(ontology {ontology.ontology_id})"
            )
            if report_invalid:
                warnings.append(message)
        else:
            boundaries.append(
                Boundary(
                    video_id=video_id,
                    from_phase=from_name,
                    to_phase=to_name,
                    frame_index=index,
                    ontology_id=ontology.ontology_id,
                    ontology_version=ontology.version,
                )
            )
        previous_label = label
    return boundaries, warnings


def extract_boundaries_from_segments(
    segments: list,
    *,
    video_id: str,
    ontology: PhaseOntology,
) -> tuple[list[Boundary], list[str]]:
    """Extract boundaries at adjacent segment interfaces."""
    if not segments:
        return [], []
    ordered = sorted(segments, key=lambda segment: segment.start_frame)
    labels = np.empty(ordered[-1].end_frame, dtype=np.int64)
    for segment in ordered:
        labels[segment.start_frame : segment.end_frame] = segment.label
    return extract_boundaries_from_labels(
        labels,
        video_id=video_id,
        ontology=ontology,
        ignore_labels=(),
        report_invalid=True,
    )


def match_boundaries_monotonic(
    ground_truth: list[Boundary],
    predicted: list[Boundary],
    *,
    transition_key: str,
    match_tolerance_frames: int | None = None,
) -> BoundaryMatchingResult:
    """
    Deterministic one-to-one monotonic matching for a single transition type.

    Each ground-truth boundary is matched to the nearest unused predicted boundary
    that occurs at or after the previous match (temporal order preserved).
    """
    gt_sorted = sorted(ground_truth, key=lambda item: item.frame_index)
    pred_sorted = sorted(predicted, key=lambda item: item.frame_index)

    result = BoundaryMatchingResult(transition_key=transition_key)
    used_pred: set[int] = set()
    last_pred_index = -1

    for gt in gt_sorted:
        best_idx = -1
        best_distance = None
        for idx, pred in enumerate(pred_sorted):
            if idx in used_pred or idx < last_pred_index:
                continue
            distance = abs(gt.frame_index - pred.frame_index)
            if match_tolerance_frames is not None and distance > match_tolerance_frames:
                continue
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_idx = idx
        if best_idx >= 0 and best_distance is not None:
            used_pred.add(best_idx)
            last_pred_index = best_idx
            pred = pred_sorted[best_idx]
            result.matches.append(
                BoundaryMatch(
                    ground_truth=gt,
                    predicted=pred,
                    abs_error_frames=best_distance,
                )
            )
        else:
            result.unmatched_ground_truth.append(gt)

    for idx, pred in enumerate(pred_sorted):
        if idx not in used_pred:
            if idx < last_pred_index:
                result.invalid_order_predicted.append(pred)
            else:
                result.unmatched_predicted.append(pred)

    frame_counts: dict[int, int] = {}
    for pred in pred_sorted:
        frame_counts[pred.frame_index] = frame_counts.get(pred.frame_index, 0) + 1
    for pred in pred_sorted:
        if frame_counts[pred.frame_index] > 1 and pred not in result.duplicate_predicted:
            result.duplicate_predicted.append(pred)

    return result


def group_boundaries_by_transition(boundaries: list[Boundary]) -> dict[str, list[Boundary]]:
    grouped: dict[str, list[Boundary]] = {}
    for boundary in boundaries:
        grouped.setdefault(boundary.transition_key, []).append(boundary)
    return grouped
