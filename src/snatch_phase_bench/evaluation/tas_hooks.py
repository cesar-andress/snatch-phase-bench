"""Evaluation hooks connecting TAS predictions to canonical benchmark metrics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.evaluation.evaluate import evaluate_dataset_videos
from snatch_phase_bench.evaluation.metric_config import EvaluationConfig
from snatch_phase_bench.evaluation.results import BenchmarkEvaluationResult, write_evaluation_result
from snatch_phase_bench.ontology.phase_ontology import LabelMapping


def build_video_evaluation_payload(
    record: FrameSequenceRecord,
    y_pred: np.ndarray,
    *,
    fps: float | None = None,
    fps_source: str | None = None,
) -> dict[str, Any]:
    """Format one video for ``evaluate_dataset_videos``."""
    gt = np.asarray(record.phase_ids, dtype=np.int64)
    pred = np.asarray(y_pred, dtype=np.int64)
    if len(gt) != len(pred):
        raise ValueError(
            f"Prediction length mismatch for {record.video_relpath}: "
            f"gt={len(gt)} pred={len(pred)}"
        )
    return {
        "y_true": gt,
        "y_pred": pred,
        "fps": fps,
        "fps_source": fps_source,
        "athlete_id": record.athlete_id,
    }


def build_dataset_evaluation_payload(
    records: list[FrameSequenceRecord],
    predictions: dict[str, np.ndarray],
    *,
    fps_by_video: dict[str, float] | None = None,
    fps_source: str | None = None,
) -> dict[str, dict[str, Any]]:
    """Build the ``videos`` argument for ``evaluate_dataset_videos``."""
    payload: dict[str, dict[str, Any]] = {}
    for record in records:
        if record.video_relpath not in predictions:
            raise KeyError(f"Missing predictions for {record.video_relpath}")
        fps = fps_by_video.get(record.video_relpath) if fps_by_video else None
        payload[record.video_relpath] = build_video_evaluation_payload(
            record,
            predictions[record.video_relpath],
            fps=fps,
            fps_source=fps_source,
        )
    return payload


def evaluate_frame_predictions(
    records: list[FrameSequenceRecord],
    predictions: dict[str, np.ndarray],
    *,
    model_identifier: str,
    config: EvaluationConfig | None = None,
    label_mapping: LabelMapping | None = None,
    use_b0_mapping: bool = False,
    fps_by_video: dict[str, float] | None = None,
    fps_source: str | None = None,
) -> BenchmarkEvaluationResult:
    """
    Evaluate per-frame predictions using canonical segment/boundary metrics.

    Primary entry point for B2 learned segmenters once inference is available.
    """
    videos = build_dataset_evaluation_payload(
        records,
        predictions,
        fps_by_video=fps_by_video,
        fps_source=fps_source,
    )
    return evaluate_dataset_videos(
        videos,
        model_identifier=model_identifier,
        config=config,
        label_mapping=label_mapping,
        use_b0_mapping=use_b0_mapping,
    )


def evaluate_and_write(
    records: list[FrameSequenceRecord],
    predictions: dict[str, np.ndarray],
    output_path: str | Path,
    *,
    model_identifier: str,
    config: EvaluationConfig | None = None,
    label_mapping: LabelMapping | None = None,
    use_b0_mapping: bool = False,
) -> BenchmarkEvaluationResult:
    """Evaluate predictions and persist JSON to ``output_path``."""
    result = evaluate_frame_predictions(
        records,
        predictions,
        model_identifier=model_identifier,
        config=config,
        label_mapping=label_mapping,
        use_b0_mapping=use_b0_mapping,
    )
    write_evaluation_result(Path(output_path), result)
    return result
