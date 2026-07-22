"""End-to-end inter-annotator agreement analysis pipeline.

Loads both annotators, aligns videos and ontology boundaries, computes
agreement statistics, and writes publication tables/figures.

Does not fabricate results: incomplete annotator-2 coverage raises
``Annotator2IncompleteError``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from snatch_phase_bench.evaluation.iaa import (
    IAAResult,
    compute_iaa,
    load_annotator2_directory,
    load_segment_csv,
    per_video_descriptive_frame,
    render_global_latex_table,
    render_global_markdown_table,
    render_per_video_latex_table,
    render_per_video_markdown_table,
    render_transition_latex_table,
    render_transition_markdown_table,
)
from snatch_phase_bench.ontology.loader import load_ontology

DEFAULT_ANNOTATOR1 = Path(
    "~/papers/Paper_TFM-main/data/annotations/master_segment_labels.csv"
).expanduser()


class Annotator2IncompleteError(RuntimeError):
    """Raised when annotator-2 labels are missing or incomplete."""

    def __init__(self, message: str, *, missing: list[str] | None = None) -> None:
        super().__init__(message)
        self.missing = missing or []


@dataclass
class PipelinePaths:
    repo_root: Path
    manifest: Path
    annotator1: Path
    annotator2_dir: Path
    results_dir: Path
    tables_dir: Path
    figures_dir: Path

    @classmethod
    def from_repo(
        cls,
        repo_root: Path,
        *,
        annotator1: Path | None = None,
        annotator2_dir: Path | None = None,
    ) -> PipelinePaths:
        root = repo_root.resolve()
        iaa = root / "analysis" / "iaa"
        return cls(
            repo_root=root,
            manifest=iaa / "subset_manifest.json",
            annotator1=annotator1 or DEFAULT_ANNOTATOR1,
            annotator2_dir=annotator2_dir or (iaa / "annotator2" / "segments"),
            results_dir=iaa / "results",
            tables_dir=iaa / "tables",
            figures_dir=iaa / "figures",
        )


@dataclass
class PipelineStatus:
    ready: bool
    n_required: int
    n_annotator1: int
    n_annotator2: int
    missing_annotator1: list[str] = field(default_factory=list)
    missing_annotator2: list[str] = field(default_factory=list)
    annotator1_exists: bool = False
    annotator2_dir_exists: bool = False
    messages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "n_required": self.n_required,
            "n_annotator1": self.n_annotator1,
            "n_annotator2": self.n_annotator2,
            "missing_annotator1": self.missing_annotator1,
            "missing_annotator2": self.missing_annotator2,
            "annotator1_exists": self.annotator1_exists,
            "annotator2_dir_exists": self.annotator2_dir_exists,
            "messages": self.messages,
        }


@dataclass
class PipelineArtifacts:
    result: IAAResult
    videos_used: list[str]
    paired_csv: Path
    agreement_json: Path
    results_md: Path
    table_paths: list[Path]
    figure_paths: list[Path]


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_videos(manifest: dict[str, Any]) -> list[str]:
    return [str(item["video_relpath"]) for item in manifest["videos"]]


def _present_videos(segments: pd.DataFrame) -> set[str]:
    return set(segments["video_relpath"].astype(str).unique())


def missing_videos(segments: pd.DataFrame, required: list[str]) -> list[str]:
    present = _present_videos(segments)
    return [vr for vr in required if vr not in present]


def assess_status(paths: PipelinePaths) -> PipelineStatus:
    """Readiness check without computing agreement numbers."""
    messages: list[str] = []
    if not paths.manifest.exists():
        return PipelineStatus(
            ready=False,
            n_required=0,
            n_annotator1=0,
            n_annotator2=0,
            messages=[f"Missing subset manifest: {paths.manifest}"],
        )
    videos = manifest_videos(load_manifest(paths.manifest))
    a1_exists = paths.annotator1.exists()
    a2_exists = paths.annotator2_dir.exists()
    missing_a1: list[str] = list(videos)
    missing_a2: list[str] = list(videos)
    n_a1 = 0
    n_a2 = 0

    if not a1_exists:
        messages.append(f"Annotator-1 CSV not found: {paths.annotator1}")
    else:
        seg_a = load_segment_csv(paths.annotator1)
        missing_a1 = missing_videos(seg_a, videos)
        n_a1 = len(videos) - len(missing_a1)
        if missing_a1:
            messages.append(f"Annotator-1 missing {len(missing_a1)} subset video(s).")

    if not a2_exists:
        messages.append(
            f"Annotator-2 directory not found: {paths.annotator2_dir}. "
            "Deposit segment CSVs when available; do not invent labels."
        )
    else:
        try:
            seg_b = load_annotator2_directory(paths.annotator2_dir)
            missing_a2 = missing_videos(seg_b, videos)
            n_a2 = len(videos) - len(missing_a2)
            if missing_a2:
                messages.append(
                    f"Annotator-2 incomplete: {n_a2}/{len(videos)} videos. "
                    "Pipeline will not emit manuscript tables/figures yet."
                )
            else:
                messages.append("Annotator-2 coverage complete; pipeline is ready to run.")
        except FileNotFoundError:
            messages.append(
                f"No annotator-2 CSV files under {paths.annotator2_dir}."
            )
            missing_a2 = list(videos)
            n_a2 = 0

    ready = a1_exists and not missing_a1 and n_a2 == len(videos) and not missing_a2
    if ready and not messages:
        messages.append("Ready.")
    return PipelineStatus(
        ready=ready,
        n_required=len(videos),
        n_annotator1=n_a1,
        n_annotator2=n_a2,
        missing_annotator1=missing_a1,
        missing_annotator2=missing_a2,
        annotator1_exists=a1_exists,
        annotator2_dir_exists=a2_exists,
        messages=messages,
    )


def load_aligned_annotations(
    paths: PipelinePaths,
    *,
    allow_partial: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, list[str], list[str]]:
    """Load both annotators and align on the frozen subset video list."""
    if not paths.manifest.exists():
        raise FileNotFoundError(paths.manifest)
    if not paths.annotator1.exists():
        raise FileNotFoundError(paths.annotator1)

    videos = manifest_videos(load_manifest(paths.manifest))
    try:
        segments_b = load_annotator2_directory(paths.annotator2_dir)
    except FileNotFoundError as exc:
        raise Annotator2IncompleteError(
            f"Annotator-2 labels unavailable under {paths.annotator2_dir}",
            missing=list(videos),
        ) from exc

    segments_a = load_segment_csv(paths.annotator1)
    segments_a = segments_a[segments_a["video_relpath"].isin(videos)].copy()
    segments_b = segments_b[segments_b["video_relpath"].isin(videos)].copy()

    missing_a = missing_videos(segments_a, videos)
    missing_b = missing_videos(segments_b, videos)
    if missing_a:
        raise FileNotFoundError(
            "Annotator-1 missing subset videos:\n  - " + "\n  - ".join(missing_a)
        )
    if missing_b and not allow_partial:
        raise Annotator2IncompleteError(
            "Annotator-2 coverage incomplete; refusing to fabricate agreement output.\n"
            "Missing:\n  - "
            + "\n  - ".join(missing_b)
            + f"\nProgress: {len(videos) - len(missing_b)}/{len(videos)}.",
            missing=missing_b,
        )
    use_videos = [vr for vr in videos if vr not in missing_b]
    return segments_a, segments_b, use_videos, missing_b


def write_tables(result: IAAResult, tables_dir: Path) -> list[Path]:
    tables_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    mapping = {
        "iaa_global.md": render_global_markdown_table(result) + "\n",
        "iaa_global.tex": render_global_latex_table(result),
        "iaa_per_transition.md": render_transition_markdown_table(result) + "\n",
        "iaa_per_transition.tex": render_transition_latex_table(result),
        "iaa_per_video.md": render_per_video_markdown_table(result) + "\n",
        "iaa_per_video.tex": render_per_video_latex_table(result),
    }
    for name, text in mapping.items():
        path = tables_dir / name
        path.write_text(text, encoding="utf-8")
        written.append(path)

    # CSV companions for easy manuscript paste / spreadsheet checks.
    per_video = per_video_descriptive_frame(result)
    csv_video = tables_dir / "iaa_per_video.csv"
    per_video.to_csv(csv_video, index=False)
    written.append(csv_video)

    transition_rows = []
    for key, tr in result.per_transition.items():
        transition_rows.append(
            {
                "transition_key": key,
                "n_matched": tr.n_matched,
                "mean_abs_diff_frames": tr.abs_diff_frames.mean,
                "median_abs_diff_frames": tr.abs_diff_frames.median,
                "p95_abs_diff_frames": tr.abs_diff_frames.p95,
                "icc_2_1": tr.icc.icc,
                "n_only_annotator1": tr.n_only_annotator1,
                "n_only_annotator2": tr.n_only_annotator2,
            }
        )
    csv_tr = tables_dir / "iaa_per_transition.csv"
    pd.DataFrame(transition_rows).to_csv(csv_tr, index=False)
    written.append(csv_tr)
    return written


def _savefig(fig: plt.Figure, path_stem: Path) -> list[Path]:
    paths = [path_stem.with_suffix(".png"), path_stem.with_suffix(".pdf")]
    for path in paths:
        fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return paths


def write_figures(result: IAAResult, figures_dir: Path) -> list[Path]:
    """Publication figures from paired boundary differences only."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    df = pd.DataFrame(result.paired_rows)
    if df.empty:
        # Still create an explanatory placeholder figure stating no pairs.
        fig, ax = plt.subplots(figsize=(6, 3), dpi=150)
        ax.axis("off")
        ax.text(
            0.5,
            0.5,
            "No paired boundaries available.\n(IAA figure deferred.)",
            ha="center",
            va="center",
        )
        written.extend(_savefig(fig, figures_dir / "iaa_no_pairs"))
        return written

    transitions = list(result.per_transition.keys())
    # 1) Global absolute-difference histogram
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=150)
    abs_vals = df["abs_diff_frames"].to_numpy(dtype=float)
    bins = max(10, min(40, int(np.sqrt(len(abs_vals))) * 2))
    ax.hist(abs_vals, bins=bins, color="#4C72B0", edgecolor="white", alpha=0.9)
    if result.global_abs_diff_frames.mean is not None:
        ax.axvline(
            result.global_abs_diff_frames.mean,
            color="#DD8452",
            linewidth=1.6,
            label=f"mean = {result.global_abs_diff_frames.mean:.2f}",
        )
    if result.global_abs_diff_frames.median is not None:
        ax.axvline(
            result.global_abs_diff_frames.median,
            color="#55A868",
            linestyle="--",
            linewidth=1.4,
            label=f"median = {result.global_abs_diff_frames.median:.2f}",
        )
    if result.global_abs_diff_frames.p95 is not None:
        ax.axvline(
            result.global_abs_diff_frames.p95,
            color="#C44E52",
            linestyle=":",
            linewidth=1.4,
            label=f"P95 = {result.global_abs_diff_frames.p95:.2f}",
        )
    ax.set_xlabel("Absolute boundary difference (frames)")
    ax.set_ylabel("Count")
    ax.set_title("IAA: pooled absolute boundary differences")
    ax.legend(frameon=False)
    written.extend(_savefig(fig, figures_dir / "iaa_abs_diff_histogram"))

    # 2) Per-transition box / strip of absolute differences
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    data = [
        df.loc[df["transition_key"] == key, "abs_diff_frames"].to_numpy(dtype=float)
        for key in transitions
    ]
    non_empty = [(key, vals) for key, vals in zip(transitions, data) if len(vals)]
    if non_empty:
        keys_ne, vals_ne = zip(*non_empty)
        ax.boxplot(
            list(vals_ne),
            orientation="vertical",
            patch_artist=True,
            boxprops=dict(facecolor="#4C72B0", alpha=0.35),
            medianprops=dict(color="#DD8452", linewidth=1.5),
        )
        ax.set_xticks(range(1, len(keys_ne) + 1))
        ax.set_xticklabels([k.replace("->", "→") for k in keys_ne])
        for i, vals in enumerate(vals_ne, start=1):
            jitter = np.random.default_rng(42).normal(0, 0.05, size=len(vals))
            ax.scatter(
                np.full(len(vals), i) + jitter,
                vals,
                s=12,
                color="#333333",
                alpha=0.35,
                zorder=3,
            )
    ax.set_ylabel("Absolute difference (frames)")
    ax.set_title("IAA: absolute boundary differences by transition")
    ax.tick_params(axis="x", rotation=25)
    written.extend(_savefig(fig, figures_dir / "iaa_per_transition_boxplot"))

    # 3) Per-transition mean ± descriptive forest (mean with P95 as upper whisker proxy)
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=150)
    y_pos = np.arange(len(transitions))
    means = []
    p95s = []
    for key in transitions:
        tr = result.per_transition[key]
        means.append(tr.abs_diff_frames.mean if tr.abs_diff_frames.mean is not None else np.nan)
        p95s.append(tr.abs_diff_frames.p95 if tr.abs_diff_frames.p95 is not None else np.nan)
    ax.errorbar(
        means,
        y_pos,
        xerr=[
            np.zeros(len(means)),
            np.nan_to_num(np.asarray(p95s) - np.asarray(means), nan=0.0),
        ],
        fmt="o",
        color="#4C72B0",
        ecolor="#4C72B0",
        capsize=3,
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels([k.replace("->", "→") for k in transitions])
    ax.set_xlabel("Mean absolute difference (frames); whisker to P95")
    ax.set_title("IAA: per-transition mean |Δ| with P95")
    written.extend(_savefig(fig, figures_dir / "iaa_per_transition_forest"))

    # 4) Bland–Altman style: mean frame vs signed difference
    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=150)
    mean_frame = 0.5 * (df["frame_annotator1"] + df["frame_annotator2"])
    signed = df["signed_diff_frames"]
    ax.scatter(mean_frame, signed, s=18, alpha=0.55, color="#4C72B0", edgecolors="none")
    ax.axhline(0.0, color="black", linestyle="--", linewidth=1.0)
    mean_signed = float(signed.mean())
    std_signed = float(signed.std(ddof=1)) if len(signed) > 1 else 0.0
    ax.axhline(mean_signed, color="#DD8452", linewidth=1.4, label=f"mean Δ = {mean_signed:.2f}")
    ax.axhline(
        mean_signed + 1.96 * std_signed,
        color="#55A868",
        linestyle=":",
        linewidth=1.2,
        label="mean ± 1.96 SD",
    )
    ax.axhline(mean_signed - 1.96 * std_signed, color="#55A868", linestyle=":", linewidth=1.2)
    ax.set_xlabel("Mean boundary frame (annotator 1 & 2)")
    ax.set_ylabel("Signed difference (A2 − A1 frames)")
    ax.set_title("IAA: Bland–Altman plot of boundary frames")
    ax.legend(frameon=False)
    written.extend(_savefig(fig, figures_dir / "iaa_bland_altman"))

    # 5) Coverage mismatch counts per transition
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=150)
    only1 = [result.per_transition[k].n_only_annotator1 for k in transitions]
    only2 = [result.per_transition[k].n_only_annotator2 for k in transitions]
    x = np.arange(len(transitions))
    width = 0.38
    ax.bar(x - width / 2, only1, width, label="Only annotator 1", color="#C44E52", alpha=0.85)
    ax.bar(x + width / 2, only2, width, label="Only annotator 2", color="#4C72B0", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([k.replace("->", "→") for k in transitions], rotation=25, ha="right")
    ax.set_ylabel("Unmatched boundary count")
    ax.set_title("IAA: transition coverage mismatches")
    ax.legend(frameon=False)
    written.extend(_savefig(fig, figures_dir / "iaa_coverage_mismatch"))

    # 6) Per-video mean absolute difference bars
    per_video = per_video_descriptive_frame(result)
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    labels = [Path(v).stem[:28] for v in per_video["video_relpath"]]
    y = np.arange(len(per_video))
    ax.barh(
        y,
        per_video["mean_abs_diff_frames"].fillna(0.0),
        color="#4C72B0",
        alpha=0.85,
    )
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Mean absolute boundary difference (frames)")
    ax.set_title("IAA: per-video mean |Δ|")
    ax.invert_yaxis()
    written.extend(_savefig(fig, figures_dir / "iaa_per_video_mean_abs"))

    return written


def write_results_markdown(
    path: Path,
    *,
    result: IAAResult,
    videos_used: list[str],
    n_required: int,
    partial: bool,
    figure_names: list[str],
) -> None:
    lines = [
        "# Inter-annotator agreement results",
        "",
        f"**Videos used:** {len(videos_used)} / {n_required}",
        f"**Partial run:** {partial}",
        f"**Paired boundaries:** {len(result.paired_rows)}",
        f"**FPS:** {result.fps}",
        "",
        "> Generated by `scripts/run_iaa_pipeline.py`. Do not hand-edit numbers.",
        "",
        "## Global agreement",
        "",
        render_global_markdown_table(result),
        "",
        "## Per-transition agreement",
        "",
        render_transition_markdown_table(result),
        "",
        "## Per-video descriptive statistics",
        "",
        render_per_video_markdown_table(result),
        "",
        "## Figures",
        "",
    ]
    for name in figure_names:
        lines.append(f"- `{name}`")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def run_pipeline(
    paths: PipelinePaths,
    *,
    fps: float = 25.0,
    allow_partial: bool = False,
) -> PipelineArtifacts:
    """Execute the full IAA analysis and write all artifacts."""
    segments_a, segments_b, use_videos, missing_b = load_aligned_annotations(
        paths, allow_partial=allow_partial
    )
    ontology = load_ontology()
    result = compute_iaa(
        segments_a,
        segments_b,
        use_videos,
        ontology=ontology,
        fps=fps,
    )

    paths.results_dir.mkdir(parents=True, exist_ok=True)
    paths.tables_dir.mkdir(parents=True, exist_ok=True)
    paths.figures_dir.mkdir(parents=True, exist_ok=True)

    paired_csv = paths.results_dir / "paired_boundaries.csv"
    pd.DataFrame(result.paired_rows).to_csv(paired_csv, index=False)

    agreement_json = paths.results_dir / "iaa_agreement.json"
    payload = {
        "status": "computed",
        "partial": bool(missing_b),
        "fps": fps,
        "manifest": str(paths.manifest),
        "annotator1": str(paths.annotator1),
        "annotator2_dir": str(paths.annotator2_dir),
        "videos_used": use_videos,
        "missing_annotator2": missing_b,
        "result": result.to_dict(),
        "paired_boundaries": result.paired_rows,
    }
    agreement_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    table_paths = write_tables(result, paths.tables_dir)
    figure_paths = write_figures(result, paths.figures_dir)
    results_md = paths.results_dir / "IAA_RESULTS.md"
    write_results_markdown(
        results_md,
        result=result,
        videos_used=use_videos,
        n_required=len(manifest_videos(load_manifest(paths.manifest))),
        partial=bool(missing_b),
        figure_names=[p.name for p in figure_paths if p.suffix == ".png"],
    )

    # Machine-readable run manifest (no invented metrics beyond computed result).
    run_meta = {
        "command": "run_iaa_pipeline",
        "ready_policy": "refuse_incomplete_unless_allow_partial",
        "artifacts": {
            "results_md": str(results_md),
            "agreement_json": str(agreement_json),
            "paired_csv": str(paired_csv),
            "tables": [str(p) for p in table_paths],
            "figures": [str(p) for p in figure_paths],
        },
    }
    (paths.results_dir / "pipeline_run_manifest.json").write_text(
        json.dumps(run_meta, indent=2) + "\n", encoding="utf-8"
    )

    return PipelineArtifacts(
        result=result,
        videos_used=use_videos,
        paired_csv=paired_csv,
        agreement_json=agreement_json,
        results_md=results_md,
        table_paths=table_paths,
        figure_paths=figure_paths,
    )
