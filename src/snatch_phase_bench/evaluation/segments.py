"""Canonical segment representation and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from snatch_phase_bench.ontology.phase_ontology import PhaseOntology


@dataclass(frozen=True)
class CanonicalSegment:
    """
    Canonical segment on a discrete frame timeline.

    Intervals use the **half-open** convention ``[start_frame, end_frame)``:
    ``start_frame`` is inclusive, ``end_frame`` is exclusive.
    """

    video_id: str
    label: int
    start_frame: int
    end_frame: int
    ontology_id: str
    ontology_version: str

    def __post_init__(self) -> None:
        if self.start_frame < 0:
            raise ValueError(f"start_frame must be >= 0, got {self.start_frame}")
        if self.end_frame <= self.start_frame:
            raise ValueError(
                f"end_frame must be > start_frame ({self.start_frame}), got {self.end_frame}"
            )

    def length(self) -> int:
        return self.end_frame - self.start_frame

    def temporal_iou(self, other: CanonicalSegment) -> float:
        inter_start = max(self.start_frame, other.start_frame)
        inter_end = min(self.end_frame, other.end_frame)
        inter = max(0, inter_end - inter_start)
        if inter == 0:
            return 0.0
        union = self.length() + other.length() - inter
        return inter / union if union > 0 else 0.0


def validate_label_sequence(
    labels: np.ndarray,
    ontology: PhaseOntology,
    *,
    ignore_labels: Iterable[int] | None = (0,),
) -> None:
    """Raise ``ValueError`` if any non-ignored label is unknown in the ontology."""
    ignore = set(ignore_labels or ())
    known = set(ontology.id_to_name)
    for value in np.asarray(labels, dtype=np.int64).ravel():
        label = int(value)
        if label in ignore:
            continue
        if label not in known:
            raise ValueError(
                f"Unknown label {label} for ontology {ontology.ontology_id}; known={sorted(known)}"
            )


def labels_to_canonical_segments(
    labels: np.ndarray,
    *,
    video_id: str,
    ontology: PhaseOntology,
    ignore_labels: Iterable[int] | None = (0,),
) -> list[CanonicalSegment]:
    """
    Convert a per-frame label sequence into contiguous canonical segments.

    Consecutive duplicate labels collapse into one segment. Ignored labels are
    omitted from the segment list but still split contiguous runs.
    """
    array = np.asarray(labels, dtype=np.int64).ravel()
    validate_label_sequence(array, ontology, ignore_labels=ignore_labels)
    ignore = set(ignore_labels or ())

    if len(array) == 0:
        return []

    segments: list[CanonicalSegment] = []
    start = 0
    current = int(array[0])
    for index in range(1, len(array)):
        label = int(array[index])
        if label != current:
            if current not in ignore:
                segments.append(
                    CanonicalSegment(
                        video_id=video_id,
                        label=current,
                        start_frame=start,
                        end_frame=index,
                        ontology_id=ontology.ontology_id,
                        ontology_version=ontology.version,
                    )
                )
            start = index
            current = label
    if current not in ignore:
        segments.append(
            CanonicalSegment(
                video_id=video_id,
                label=current,
                start_frame=start,
                end_frame=len(array),
                ontology_id=ontology.ontology_id,
                ontology_version=ontology.version,
            )
        )
    return segments


def validate_non_overlapping(segments: list[CanonicalSegment]) -> None:
    """Ensure segments are sorted and non-overlapping on the same timeline."""
    if not segments:
        return
    ordered = sorted(segments, key=lambda segment: segment.start_frame)
    for previous, current in zip(ordered, ordered[1:], strict=False):
        if current.start_frame < previous.end_frame:
            raise ValueError(
                "Overlapping segments are not allowed: "
                f"{previous} overlaps {current}"
            )


def canonical_to_legacy_segments(
    segments: list[CanonicalSegment],
) -> list[tuple[int, int, int]]:
    """Return ``(start, end, label)`` tuples for backward-compatible metric code."""
    return [(segment.start_frame, segment.end_frame, segment.label) for segment in segments]
