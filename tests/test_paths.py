"""Tests for path helpers."""

from __future__ import annotations

from snatch_phase_bench.config import load_config
from snatch_phase_bench.data.paths import get_processed_dir, get_snapshot_root, get_split_json


def test_snapshot_root_exists() -> None:
    root = get_snapshot_root()
    assert root.exists()
    assert (root / "data" / "annotations").is_dir()


def test_split_json_exists() -> None:
    path = get_split_json()
    assert path.exists()


def test_processed_dir_under_project() -> None:
    path = get_processed_dir()
    assert "processed" in str(path)
