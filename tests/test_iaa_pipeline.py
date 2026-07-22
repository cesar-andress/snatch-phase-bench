"""Pipeline tests with synthetic data only (no fabricated study results)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from snatch_phase_bench.evaluation.iaa import compute_iaa
from snatch_phase_bench.evaluation.iaa_pipeline import (
    Annotator2IncompleteError,
    PipelinePaths,
    assess_status,
    load_aligned_annotations,
    run_pipeline,
    write_figures,
    write_tables,
)
from snatch_phase_bench.ontology.loader import load_ontology
from tests.test_iaa import _segment_rows


def test_assess_status_not_ready_without_annotator2(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    iaa = repo / "analysis" / "iaa"
    iaa.mkdir(parents=True)
    (iaa / "subset_manifest.json").write_text(
        '{"videos": [{"video_relpath": "demo/a.mp4"}, {"video_relpath": "demo/b.mp4"}]}\n',
        encoding="utf-8",
    )
    a1 = tmp_path / "a1.csv"
    rows = _segment_rows(
        "demo/a.mp4",
        [
            (0, 4, "unlabeled"),
            (5, 14, "setup"),
            (15, 24, "first_pull"),
            (25, 27, "transition"),
            (28, 34, "second_pull"),
            (35, 44, "turnover"),
            (45, 54, "catch"),
            (55, 70, "recovery"),
        ],
    )
    rows.to_csv(a1, index=False)
    paths = PipelinePaths.from_repo(
        repo, annotator1=a1, annotator2_dir=iaa / "annotator2" / "segments"
    )
    status = assess_status(paths)
    assert status.ready is False
    assert status.n_required == 2
    assert status.n_annotator2 == 0


def test_write_tables_and_figures_synthetic(tmp_path: Path) -> None:
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
    result = compute_iaa(
        _segment_rows(vr, intervals_a),
        _segment_rows(vr, intervals_b),
        [vr],
        ontology=ontology,
        fps=25.0,
    )
    tables = write_tables(result, tmp_path / "tables")
    figs = write_figures(result, tmp_path / "figures")
    assert any(p.name == "iaa_global.tex" for p in tables)
    assert any(p.name == "iaa_per_video.csv" for p in tables)
    assert any(p.name == "iaa_abs_diff_histogram.png" for p in figs)
    assert any(p.name == "iaa_bland_altman.pdf" for p in figs)
    assert result.global_abs_diff_frames.mean == pytest.approx(1.0)


def test_run_pipeline_end_to_end_tmp(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    iaa = repo / "analysis" / "iaa"
    seg_dir = iaa / "annotator2" / "segments" / "demo"
    seg_dir.mkdir(parents=True)
    vr = "demo/snatch_demo_i1_ok_000001.mp4"
    (iaa / "subset_manifest.json").write_text(
        f'{{"videos": [{{"video_relpath": "{vr}"}}]}}\n',
        encoding="utf-8",
    )
    intervals = [
        (0, 4, "unlabeled"),
        (5, 14, "setup"),
        (15, 24, "first_pull"),
        (25, 27, "transition"),
        (28, 34, "second_pull"),
        (35, 44, "turnover"),
        (45, 54, "catch"),
        (55, 70, "recovery"),
    ]
    a1 = tmp_path / "a1.csv"
    _segment_rows(vr, intervals).to_csv(a1, index=False)
    _segment_rows(vr, intervals).to_csv(seg_dir / "snatch_demo_i1_ok_000001.csv", index=False)

    paths = PipelinePaths.from_repo(
        repo, annotator1=a1, annotator2_dir=iaa / "annotator2" / "segments"
    )
    artifacts = run_pipeline(paths, fps=25.0)
    assert artifacts.result.global_abs_diff_frames.mean == pytest.approx(0.0)
    assert artifacts.results_md.exists()
    assert (paths.figures_dir / "iaa_abs_diff_histogram.png").exists()
    assert (paths.tables_dir / "iaa_global.tex").exists()


def test_load_aligned_refuses_incomplete(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    iaa = repo / "analysis" / "iaa"
    (iaa / "annotator2" / "segments").mkdir(parents=True)
    (iaa / "subset_manifest.json").write_text(
        '{"videos": [{"video_relpath": "demo/a.mp4"}, {"video_relpath": "demo/b.mp4"}]}\n',
        encoding="utf-8",
    )
    a1 = tmp_path / "a1.csv"
    intervals = [
        (0, 4, "unlabeled"),
        (5, 14, "setup"),
        (15, 24, "first_pull"),
        (25, 27, "transition"),
        (28, 34, "second_pull"),
        (35, 44, "turnover"),
        (45, 54, "catch"),
        (55, 70, "recovery"),
    ]
    pd.concat(
        [_segment_rows("demo/a.mp4", intervals), _segment_rows("demo/b.mp4", intervals)],
        ignore_index=True,
    ).to_csv(a1, index=False)
    _segment_rows("demo/a.mp4", intervals).to_csv(
        iaa / "annotator2" / "segments" / "a.csv", index=False
    )
    paths = PipelinePaths.from_repo(
        repo, annotator1=a1, annotator2_dir=iaa / "annotator2" / "segments"
    )
    with pytest.raises(Annotator2IncompleteError) as exc:
        load_aligned_annotations(paths, allow_partial=False)
    assert "demo/b.mp4" in exc.value.missing
