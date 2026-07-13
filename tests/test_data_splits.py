"""Tests for athlete split helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from snatch_phase_bench.data.splits import AthleteSplit, load_athlete_split


def test_athlete_split_partition_for_athlete() -> None:
    split = AthleteSplit(
        train_athletes=frozenset(["a", "b"]),
        val_athletes=frozenset(["c"]),
        test_athletes=frozenset(["d"]),
    )
    assert split.partition_for_athlete("a") == "train"
    assert split.partition_for_athlete("c") == "val"
    assert split.partition_for_athlete("d") == "test"
    assert split.partition_for_athlete("unknown") == "unknown"


def test_athlete_split_filter_video_relpaths() -> None:
    split = AthleteSplit(
        train_athletes=frozenset(["alice"]),
        val_athletes=frozenset(["bob"]),
        test_athletes=frozenset(),
    )
    videos = ["alice/v1.mp4", "bob/v2.mp4", "alice/v3.mp4"]
    assert split.filter_video_relpaths(videos, split="train") == ("alice/v1.mp4", "alice/v3.mp4")
    assert split.filter_video_relpaths(videos, split="val") == ("bob/v2.mp4",)


def test_athlete_split_from_json(tmp_path: Path) -> None:
    payload = {
        "seed": 42,
        "train_athletes": ["x", "y"],
        "val_athletes": ["z"],
        "test_athletes": ["w"],
    }
    path = tmp_path / "split.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    split = load_athlete_split(path)
    assert split.seed == 42
    assert split.train_athletes == frozenset(["x", "y"])
    assert split.source_path == path.resolve()


def test_athlete_split_athletes_in_invalid_raises() -> None:
    split = AthleteSplit(
        train_athletes=frozenset(["a"]),
        val_athletes=frozenset(),
        test_athletes=frozenset(),
    )
    with pytest.raises(ValueError, match="Unsupported split"):
        split.athletes_in("unknown")


def test_athlete_split_no_overlap_between_partitions() -> None:
    split = AthleteSplit(
        train_athletes=frozenset(["a", "b"]),
        val_athletes=frozenset(["c"]),
        test_athletes=frozenset(["d", "e"]),
    )
    assert not (split.train_athletes & split.val_athletes)
    assert not (split.train_athletes & split.test_athletes)
    assert not (split.val_athletes & split.test_athletes)
