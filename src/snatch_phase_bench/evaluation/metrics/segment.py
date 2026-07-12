"""Segment-level temporal segmentation metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class Segment:
    """Half-open interval ``[start, end)`` with class label."""

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


def labels_to_segments(labels: np.ndarray, ignore_label: int | None = 0) -> list[Segment]:
    """Convert per-frame label sequence to contiguous segments."""
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


def edit_score(y_true: np.ndarray, y_pred: np.ndarray, ignore_label: int | None = 0) -> float:
    """
    Segment edit score: ``1 - d / max(n, m)`` where ``d`` is Levenshtein distance
    between GT and predicted segment label sequences.
    """
    gt_seg = labels_to_segments(y_true, ignore_label=ignore_label)
    pred_seg = labels_to_segments(y_pred, ignore_label=ignore_label)
    gt_labels = [segment.label for segment in gt_seg]
    pred_labels = [segment.label for segment in pred_seg]
    n = max(len(gt_labels), len(pred_labels), 1)
    distance = _levenshtein(gt_labels, pred_labels)
    return 1.0 - distance / n


def _match_segments(
    gt_segments: list[Segment],
    pred_segments: list[Segment],
    iou_threshold: float,
) -> tuple[int, int, int]:
    """Greedy IoU matching; returns tp, fp, fn."""
    matched_gt: set[int] = set()
    tp = 0
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
    fp = len(pred_segments) - tp
    fn = len(gt_segments) - tp
    return tp, fp, fn


def segmental_f1(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    iou_threshold: float,
    ignore_label: int | None = 0,
) -> float:
    """Segmental F1 at IoU threshold ``iou_threshold``."""
    gt_segments = labels_to_segments(y_true, ignore_label=ignore_label)
    pred_segments = labels_to_segments(y_pred, ignore_label=ignore_label)
    tp, fp, fn = _match_segments(gt_segments, pred_segments, iou_threshold)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def compute_segment_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    iou_thresholds: Iterable[float] = (0.10, 0.25, 0.50),
    ignore_label: int | None = 0,
) -> dict[str, float]:
    """Compute edit score and segmental F1 at multiple IoU thresholds."""
    result = {"edit_score": float(edit_score(y_true, y_pred, ignore_label=ignore_label))}
    for threshold in iou_thresholds:
        key = f"segmental_f1_at_{int(threshold * 100)}"
        result[key] = float(segmental_f1(y_true, y_pred, threshold, ignore_label=ignore_label))
    return result
