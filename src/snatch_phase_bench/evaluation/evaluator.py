"""High-level evaluation orchestrator (extensible, does not replace frozen baseline eval)."""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
import pandas as pd

from snatch_phase_bench.evaluation.metrics import (
    compute_frame_metrics,
    compute_segment_metrics,
    compute_window_metrics,
)

EvaluationLevel = Literal["window", "frame", "segment"]


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    meta: pd.DataFrame | None = None,
    *,
    levels: tuple[EvaluationLevel, ...] = ("window",),
    target_names: list[str] | None = None,
    frame_aggregation: Literal["center", "majority_vote"] = "majority_vote",
) -> dict[str, Any]:
    """
    Run selected evaluation levels on aligned predictions.

    Window-level metrics match the frozen baseline protocol when ``levels`` includes ``window``.
    """
    results: dict[str, Any] = {}
    if "window" in levels:
        results["window"] = compute_window_metrics(y_true, y_pred, target_names=target_names)
    if "frame" in levels:
        if meta is None:
            raise ValueError("meta DataFrame required for frame-level evaluation.")
        results["frame"] = compute_frame_metrics(
            meta, y_pred, aggregation=frame_aggregation, target_names=target_names
        )
    if "segment" in levels:
        if meta is None:
            raise ValueError("meta DataFrame required for segment-level evaluation.")
        from snatch_phase_bench.evaluation.metrics.frame import aggregate_window_predictions

        per_video: dict[str, dict[str, float]] = {}
        for video, group in meta.groupby("video_relpath", sort=False):
            indices = group.index.to_numpy()
            gt_windows = group["phase_id"].to_numpy(dtype=np.int64)
            pred_windows = y_pred[indices]
            sub_meta = group.reset_index(drop=True)
            y_true_frame, y_pred_frame = aggregate_window_predictions(
                sub_meta, pred_windows, aggregation=frame_aggregation
            )
            per_video[str(video)] = compute_segment_metrics(y_true_frame, y_pred_frame)
        # macro-average segment metrics across videos
        if per_video:
            keys = next(iter(per_video.values())).keys()
            results["segment"] = {
                key: float(np.mean([video_metrics[key] for video_metrics in per_video.values()]))
                for key in keys
            }
            results["segment_per_video"] = per_video
    return results
