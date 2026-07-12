"""Tests for athlete-level split validation."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from snatch_phase_bench.config import load_config, resolve_path
from snatch_phase_bench.reproduction.split_validation import load_split, validate_split


@pytest.fixture(scope="module")
def config() -> dict:
    return load_config()


def test_split_has_no_athlete_overlap(config: dict) -> None:
    meta = pd.read_csv(resolve_path(config, "baseline_meta_csv"))
    split = load_split(resolve_path(config, "athlete_split_json"))
    report = validate_split(meta, split, expected=config["expected"])
    assert report.athlete_overlap == []
    assert report.video_overlap == []


def test_split_expected_counts(config: dict) -> None:
    meta = pd.read_csv(resolve_path(config, "baseline_meta_csv"))
    split = load_split(resolve_path(config, "athlete_split_json"))
    report = validate_split(meta, split, keypoints_dir=resolve_path(config, "keypoints_dir"))
    assert report.passed
    assert report.train_athletes == 49
    assert report.val_athletes == 10
    assert report.test_athletes == 11
    assert report.test_windows == 3877
