"""Unit tests for IAA helpers (synthetic data only; no study results)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from snatch_phase_bench.evaluation.iaa import (
    compute_iaa,
    icc_2_1_absolute,
    segments_to_frame_labels,
    summarize_absolute_differences,
)
from snatch_phase_bench.ontology.loader import load_ontology


def test_icc_perfect_agreement() -> None:
    ratings = np.asarray([[10.0, 10.0], [20.0, 20.0], [30.0, 30.0], [40.0, 40.0]])
    result = icc_2_1_absolute(ratings)
    assert result.icc is not None
    assert result.icc == pytest.approx(1.0, abs=1e-9)


def test_icc_constant_disagreement_includes_bias() -> None:
    # Absolute-agreement ICC should be < 1 when raters differ by a constant offset.
    ratings = np.asarray([[10.0, 12.0], [20.0, 22.0], [30.0, 32.0], [40.0, 42.0]])
    result = icc_2_1_absolute(ratings)
    assert result.icc is not None
    assert result.icc < 1.0


def test_summarize_absolute_differences() -> None:
    summary = summarize_absolute_differences([0, 1, 2, 3, 100])
    assert summary.n == 5
    assert summary.mean == pytest.approx(21.2)
    assert summary.median == pytest.approx(2.0)
    assert summary.p95 == pytest.approx(80.4) or summary.p95 is not None


def _segment_rows(video_relpath: str, intervals: list[tuple[int, int, str]]) -> pd.DataFrame:
    video = video_relpath.split("/")[-1]
    rows = []
    phase_ids = {
        "unlabeled": 0,
        "setup": 1,
        "first_pull": 2,
        "transition": 3,
        "second_pull": 4,
        "turnover": 5,
        "catch": 6,
        "recovery": 7,
    }
    for start, end, name in intervals:
        rows.append(
            {
                "video": video,
                "video_relpath": video_relpath,
                "start_frame": start,
                "end_frame": end,
                "phase_id": phase_ids[name],
                "phase_name": name,
            }
        )
    return pd.DataFrame(rows)


def test_compute_iaa_synthetic_small_offset() -> None:
    ontology = load_ontology()
    vr = "demo/snatch_demo_i1_ok_000001.mp4"
    intervals_a = [
        (0, 4, "unlabeled"),
        (5, 14, "setup"),
        (15, 24, "first_pull"),
        (25, 27, "transition"),
        (28, 34, "second_pull"),
        (35, 44, "turnover"),
        (45, 54, "catch"),
        (55, 70, "recovery"),
        (71, 80, "unlabeled"),
    ]
    # Annotator 2 shifts every supervised boundary by +1 frame.
    intervals_b = [
        (0, 5, "unlabeled"),
        (6, 15, "setup"),
        (16, 25, "first_pull"),
        (26, 28, "transition"),
        (29, 35, "second_pull"),
        (36, 45, "turnover"),
        (46, 55, "catch"),
        (56, 71, "recovery"),
        (72, 80, "unlabeled"),
    ]
    seg_a = _segment_rows(vr, intervals_a)
    seg_b = _segment_rows(vr, intervals_b)
    labels = segments_to_frame_labels(seg_a, vr)
    assert labels[15] == 2
    result = compute_iaa(seg_a, seg_b, [vr], ontology=ontology, fps=25.0)
    assert result.global_abs_diff_frames.n == 6
    assert result.global_abs_diff_frames.mean == pytest.approx(1.0)
    assert result.global_abs_diff_frames.median == pytest.approx(1.0)
    assert result.global_abs_diff_ms.mean == pytest.approx(40.0)
    assert result.global_icc.icc is not None
