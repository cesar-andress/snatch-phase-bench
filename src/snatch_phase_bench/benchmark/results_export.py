"""Export dense predictions and auxiliary evaluation artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from snatch_phase_bench.benchmark.aggregate_results import (
    compute_confusion_matrix_from_predictions,
    compute_frame_macro_f1_from_predictions,
    per_class_recall_from_predictions,
)
from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.evaluation.results import BenchmarkEvaluationResult


def export_predictions_json(
    records: list[FrameSequenceRecord],
    predictions: dict[str, np.ndarray],
    path: Path,
) -> None:
    videos = []
    for record in records:
        pred = predictions[record.video_relpath]
        videos.append(
            {
                "video_relpath": record.video_relpath,
                "athlete_id": record.athlete_id,
                "frames": record.frames.tolist(),
                "y_true": record.phase_ids.tolist(),
                "y_pred": pred.astype(int).tolist(),
                "num_frames": record.num_frames,
            }
        )
    payload = {"videos": videos, "num_videos": len(videos)}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def enrich_eval_result_with_frame_metrics(
    result: BenchmarkEvaluationResult,
    predictions_path: Path,
    *,
    ignore_label_id: int = 0,
) -> dict[str, Any]:
    payload = result.to_dict()
    payload["frame_macro_f1"] = compute_frame_macro_f1_from_predictions(
        predictions_path,
        ignore_label_id=ignore_label_id,
    )
    payload["confusion_matrix"] = compute_confusion_matrix_from_predictions(
        predictions_path,
        ignore_label_id=ignore_label_id,
    )
    payload["per_class_recall"] = per_class_recall_from_predictions(
        predictions_path,
        ignore_label_id=ignore_label_id,
    )
    return payload
