"""Preflight integrity checks for MS-TCN benchmark."""

from __future__ import annotations

from pathlib import Path

import pytest

from snatch_phase_bench.benchmark.preflight import run_preflight


@pytest.fixture(scope="module")
def preflight_report():
    return run_preflight()


@pytest.mark.integration
def test_preflight_passes(preflight_report):
    failed = [check.name for check in preflight_report.checks if not check.passed]
    assert preflight_report.passed, f"Preflight failed: {failed}"


@pytest.mark.integration
def test_preflight_video_count(preflight_report):
    assert preflight_report.summary["total_records"] == 208


@pytest.mark.integration
def test_preflight_split_counts(preflight_report):
    by_split = preflight_report.summary["by_split"]
    assert by_split["train"]["videos"] == 145
    assert by_split["val"]["videos"] == 30
    assert by_split["test"]["videos"] == 33
