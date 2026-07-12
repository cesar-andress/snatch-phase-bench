"""Window-level classification metrics (frozen baseline protocol)."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score


def compute_window_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    target_names: list[str] | None = None,
) -> dict[str, Any]:
    """
    Compute window-level metrics identical to the frozen baseline evaluation.

    Uses ``sklearn.metrics.classification_report`` with ``digits=10``.
    """
    if len(y_true) != len(y_pred):
        raise ValueError(f"y_true and y_pred length mismatch: {len(y_true)} vs {len(y_pred)}")

    report = classification_report(
        y_true,
        y_pred,
        target_names=target_names,
        digits=10,
        zero_division=0,
        output_dict=True,
    )
    matrix = confusion_matrix(y_true, y_pred)
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "weighted_f1": float(f1_score(y_true, y_pred, average="weighted")),
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
        "confusion_matrix_shape": list(matrix.shape),
        "num_samples": int(len(y_true)),
    }
