"""Tests for TAS evaluation hooks."""

from __future__ import annotations

import numpy as np

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.evaluation.tas_hooks import (
    build_dataset_evaluation_payload,
    evaluate_frame_predictions,
)


def _record(video: str, labels: list[int]) -> FrameSequenceRecord:
    frames = np.arange(len(labels), dtype=np.int64)
    features = np.zeros((len(labels), 99), dtype=np.float32)
    return FrameSequenceRecord(
        video_relpath=video,
        athlete_id=video.split("/", 1)[0],
        frames=frames,
        features=features,
        phase_ids=np.asarray(labels, dtype=np.int64),
        split="test",
    )


def test_build_dataset_evaluation_payload() -> None:
    records = [_record("athlete_a/clip1.mp4", [1, 2, 3])]
    predictions = {"athlete_a/clip1.mp4": np.array([1, 2, 2], dtype=np.int64)}
    payload = build_dataset_evaluation_payload(records, predictions)
    assert payload["athlete_a/clip1.mp4"]["y_true"].tolist() == [1, 2, 3]
    assert payload["athlete_a/clip1.mp4"]["y_pred"].tolist() == [1, 2, 2]


def test_evaluate_frame_predictions_runs_canonical_metrics() -> None:
    records = [
        _record("athlete_a/clip1.mp4", [1, 2, 3, 4]),
        _record("athlete_b/clip2.mp4", [2, 3, 4, 5]),
    ]
    predictions = {
        "athlete_a/clip1.mp4": np.array([1, 2, 3, 4], dtype=np.int64),
        "athlete_b/clip2.mp4": np.array([2, 3, 4, 5], dtype=np.int64),
    }
    result = evaluate_frame_predictions(
        records,
        predictions,
        model_identifier="ms_tcn_stub_test",
    )
    assert result.model_identifier == "ms_tcn_stub_test"
    assert len(result.per_video) == 2
    assert "segment_macro_over_videos" in result.aggregate
