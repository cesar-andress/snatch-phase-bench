"""Comprehensive tests for canonical segment and boundary metrics."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from snatch_phase_bench.evaluation.boundaries import (
    extract_boundaries_from_labels,
    match_boundaries_monotonic,
)
from snatch_phase_bench.evaluation.evaluate import evaluate_dataset_videos, evaluate_video
from snatch_phase_bench.evaluation.metric_config import load_evaluation_config
from snatch_phase_bench.evaluation.metrics.boundary import (
    FpsRequiredError,
    compute_boundary_metrics,
    frames_to_milliseconds,
    require_fps,
)
from snatch_phase_bench.evaluation.metrics.segment import (
    compute_edit_score,
    compute_segment_metrics,
    compute_segment_metrics_detailed,
    greedy_match_segments,
    labels_to_segments,
    segmental_f1,
)
from snatch_phase_bench.evaluation.results import validate_result_schema, write_evaluation_result
from snatch_phase_bench.evaluation.segments import (
    CanonicalSegment,
    labels_to_canonical_segments,
    validate_non_overlapping,
)
from snatch_phase_bench.ontology import load_label_mapping, load_ontology

FIXTURES = Path(__file__).resolve().parent / "fixtures"
ONTOLOGY_DIR = Path(__file__).resolve().parents[1] / "configs" / "ontology"


def mini_ontology():
    return load_ontology(FIXTURES / "mini_three_phase_v1.yaml")


def seven_ontology():
    return load_ontology(ONTOLOGY_DIR / "seven_phase_v1.yaml")


def test_half_open_segment_convention() -> None:
    segment = CanonicalSegment(
        video_id="v1",
        label=1,
        start_frame=0,
        end_frame=3,
        ontology_id="mini",
        ontology_version="1.0.0",
    )
    assert segment.length() == 3
    other = CanonicalSegment("v1", 1, 2, 5, "mini", "1.0.0")
    assert segment.temporal_iou(other) == pytest.approx(0.2)


def test_segment_validation_rejects_invalid_interval() -> None:
    with pytest.raises(ValueError):
        CanonicalSegment("v1", 1, 4, 4, "mini", "1.0.0")


def test_perfect_segmental_f1_and_edit_score() -> None:
    labels = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    assert segmental_f1(labels, labels, iou_threshold=0.5) == 1.0
    edit = compute_edit_score(labels, labels)
    assert edit.normalized_score == 1.0
    assert edit.levenshtein_distance == 0


def test_one_frame_boundary_shift_mae() -> None:
    gt = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    pred = np.array([1, 1, 1, 2, 2, 3, 3], dtype=np.int64)
    ontology = mini_ontology()
    metrics = compute_boundary_metrics(
        gt,
        pred,
        video_id="v1",
        ontology=ontology,
        ignore_labels=(0,),
    )
    ab = metrics.per_transition["phase_a->phase_b"]
    bc = metrics.per_transition["phase_b->phase_c"]
    assert ab.num_matched == 1
    assert ab.mae_frames == 1.0
    assert bc.mae_frames == 1.0
    assert metrics.aggregate_micro["boundary_mae_frames"] == 1.0


def test_missing_phase_extra_boundary() -> None:
    gt = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    pred = np.array([1, 1, 2, 2, 2, 2, 2, 2], dtype=np.int64)
    ontology = mini_ontology()
    metrics = compute_boundary_metrics(gt, pred, video_id="v1", ontology=ontology)
    assert metrics.per_transition["phase_b->phase_c"].num_missed == 1
    assert metrics.per_transition["phase_b->phase_c"].num_matched == 0


def test_empty_prediction_segment_metrics() -> None:
    gt = np.array([1, 1, 2, 2], dtype=np.int64)
    pred = np.array([0, 0, 0, 0], dtype=np.int64)
    detailed = compute_segment_metrics_detailed(gt, pred, ignore_label=0)
    assert detailed.aggregate["segmental_f1_at_50"] == 0.0
    assert detailed.edit.normalized_score < 1.0


def test_empty_ground_truth_edit_score() -> None:
    gt = np.array([0, 0, 0], dtype=np.int64)
    pred = np.array([1, 1, 1], dtype=np.int64)
    edit = compute_edit_score(gt, pred, ignore_label=0)
    assert edit.normalized_score == 0.0
    assert edit.levenshtein_distance == 1


def test_greedy_segment_matching_not_hungarian() -> None:
    gt = [labels_to_segments(np.array([1, 1, 2, 2]))[0]]
    pred_segments = labels_to_segments(np.array([1, 1, 1, 2]))
    counts, _ = greedy_match_segments(gt, pred_segments, iou_threshold=0.1)
    assert counts.tp == 1


def test_invalid_transition_reported() -> None:
    labels = np.array([1, 3, 2, 2], dtype=np.int64)
    ontology = mini_ontology()
    _, warnings = extract_boundaries_from_labels(labels, video_id="v1", ontology=ontology)
    assert any("Invalid transition" in warning for warning in warnings)


def test_fps_conversion_and_missing_fps_error() -> None:
    assert frames_to_milliseconds(3.0, fps=30.0) == 100.0
    with pytest.raises(FpsRequiredError):
        require_fps(None, context="test")


def test_ms_metrics_only_with_explicit_fps() -> None:
    gt = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    pred = np.array([1, 1, 1, 2, 2, 3, 3], dtype=np.int64)
    ontology = mini_ontology()
    frames_only = compute_boundary_metrics(gt, pred, video_id="v1", ontology=ontology)
    assert "boundary_mae_ms" not in frames_only.aggregate_micro

    with_fps = compute_boundary_metrics(
        gt,
        pred,
        video_id="v1",
        ontology=ontology,
        fps=25.0,
        fps_source="unit_test",
    )
    assert with_fps.aggregate_micro["boundary_mae_ms"] == pytest.approx(40.0)


def test_mixed_fps_per_video_in_dataset_eval() -> None:
    ontology = mini_ontology()
    config = load_evaluation_config()
    config_path = Path(__file__).resolve().parents[1] / "configs" / "benchmark.yaml"
    config = load_evaluation_config(config_path)
    from snatch_phase_bench.evaluation.metric_config import load_evaluation_artifacts

    artifacts = load_evaluation_artifacts(config)
    gt = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    pred = gt.copy()
    v25 = evaluate_video(
        gt,
        pred,
        video_id="v25",
        ontology=ontology,
        config=config,
        ignore_label_ids=artifacts["ignore_label_ids"],
        fps=25.0,
        fps_source="synthetic",
    )
    v30 = evaluate_video(
        gt,
        pred,
        video_id="v30",
        ontology=ontology,
        config=config,
        ignore_label_ids=artifacts["ignore_label_ids"],
        fps=30.0,
        fps_source="synthetic",
    )
    assert v25.boundary["aggregate_micro"]["boundary_mae_ms"] == 0.0
    assert v30.boundary["aggregate_micro"]["boundary_mae_ms"] == 0.0


def test_seven_phase_ontology_boundaries() -> None:
    gt = np.array([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7], dtype=np.int64)
    ontology = seven_ontology()
    boundaries, warnings = extract_boundaries_from_labels(gt, video_id="lift", ontology=ontology)
    assert len(warnings) == 0
    assert len(boundaries) == 6
    assert boundaries[0].transition_key == "setup->first_pull"


def test_mapped_five_phase_evaluation_is_derived() -> None:
    gt = np.array([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7], dtype=np.int64)
    pred = gt.copy()
    result = evaluate_dataset_videos(
        {"lift": {"y_true": gt, "y_pred": pred}},
        model_identifier="unit_test",
        use_b0_mapping=True,
    )
    assert result.evaluation_derived is True
    assert result.mapping_id == "seven_to_five_knee_angle_v1"
    assert np.array_equal(gt, np.array([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]))


def test_original_labels_untouched_by_mapping() -> None:
    gt = np.array([1, 1, 2, 2, 5, 5, 6, 6, 7, 7], dtype=np.int64)
    pred = gt.copy()
    mapping = load_label_mapping(ONTOLOGY_DIR / "seven_to_five_knee_angle_v1.yaml")
    mapped = mapping.map_labels(gt.copy())
    assert 6 in gt
    assert 5 in mapped


def test_deterministic_repeated_execution() -> None:
    gt = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    pred = np.array([1, 1, 1, 2, 2, 3, 3], dtype=np.int64)
    ontology = mini_ontology()
    first = compute_boundary_metrics(gt, pred, video_id="v1", ontology=ontology)
    second = compute_boundary_metrics(gt, pred, video_id="v1", ontology=ontology)
    assert first.aggregate_micro == second.aggregate_micro


def test_result_schema_roundtrip(tmp_path: Path) -> None:
    gt = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    result = evaluate_dataset_videos(
        {"v1": {"y_true": gt, "y_pred": gt}},
        model_identifier="schema_test",
    )
    out = tmp_path / "result.json"
    write_evaluation_result(out, result)
    payload = __import__("json").loads(out.read_text(encoding="utf-8"))
    validate_result_schema(payload)
    assert payload["schema_version"] == "1.0.0"


def test_monotonic_matching_wrong_order() -> None:
    gt = extract_boundaries_from_labels(
        np.array([1, 1, 2, 2, 3, 3, 3, 3, 3, 3]),
        video_id="v1",
        ontology=mini_ontology(),
    )[0]
    pred = extract_boundaries_from_labels(
        np.array([1, 1, 2, 2, 2, 2, 3, 3, 3, 3]),
        video_id="v1",
        ontology=mini_ontology(),
    )[0]
    matching = match_boundaries_monotonic(
        [item for item in gt if item.transition_key == "phase_b->phase_c"],
        [item for item in pred if item.transition_key == "phase_b->phase_c"],
        transition_key="phase_b->phase_c",
    )
    assert matching.num_matched == 1


def test_canonical_segments_non_overlapping() -> None:
    labels = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    segments = labels_to_canonical_segments(
        labels,
        video_id="v1",
        ontology=mini_ontology(),
        ignore_labels=(0,),
    )
    validate_non_overlapping(segments)
    assert len(segments) == 3


def test_legacy_compute_segment_metrics_keys() -> None:
    labels = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    metrics = compute_segment_metrics(labels, labels)
    assert "segmental_f1_at_50" in metrics
    assert "edit_levenshtein_distance" in metrics
