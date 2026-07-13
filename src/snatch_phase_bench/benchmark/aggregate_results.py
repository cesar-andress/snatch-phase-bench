"""Aggregate multi-seed MS-TCN benchmark results."""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any

import numpy as np
from sklearn.metrics import confusion_matrix, f1_score


PRIMARY_METRICS = [
    "frame_macro_f1",
    "segmental_f1_at_50",
    "edit_score",
    "boundary_mae_frames",
    "boundary_f1",
]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _aggregate_stats(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "std": None, "median": None, "min": None, "max": None, "n": 0}
    if len(values) == 1:
        return {
            "mean": values[0],
            "std": 0.0,
            "median": values[0],
            "min": values[0],
            "max": values[0],
            "n": 1,
        }
    return {
        "mean": float(mean(values)),
        "std": float(pstdev(values)),
        "median": float(median(values)),
        "min": float(min(values)),
        "max": float(max(values)),
        "n": len(values),
    }


def extract_seed_metrics(eval_payload: dict[str, Any]) -> dict[str, float | None]:
    aggregate = eval_payload.get("aggregate", {})
    segment = aggregate.get("segment_macro_over_videos", {})
    boundary_micro = aggregate.get("boundary_mae_frames_micro_over_videos")

    boundary_f1_values: list[float] = []
    for _key, payload in eval_payload.get("per_transition", {}).items():
        matched = payload.get("num_matched", 0)
        missed = payload.get("num_missed", 0)
        extra = payload.get("num_extra", 0)
        denom_p = matched + extra
        denom_r = matched + missed
        if denom_p > 0 and denom_r > 0:
            precision = matched / denom_p
            recall = matched / denom_r
            if precision + recall > 0:
                boundary_f1_values.append(2 * precision * recall / (precision + recall))
    boundary_f1 = float(mean(boundary_f1_values)) if boundary_f1_values else None

    metrics = {
        "frame_macro_f1": eval_payload.get("frame_macro_f1"),
        "segmental_f1_at_50": segment.get("segmental_f1_at_50"),
        "segmental_f1_at_25": segment.get("segmental_f1_at_25"),
        "segmental_f1_at_10": segment.get("segmental_f1_at_10"),
        "edit_score": segment.get("edit_score"),
        "boundary_mae_frames": boundary_micro,
        "boundary_f1": boundary_f1,
    }
    return metrics


def compute_frame_macro_f1_from_predictions(
    predictions_path: Path,
    *,
    ignore_label_id: int = 0,
) -> float:
    payload = _load_json(predictions_path)
    y_true_all: list[int] = []
    y_pred_all: list[int] = []
    for video in payload["videos"]:
        gt = np.asarray(video["y_true"], dtype=np.int64)
        pred = np.asarray(video["y_pred"], dtype=np.int64)
        mask = gt != ignore_label_id
        y_true_all.extend(gt[mask].tolist())
        y_pred_all.extend(pred[mask].tolist())
    if not y_true_all:
        return 0.0
    return float(
        f1_score(y_true_all, y_pred_all, average="macro", zero_division=0)
    )


def compute_confusion_matrix_from_predictions(
    predictions_path: Path,
    *,
    num_classes: int = 8,
    ignore_label_id: int = 0,
) -> dict[str, Any]:
    payload = _load_json(predictions_path)
    y_true_all: list[int] = []
    y_pred_all: list[int] = []
    for video in payload["videos"]:
        gt = np.asarray(video["y_true"], dtype=np.int64)
        pred = np.asarray(video["y_pred"], dtype=np.int64)
        mask = gt != ignore_label_id
        y_true_all.extend(gt[mask].tolist())
        y_pred_all.extend(pred[mask].tolist())
    if not y_true_all:
        return {"matrix": [], "labels": list(range(num_classes))}
    labels = [idx for idx in range(num_classes) if idx != ignore_label_id]
    matrix = confusion_matrix(y_true_all, y_pred_all, labels=labels).tolist()
    return {"matrix": matrix, "labels": labels}


def per_class_recall_from_predictions(
    predictions_path: Path,
    *,
    ignore_label_id: int = 0,
) -> dict[str, float]:
    payload = _load_json(predictions_path)
    y_true_all: list[int] = []
    y_pred_all: list[int] = []
    for video in payload["videos"]:
        gt = np.asarray(video["y_true"], dtype=np.int64)
        pred = np.asarray(video["y_pred"], dtype=np.int64)
        mask = gt != ignore_label_id
        y_true_all.extend(gt[mask].tolist())
        y_pred_all.extend(pred[mask].tolist())
    if not y_true_all:
        return {}
    labels = sorted(set(y_true_all))
    recalls: dict[str, float] = {}
    for label in labels:
        if label == ignore_label_id:
            continue
        tp = sum(1 for t, p in zip(y_true_all, y_pred_all) if t == label and p == label)
        fn = sum(1 for t, p in zip(y_true_all, y_pred_all) if t == label and p != label)
        recalls[str(label)] = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    return recalls


def aggregate_seed_results(
    seed_dirs: dict[int, Path],
    *,
    split: str = "test",
) -> dict[str, Any]:
    per_seed: dict[str, Any] = {}
    metric_series: dict[str, list[float]] = {key: [] for key in PRIMARY_METRICS}

    for seed, seed_dir in sorted(seed_dirs.items()):
        eval_path = seed_dir / f"eval_{split}.json"
        predictions_path = seed_dir / f"predictions_{split}.json"
        train_summary_path = seed_dir / "train_summary.json"
        early_stop_path = seed_dir / "early_stopping.json"

        if not eval_path.exists():
            raise FileNotFoundError(f"Missing evaluation JSON for seed {seed}: {eval_path}")

        eval_payload = _load_json(eval_path)
        if predictions_path.exists() and eval_payload.get("frame_macro_f1") is None:
            eval_payload["frame_macro_f1"] = compute_frame_macro_f1_from_predictions(predictions_path)

        seed_metrics = extract_seed_metrics(eval_payload)
        per_seed[str(seed)] = {
            "metrics": seed_metrics,
            "eval_path": str(eval_path),
            "train_summary": _load_json(train_summary_path) if train_summary_path.exists() else None,
            "early_stopping": _load_json(early_stop_path) if early_stop_path.exists() else None,
        }
        for key in PRIMARY_METRICS:
            value = seed_metrics.get(key)
            if value is not None and not (isinstance(value, float) and math.isnan(value)):
                metric_series[key].append(float(value))

    aggregate = {key: _aggregate_stats(metric_series[key]) for key in PRIMARY_METRICS}
    return {
        "split": split,
        "seeds": sorted(seed_dirs.keys()),
        "per_seed": per_seed,
        "aggregate": aggregate,
        "metric_series": metric_series,
    }
