"""Tests for evaluation metrics."""

from __future__ import annotations

import numpy as np

from snatch_phase_bench.evaluation.metrics import (
    compute_segment_metrics,
    compute_window_metrics,
    edit_score,
    segmental_f1,
)


def test_window_metrics_perfect() -> None:
    y = np.array([0, 1, 2, 1, 0])
    result = compute_window_metrics(y, y)
    assert result["accuracy"] == 1.0
    assert result["macro_f1"] == 1.0


def test_edit_score_identical() -> None:
    labels = np.array([1, 1, 2, 2, 3, 3])
    assert edit_score(labels, labels) == 1.0


def test_segmental_f1_perfect() -> None:
    labels = np.array([1, 1, 2, 2, 3, 3])
    assert segmental_f1(labels, labels, iou_threshold=0.5) == 1.0


def test_compute_segment_metrics_keys() -> None:
    labels = np.array([1, 1, 2, 2, 3, 3, 3])
    metrics = compute_segment_metrics(labels, labels)
    assert "edit_score" in metrics
    assert "segmental_f1_at_50" in metrics
