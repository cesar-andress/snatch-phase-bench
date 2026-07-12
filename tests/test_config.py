"""Tests for experiment configuration loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from snatch_phase_bench.experiments.config_loader import get_section, load_experiment_config


def test_load_baseline_experiment_config() -> None:
    config = load_experiment_config()
    assert config["experiment"]["name"] == "baseline_lstm_thesis"
    assert config["model"]["name"] == "lstm_baseline"
    assert config["dataset"]["window_size"] == 31
    assert "reproduction" in config


def test_get_section() -> None:
    config = {"training": {"batch_size": 64}}
    assert get_section(config, "training")["batch_size"] == 64
    assert get_section(config, "missing") == {}


def test_missing_experiment_file_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_experiment_config(Path("/nonexistent/baseline.yaml"), merge_reproduction=False)
