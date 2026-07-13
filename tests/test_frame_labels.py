"""Tests for frame label store."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from snatch_phase_bench.data.labels import FrameLabelStore
from snatch_phase_bench.ontology.loader import load_ontology


@pytest.fixture
def labels_csv(tmp_path: Path) -> Path:
    df = pd.DataFrame(
        {
            "video_relpath": ["athlete_a/clip1.mp4"] * 3 + ["athlete_b/clip2.mp4"] * 2,
            "frame": [0, 1, 2, 0, 1],
            "phase_id": [1, 2, 3, 4, 5],
            "phase_name": ["setup", "first_pull", "transition", "second_pull", "turnover"],
        }
    )
    path = tmp_path / "labels.csv"
    df.to_csv(path, index=False)
    return path


def test_frame_label_store_lists_videos(labels_csv: Path) -> None:
    store = FrameLabelStore(labels_csv)
    assert store.video_relpaths == ("athlete_a/clip1.mp4", "athlete_b/clip2.mp4")


def test_frame_label_store_get_sequence(labels_csv: Path) -> None:
    store = FrameLabelStore(labels_csv)
    sequence = store.get("athlete_a/clip1.mp4")
    assert sequence.num_frames == 3
    assert sequence.phase_ids.tolist() == [1, 2, 3]


def test_supervised_mask_uses_ontology(labels_csv: Path) -> None:
    ontology = load_ontology()
    store = FrameLabelStore(labels_csv, ontology=ontology)
    sequence = store.get("athlete_a/clip1.mp4")
    assert sequence.supervised_mask(ontology).tolist() == [True, True, True]
