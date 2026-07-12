"""Tests for SnatchPhaseBench."""

from __future__ import annotations

from snatch_phase_bench.utils import resolve_project_root


def test_resolve_project_root() -> None:
    root = resolve_project_root()
    assert (root / "pyproject.toml").exists()
    assert (root / "src" / "snatch_phase_bench").is_dir()
