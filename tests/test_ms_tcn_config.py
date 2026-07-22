"""Tests for MS-TCN benchmark configuration."""

from __future__ import annotations

from pathlib import Path

import pytest

from snatch_phase_bench.benchmark.registry import load_benchmark_registry, load_model_experiment_config


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MS_TCN_CONFIG = PROJECT_ROOT / "configs" / "benchmark" / "ms_tcn.yaml"


def test_ms_tcn_yaml_exists() -> None:
    assert MS_TCN_CONFIG.exists()


def test_ms_tcn_config_loads() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    assert config["experiment"]["registry_name"] == "ms_tcn"


def test_ms_tcn_paper_architecture_defaults() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    model = config["model"]
    assert model["num_stages"] == 4
    assert model["num_layers"] == 10
    assert model["num_f_maps"] == 64
    assert model["kernel_size"] == 3


def test_ms_tcn_paper_optimizer_defaults() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    assert config["optimizer"]["name"] == "adam"
    assert config["optimizer"]["learning_rate"] == 0.0005
    assert config["optimizer"]["weight_decay"] == 0.0


def test_ms_tcn_paper_loss_defaults() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    assert config["loss"]["tmse_weight"] == 0.15
    assert config["loss"]["tmse_truncate_tau"] == 4


def test_ms_tcn_training_protocol() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    training = config["training"]
    assert training["batch_size"] == 1
    assert training["epochs"] == 50
    assert training["trainer"] == "ms_tcn_trainer"
    assert training["early_stopping"]["monitor"] == "val_segmental_f1_at_50"


def test_ms_tcn_dataset_adapter() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    assert config["dataset"]["adapter"] == "frame_sequence"
    assert config["dataset"]["features_per_frame"] == 99


def test_ms_tcn_ontology_settings() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    assert config["ontology"]["id"] == "seven_phase_v1"
    assert config["ontology"]["ignore_label_id"] == 0
    assert config["evaluation"]["use_b0_mapping"] is False


def test_ms_tcn_registry_implemented() -> None:
    registry = load_benchmark_registry()
    spec = registry.get("ms_tcn")
    assert spec.status == "verified"
    assert spec.registry_name == "ms_tcn"
    assert spec.config_path == MS_TCN_CONFIG.resolve()


def test_ms_tcn_seeds_in_manifest() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    assert config["experiment"]["seeds"] == [42, 123, 456]


def test_ms_tcn_scheduler_none() -> None:
    config = load_model_experiment_config(MS_TCN_CONFIG)
    assert config["scheduler"]["name"] == "none"
