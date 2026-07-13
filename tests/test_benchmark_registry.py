"""Tests for benchmark model registry."""

from __future__ import annotations

from snatch_phase_bench.benchmark.registry import load_benchmark_registry, load_model_experiment_config


def test_benchmark_registry_includes_b0_and_ms_tcn() -> None:
    registry = load_benchmark_registry()
    b0 = registry.get("B0")
    ms_tcn = registry.get("ms_tcn")

    assert b0.status == "frozen_exploratory_reference"
    assert b0.role == "exploratory_only"
    assert ms_tcn.status == "infrastructure_ready"
    assert ms_tcn.registry_name == "ms_tcn"
    assert ms_tcn.input_layout == "frame_sequence"


def test_primary_comparators_are_b2_learned_models() -> None:
    registry = load_benchmark_registry()
    primary = registry.primary_comparators()
    assert primary
    assert all(spec.tier_id == "B2" for spec in primary)
    assert "ms_tcn" in {spec.model_id for spec in primary}


def test_ms_tcn_config_stub_loads() -> None:
    registry = load_benchmark_registry()
    ms_tcn = registry.get("ms_tcn")
    assert ms_tcn.config_path is not None
    config = load_model_experiment_config(ms_tcn.config_path)
    assert config["model"]["name"] == "ms_tcn"
    assert config["dataset"]["adapter"] == "frame_sequence"
    assert config["expected"]["implementation_status"] == "not_implemented"
