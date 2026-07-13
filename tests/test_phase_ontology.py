"""Tests for phase ontology and label mapping (EXP-ONT)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from snatch_phase_bench.ontology import (
    load_benchmark_manifest,
    load_label_mapping,
    load_ontology,
)

ONTOLOGY_DIR = Path(__file__).resolve().parents[1] / "configs" / "ontology"


def test_seven_phase_ontology_matches_dataset() -> None:
    ontology = load_ontology(ONTOLOGY_DIR / "seven_phase_v1.yaml")
    assert ontology.ontology_id == "seven_phase_v1"
    assert ontology.num_supervised_phases == 7
    assert ontology.name_to_id["setup"] == 1
    assert ontology.name_to_id["recovery"] == 7
    assert len(ontology.transitions) == 6


def test_seven_phase_priority_transition() -> None:
    ontology = load_ontology(ONTOLOGY_DIR / "seven_phase_v1.yaml")
    priority = ontology.priority_transitions()
    assert len(priority) == 1
    assert priority[0].from_phase == "second_pull"
    assert priority[0].to_phase == "turnover"


def test_five_phase_ontology_for_b0() -> None:
    ontology = load_ontology(ONTOLOGY_DIR / "five_phase_knee_angle_v1.yaml")
    assert ontology.num_supervised_phases == 6
    assert "catch" not in ontology.name_to_id
    assert len(ontology.transitions) == 5


def test_seven_to_five_mapping_preserves_non_catch() -> None:
    mapping = load_label_mapping(ONTOLOGY_DIR / "seven_to_five_knee_angle_v1.yaml")
    assert mapping.map_label(2) == 2  # first_pull
    assert mapping.map_label(5) == 5  # turnover
    assert mapping.map_label(7) == 6  # recovery


def test_seven_to_five_mapping_merges_catch_into_turnover() -> None:
    mapping = load_label_mapping(ONTOLOGY_DIR / "seven_to_five_knee_angle_v1.yaml")
    assert mapping.map_label(6) == 5
    assert mapping.merge_rules
    table = dict(mapping.mapping_table())
    assert table["catch"] == "turnover"
    assert table["turnover"] == "turnover"


def test_map_labels_vectorized() -> None:
    mapping = load_label_mapping(ONTOLOGY_DIR / "seven_to_five_knee_angle_v1.yaml")
    labels = np.array([1, 2, 5, 6, 7], dtype=np.int64)
    mapped = mapping.map_labels(labels)
    np.testing.assert_array_equal(mapped, np.array([1, 2, 5, 5, 6], dtype=np.int64))


def test_benchmark_manifest_contract() -> None:
    manifest = load_benchmark_manifest()
    assert manifest["benchmark"]["version"] == "1.0.0"
    assert manifest["dataset"]["frame_label_rows"] == 35825
    assert manifest["ontology"]["canonical"].endswith("seven_phase_v1.yaml")
    assert manifest["baselines"]["B1"]["version"] == "B1-repro-v1"
    assert "boundary_mae_frames" in manifest["evaluation"]["primary_metrics"]
    assert "boundary_mae_ms" in manifest["evaluation"]["secondary_metrics"]
    assert manifest["evaluation"]["fps_policy"] == "explicit_required_for_ms"


def test_incomplete_mapping_raises() -> None:
    invalid = Path(__file__).resolve().parent / "fixtures" / "invalid_incomplete_mapping.yaml"
    with pytest.raises(ValueError, match="Incomplete mapping"):
        load_label_mapping(invalid, ontology_dir=ONTOLOGY_DIR)
