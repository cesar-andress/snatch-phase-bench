"""Tests for artifact inspection."""

from __future__ import annotations

from pathlib import Path

import pytest

from snatch_phase_bench.config import load_config, resolve_path
from snatch_phase_bench.reproduction.artifact_inventory import inspect_artifact, is_lfs_pointer


def test_baseline_X_is_lfs_pointer() -> None:
    config = load_config()
    path = resolve_path(config, "baseline_X_npy")
    assert path.exists()
    assert is_lfs_pointer(path)
    status = inspect_artifact(path)
    assert status.status == "git_lfs_pointer"


def test_baseline_meta_is_real_csv() -> None:
    config = load_config()
    path = resolve_path(config, "baseline_meta_csv")
    assert path.exists()
    assert not is_lfs_pointer(path)
    status = inspect_artifact(path)
    assert status.status == "real_binary"
