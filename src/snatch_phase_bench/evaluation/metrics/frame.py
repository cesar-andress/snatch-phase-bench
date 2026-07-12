"""Frame-level metrics via window prediction aggregation."""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

from snatch_phase_bench.evaluation.metrics.window import compute_window_metrics


Aggregation = Literal["center", "majority_vote"]


def aggregate_window_predictions(
    meta: pd.DataFrame,
    y_pred: np.ndarray,
    *,
    aggregation: Aggregation = "center",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Collapse window predictions to unique frames.

    ``center``: use label at each window's ``center_frame`` (last window wins on ties).
    ``majority_vote``: per (video, center_frame) majority vote across overlapping windows.
    """
    if len(meta) != len(y_pred):
        raise ValueError("meta and y_pred must have the same length.")

    df = meta.copy()
    df["y_pred"] = y_pred
    df["y_true"] = meta["phase_id"].to_numpy(dtype=np.int64)

    if aggregation == "center":
        dedup = df.drop_duplicates(subset=["video_relpath", "center_frame"], keep="last")
        return (
            dedup["y_true"].to_numpy(dtype=np.int64),
            dedup["y_pred"].to_numpy(dtype=np.int64),
        )

    grouped = df.groupby(["video_relpath", "center_frame"], sort=False)
    y_true_list: list[int] = []
    y_pred_list: list[int] = []
    for (_, _frame), group in grouped:
        y_true_list.append(int(group["y_true"].iloc[0]))
        values, counts = np.unique(group["y_pred"].to_numpy(), return_counts=True)
        y_pred_list.append(int(values[int(np.argmax(counts))]))
    return np.asarray(y_true_list, dtype=np.int64), np.asarray(y_pred_list, dtype=np.int64)


def compute_frame_metrics(
    meta: pd.DataFrame,
    y_pred: np.ndarray,
    *,
    aggregation: Aggregation = "majority_vote",
    target_names: list[str] | None = None,
) -> dict:
    """Compute frame-level metrics after aggregating overlapping windows."""
    y_true, y_pred_frame = aggregate_window_predictions(meta, y_pred, aggregation=aggregation)
    result = compute_window_metrics(y_true, y_pred_frame, target_names=target_names)
    result["aggregation"] = aggregation
    result["num_frames"] = int(len(y_true))
    return result
