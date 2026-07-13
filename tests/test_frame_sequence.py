"""Tests for dense frame sequence builder."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from snatch_phase_bench.data.frame_sequence import build_frame_sequence, summarize_frame_sequences
from snatch_phase_bench.data.splits import AthleteSplit


@pytest.fixture
def synthetic_dataset(tmp_path: Path) -> tuple[Path, Path]:
    labels = pd.DataFrame(
        {
            "video_relpath": ["athlete_a/clip1.mp4"] * 4,
            "frame": [0, 1, 2, 3],
            "phase_id": [1, 2, 3, 4],
            "phase_name": ["setup", "first_pull", "transition", "second_pull"],
        }
    )
    labels_csv = tmp_path / "labels.csv"
    labels.to_csv(labels_csv, index=False)

    keypoints_dir = tmp_path / "keypoints" / "athlete_a"
    keypoints_dir.mkdir(parents=True)
    rows = {"frame": [0, 1, 2, 3]}
    for i in range(33):
        rows[f"x{i}"] = [0.1 * i] * 4
        rows[f"y{i}"] = [0.2 * i] * 4
        rows[f"z{i}"] = [0.3 * i] * 4
    pd.DataFrame(rows).to_csv(keypoints_dir / "clip1.csv", index=False)
    return labels_csv, tmp_path / "keypoints"


def test_build_frame_sequence_aligns_features_and_labels(
    synthetic_dataset: tuple[Path, Path],
) -> None:
    labels_csv, keypoints_dir = synthetic_dataset
    record = build_frame_sequence(
        "athlete_a/clip1.mp4",
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
    )
    assert record.num_frames == 4
    assert record.feature_dim == 99
    assert record.phase_ids.tolist() == [1, 2, 3, 4]
    assert record.features.shape == (4, 99)
    assert not np.isnan(record.features).any()


def test_build_frame_sequence_assigns_split(
    synthetic_dataset: tuple[Path, Path],
) -> None:
    labels_csv, keypoints_dir = synthetic_dataset
    split = AthleteSplit(
        train_athletes=frozenset(["athlete_a"]),
        val_athletes=frozenset(),
        test_athletes=frozenset(),
    )
    record = build_frame_sequence(
        "athlete_a/clip1.mp4",
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
        athlete_split=split,
    )
    assert record.split == "train"


def test_summarize_frame_sequences(synthetic_dataset: tuple[Path, Path]) -> None:
    labels_csv, keypoints_dir = synthetic_dataset
    record = build_frame_sequence(
        "athlete_a/clip1.mp4",
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
    )
    summary = summarize_frame_sequences([record])
    assert summary["videos"] == 1
    assert summary["frames"] == 4
    assert summary["feature_dim"] == 99
