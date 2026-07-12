"""Evaluation metrics and orchestration."""

from snatch_phase_bench.evaluation.evaluator import EvaluationResult, evaluate_predictions
from snatch_phase_bench.evaluation.metrics import (
    aggregate_window_predictions,
    compute_frame_metrics,
    compute_segment_metrics,
    compute_window_metrics,
    edit_score,
    segmental_f1,
)

__all__ = [
    "EvaluationResult",
    "aggregate_window_predictions",
    "compute_frame_metrics",
    "compute_segment_metrics",
    "compute_window_metrics",
    "edit_score",
    "evaluate_predictions",
    "segmental_f1",
]
