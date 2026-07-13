"""Extended tests for frame sequence and label data layer."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from snatch_phase_bench.data.frame_sequence import (
    iter_frame_sequences,
    load_frame_sequences,
    summarize_frame_sequences,
)
from snatch_phase_bench.data.labels import FrameLabelStore
from snatch_phase_bench.data.splits import AthleteSplit


def test_frame_label_store_len_and_get(synthetic_ms_tcn_dataset: tuple[Path, Path, AthleteSplit]) -> None:
    labels_csv, _, _ = synthetic_ms_tcn_dataset
    store = FrameLabelStore(labels_csv)
    assert len(store.video_relpaths) == 4
    seq = store.get("athlete_a/clip0.mp4")
    assert seq.num_frames == 10


def test_frame_label_store_missing_video_raises(synthetic_ms_tcn_dataset: tuple[Path, Path, AthleteSplit]) -> None:
    labels_csv, _, _ = synthetic_ms_tcn_dataset
    store = FrameLabelStore(labels_csv)
    with pytest.raises(KeyError):
        store.get("missing/video.mp4")


def test_iter_frame_sequences_respects_split_filter(
    synthetic_ms_tcn_dataset: tuple[Path, Path, AthleteSplit],
) -> None:
    labels_csv, keypoints_dir, split = synthetic_ms_tcn_dataset
    train = list(
        iter_frame_sequences(
            labels_csv=labels_csv,
            keypoints_dir=keypoints_dir,
            athlete_split=split,
            split_filter="train",
        )
    )
    assert len(train) == 2
    assert all(record.athlete_id == "athlete_a" for record in train)


def test_load_frame_sequences_all_videos(
    synthetic_ms_tcn_dataset: tuple[Path, Path, AthleteSplit],
) -> None:
    labels_csv, keypoints_dir, _ = synthetic_ms_tcn_dataset
    records = load_frame_sequences(labels_csv=labels_csv, keypoints_dir=keypoints_dir)
    summary = summarize_frame_sequences(records)
    assert summary["videos"] == 4
    assert summary["frames"] == 40
    assert summary["feature_dim"] == 99


def test_frame_sequence_aligned_lengths(
    synthetic_train_val_records: tuple[list, list],
) -> None:
    train, _ = synthetic_train_val_records
    for record in train:
        assert record.num_frames == len(record.frames)
        assert record.features.shape[0] == record.num_frames
        assert len(record.phase_ids) == record.num_frames


def test_frame_sequence_features_no_nan(
    synthetic_train_val_records: tuple[list, list],
) -> None:
    train, _ = synthetic_train_val_records
    for record in train:
        assert not np.isnan(record.features).any()
