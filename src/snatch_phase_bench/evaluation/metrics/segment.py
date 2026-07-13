"""Segment-level temporal segmentation metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from snatch_phase_bench.evaluation.segments import CanonicalSegment, labels_to_canonical_segments
from snatch_phase_bench.ontology.phase_ontology import PhaseOntology


@dataclass(frozen=True)
class Segment:
    """Half-open interval ``[start, end)`` with class label (legacy API)."""

    start: int
    end: int
    label: int

    def length(self) -> int:
        return self.end - self.start

    def iou(self, other: Segment) -> float:
        inter_start = max(self.start, other.start)
        inter_end = min(self.end, other.end)
        inter = max(0, inter_end - inter_start)
        if inter == 0:
            return 0.0
        union = self.length() + other.length() - inter
        return inter / union if union > 0 else 0.0

    @classmethod
    def from_canonical(cls, segment: CanonicalSegment) -> Segment:
        return cls(start=segment.start_frame, end=segment.end_frame, label=segment.label)


def labels_to_segments(labels: np.ndarray, ignore_label: int | None = 0) -> list[Segment]:
    """Convert per-frame label sequence to contiguous segments (legacy helper)."""
    if len(labels) == 0:
        return []
    segments: list[Segment] = []
    start = 0
    current = int(labels[0])
    for idx in range(1, len(labels)):
        label = int(labels[idx])
        if label != current:
            if ignore_label is None or current != ignore_label:
                segments.append(Segment(start=start, end=idx, label=current))
            start = idx
            current = label
    if ignore_label is None or current != ignore_label:
        segments.append(Segment(start=start, end=len(labels), label=current))
    return segments


def _levenshtein(a: list[int], b: list[int]) -> int:
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curr.append(min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost))
        prev = curr
    return prev[-1]


@dataclass(frozen=True)
class EditScoreResult:
    normalized_score: float
    levenshtein_distance: int
    gt_segment_count: int
    pred_segment_count: int

    @property
    def normalization_denominator(self) -> int:
        return max(self.gt_segment_count, self.pred_segment_count, 1)


def compute_edit_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    ignore_label: int | None = 0,
) -> EditScoreResult:
    """
    Normalized segment edit score in ``[0, 1]``.

    ``normalized_score = 1 - d / max(n_gt, n_pred, 1)`` where ``d`` is the
    Levenshtein distance between segment label sequences after collapsing
    consecutive duplicate frame labels and removing ignored labels.
    """
    gt_seg = labels_to_segments(y_true, ignore_label=ignore_label)
    pred_seg = labels_to_segments(y_pred, ignore_label=ignore_label)
    gt_labels = [segment.label for segment in gt_seg]
    pred_labels = [segment.label for segment in pred_seg]
    denominator = max(len(gt_labels), len(pred_labels), 1)
    distance = _levenshtein(gt_labels, pred_labels)
    normalized = 1.0 - distance / denominator
    return EditScoreResult(
        normalized_score=float(normalized),
        levenshtein_distance=distance,
        gt_segment_count=len(gt_labels),
        pred_segment_count=len(pred_labels),
    )


def edit_score(y_true: np.ndarray, y_pred: np.ndarray, ignore_label: int | None = 0) -> float:
    """Backward-compatible wrapper returning only the normalized edit score."""
    return compute_edit_score(y_true, y_pred, ignore_label=ignore_label).normalized_score


@dataclass(frozen=True)
class SegmentMatchCounts:
    tp: int
    fp: int
    fn: int

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) else 0.0

    @property
    def f1(self) -> float:
        if self.precision + self.recall == 0:
            return 0.0
        return 2 * self.precision * self.recall / (self.precision + self.recall)


def greedy_match_segments(
    gt_segments: list[Segment],
    pred_segments: list[Segment],
    iou_threshold: float,
) -> tuple[SegmentMatchCounts, dict[int, SegmentMatchCounts]]:
    """
    Greedy class-aware one-to-one segment matching.

    Predicted segments are processed in order. Each prediction matches the
    highest-IoU unmatched ground-truth segment of the same class if IoU >= threshold.
    """
    matched_gt: set[int] = set()
    tp = 0
    per_class: dict[int, SegmentMatchCounts] = {}

    def bump(class_id: int, field: str) -> None:
        counts = per_class.setdefault(class_id, SegmentMatchCounts(tp=0, fp=0, fn=0))
        per_class[class_id] = SegmentMatchCounts(
            tp=counts.tp + (1 if field == "tp" else 0),
            fp=counts.fp + (1 if field == "fp" else 0),
            fn=counts.fn + (1 if field == "fn" else 0),
        )

    for pred in pred_segments:
        best_iou = 0.0
        best_idx = -1
        for idx, gt in enumerate(gt_segments):
            if idx in matched_gt or gt.label != pred.label:
                continue
            iou = pred.iou(gt)
            if iou > best_iou:
                best_iou = iou
                best_idx = idx
        if best_idx >= 0 and best_iou >= iou_threshold:
            matched_gt.add(best_idx)
            tp += 1
            bump(pred.label, "tp")
        else:
            bump(pred.label, "fp")

    for idx, gt in enumerate(gt_segments):
        if idx not in matched_gt:
            bump(gt.label, "fn")

    fp = len(pred_segments) - tp
    fn = len(gt_segments) - tp
    return SegmentMatchCounts(tp=tp, fp=fp, fn=fn), per_class


def _match_segments(
    gt_segments: list[Segment],
    pred_segments: list[Segment],
    iou_threshold: float,
) -> tuple[int, int, int]:
    counts, _ = greedy_match_segments(gt_segments, pred_segments, iou_threshold)
    return counts.tp, counts.fp, counts.fn


def segmental_f1(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    iou_threshold: float,
    ignore_label: int | None = 0,
) -> float:
    """Segmental F1 at IoU threshold ``iou_threshold``."""
    gt_segments = labels_to_segments(y_true, ignore_label=ignore_label)
    pred_segments = labels_to_segments(y_pred, ignore_label=ignore_label)
    counts, _ = greedy_match_segments(gt_segments, pred_segments, iou_threshold)
    return counts.f1


@dataclass(frozen=True)
class SegmentMetricsResult:
    edit: EditScoreResult
    aggregate: dict[str, float]
    per_class: dict[int, dict[str, float]]


def compute_segment_metrics_detailed(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    iou_thresholds: Iterable[float] = (0.10, 0.25, 0.50),
    ignore_label: int | None = 0,
    class_ids: Iterable[int] | None = None,
) -> SegmentMetricsResult:
    """Compute edit score and segmental F1 with per-class breakdown."""
    gt_segments = labels_to_segments(y_true, ignore_label=ignore_label)
    pred_segments = labels_to_segments(y_pred, ignore_label=ignore_label)
    edit = compute_edit_score(y_true, y_pred, ignore_label=ignore_label)

    aggregate: dict[str, float] = {"edit_score": edit.normalized_score}
    per_class_out: dict[int, dict[str, float]] = {}

    observed_classes = class_ids or sorted(
        {segment.label for segment in gt_segments} | {segment.label for segment in pred_segments}
    )

    for threshold in iou_thresholds:
        counts, per_class = greedy_match_segments(gt_segments, pred_segments, threshold)
        key = f"segmental_f1_at_{int(threshold * 100)}"
        aggregate[key] = counts.f1
        aggregate[f"segmental_precision_at_{int(threshold * 100)}"] = counts.precision
        aggregate[f"segmental_recall_at_{int(threshold * 100)}"] = counts.recall
        for class_id in observed_classes:
            class_counts = per_class.get(class_id, SegmentMatchCounts(tp=0, fp=0, fn=0))
            per_class_out.setdefault(class_id, {})[key] = class_counts.f1

    return SegmentMetricsResult(edit=edit, aggregate=aggregate, per_class=per_class_out)


def compute_segment_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    iou_thresholds: Iterable[float] = (0.10, 0.25, 0.50),
    ignore_label: int | None = 0,
) -> dict[str, float]:
    """Compute edit score and segmental F1 at multiple IoU thresholds (legacy API)."""
    detailed = compute_segment_metrics_detailed(
        y_true,
        y_pred,
        iou_thresholds=iou_thresholds,
        ignore_label=ignore_label,
    )
    result = dict(detailed.aggregate)
    result["edit_levenshtein_distance"] = float(detailed.edit.levenshtein_distance)
    return result


def compute_segment_metrics_with_ontology(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    video_id: str,
    ontology: PhaseOntology,
    iou_thresholds: Iterable[float] = (0.10, 0.25, 0.50),
    ignore_labels: Iterable[int] | None = (0,),
) -> SegmentMetricsResult:
    """Validate labels against ontology before computing segment metrics."""
    ignore = next(iter(ignore_labels), 0) if ignore_labels is not None else None
    labels_to_canonical_segments(y_true, video_id=video_id, ontology=ontology, ignore_labels=ignore_labels)
    labels_to_canonical_segments(y_pred, video_id=video_id, ontology=ontology, ignore_labels=ignore_labels)
    return compute_segment_metrics_detailed(
        y_true,
        y_pred,
        iou_thresholds=iou_thresholds,
        ignore_label=ignore,
        class_ids=ontology.supervised_phase_ids,
    )
