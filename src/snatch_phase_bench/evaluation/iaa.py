"""Inter-annotator agreement (IAA) metrics for snatch phase boundaries.

Computes boundary-centric agreement between two annotators. Does not invent
results: callers must supply both annotation tables.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd

from snatch_phase_bench.evaluation.boundaries import (
    Boundary,
    allowed_transition_keys,
    extract_boundaries_from_labels,
    match_boundaries_monotonic,
)
from snatch_phase_bench.ontology.loader import load_ontology
from snatch_phase_bench.ontology.phase_ontology import PhaseOntology

PHASE_ORDER = [
    "unlabeled",
    "setup",
    "first_pull",
    "transition",
    "second_pull",
    "turnover",
    "catch",
    "recovery",
]

PHASE_NAME_TO_ID = {name: i for i, name in enumerate(PHASE_ORDER)}

SEGMENT_COLUMNS = [
    "video",
    "video_relpath",
    "start_frame",
    "end_frame",
    "phase_id",
    "phase_name",
]


@dataclass(frozen=True)
class AbsoluteDifferenceSummary:
    n: int
    mean: float | None
    median: float | None
    p95: float | None
    std: float | None
    max: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ICCResult:
    icc: float | None
    n_targets: int
    n_raters: int = 2
    model: str = "ICC(2,1)_absolute_agreement"
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TransitionAgreement:
    transition_key: str
    n_matched: int
    n_only_annotator1: int
    n_only_annotator2: int
    abs_diff_frames: AbsoluteDifferenceSummary
    abs_diff_ms: AbsoluteDifferenceSummary
    icc: ICCResult

    def to_dict(self) -> dict[str, Any]:
        return {
            "transition_key": self.transition_key,
            "n_matched": self.n_matched,
            "n_only_annotator1": self.n_only_annotator1,
            "n_only_annotator2": self.n_only_annotator2,
            "abs_diff_frames": self.abs_diff_frames.to_dict(),
            "abs_diff_ms": self.abs_diff_ms.to_dict(),
            "icc": self.icc.to_dict(),
        }


@dataclass
class IAAResult:
    n_videos: int
    fps: float
    global_abs_diff_frames: AbsoluteDifferenceSummary
    global_abs_diff_ms: AbsoluteDifferenceSummary
    global_icc: ICCResult
    per_transition: dict[str, TransitionAgreement] = field(default_factory=dict)
    paired_rows: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_videos": self.n_videos,
            "fps": self.fps,
            "global_abs_diff_frames": self.global_abs_diff_frames.to_dict(),
            "global_abs_diff_ms": self.global_abs_diff_ms.to_dict(),
            "global_icc": self.global_icc.to_dict(),
            "per_transition": {k: v.to_dict() for k, v in self.per_transition.items()},
            "n_paired_boundaries": len(self.paired_rows),
            "warnings": self.warnings,
        }


def summarize_absolute_differences(values: Iterable[float]) -> AbsoluteDifferenceSummary:
    arr = np.asarray(list(values), dtype=np.float64)
    if arr.size == 0:
        return AbsoluteDifferenceSummary(n=0, mean=None, median=None, p95=None, std=None, max=None)
    return AbsoluteDifferenceSummary(
        n=int(arr.size),
        mean=float(np.mean(arr)),
        median=float(np.median(arr)),
        p95=float(np.percentile(arr, 95)),
        std=float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0,
        max=float(np.max(arr)),
    )


def icc_2_1_absolute(ratings: np.ndarray) -> ICCResult:
    """Two-way random effects, single measures, absolute agreement (Shrout & Fleiss).

    ``ratings`` shape: (n_targets, n_raters). Requires n_targets >= 2 and n_raters == 2
    for the IAA use case; returns ``icc=None`` when underdetermined.
    """
    x = np.asarray(ratings, dtype=np.float64)
    if x.ndim != 2:
        raise ValueError("ratings must be 2-D (targets x raters)")
    n, k = x.shape
    if k != 2:
        raise ValueError(f"expected 2 raters, got {k}")
    if n < 2:
        return ICCResult(icc=None, n_targets=n, note="need at least 2 paired targets")

    mean_target = x.mean(axis=1, keepdims=True)
    mean_rater = x.mean(axis=0, keepdims=True)
    grand = x.mean()

    ss_targets = k * np.sum((mean_target.ravel() - grand) ** 2)
    ss_raters = n * np.sum((mean_rater.ravel() - grand) ** 2)
    ss_error = np.sum((x - mean_target - mean_rater + grand) ** 2)

    df_t = n - 1
    df_r = k - 1
    df_e = (n - 1) * (k - 1)
    msb = ss_targets / df_t
    msr = ss_raters / df_r
    mse = ss_error / df_e if df_e > 0 else np.nan

    denom = msb + (k - 1) * mse + k * (msr - mse) / n
    if not np.isfinite(denom) or denom == 0:
        return ICCResult(icc=None, n_targets=n, note="undefined ICC denominator")
    return ICCResult(icc=float((msb - mse) / denom), n_targets=n)


def load_segment_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in ("video_relpath", "start_frame", "end_frame", "phase_name") if c not in df.columns]
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    if "phase_id" not in df.columns:
        df["phase_id"] = df["phase_name"].map(PHASE_NAME_TO_ID)
    if "video" not in df.columns:
        df["video"] = df["video_relpath"].map(lambda p: Path(str(p)).name)
    return df


def load_annotator2_directory(directory: Path) -> pd.DataFrame:
    """Load per-video segment CSVs or a single combined CSV from annotator2."""
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(directory)
    combined = directory / "master_segment_labels_annotator2.csv"
    if combined.exists():
        return load_segment_csv(combined)
    paths = sorted(directory.glob("**/*.csv"))
    if not paths:
        raise FileNotFoundError(f"no annotator2 CSV files under {directory}")
    frames = [load_segment_csv(p) for p in paths]
    return pd.concat(frames, ignore_index=True)


def segments_to_frame_labels(segments: pd.DataFrame, video_relpath: str) -> np.ndarray:
    """Convert inclusive [start_frame, end_frame] segment rows to a dense label vector."""
    rows = segments[segments["video_relpath"] == video_relpath].sort_values("start_frame")
    if rows.empty:
        raise KeyError(f"no segments for {video_relpath}")
    end = int(rows["end_frame"].max())
    labels = np.zeros(end + 1, dtype=np.int64)
    for row in rows.itertuples():
        start = int(row.start_frame)
        stop = int(row.end_frame)
        if stop < start:
            raise ValueError(f"{video_relpath}: end_frame < start_frame for {row.phase_name}")
        phase_id = int(row.phase_id) if not pd.isna(row.phase_id) else PHASE_NAME_TO_ID[str(row.phase_name)]
        labels[start : stop + 1] = phase_id
    return labels


def extract_video_boundaries(
    segments: pd.DataFrame,
    video_relpath: str,
    ontology: PhaseOntology,
) -> tuple[list[Boundary], list[str]]:
    labels = segments_to_frame_labels(segments, video_relpath)
    return extract_boundaries_from_labels(
        labels,
        video_id=video_relpath,
        ontology=ontology,
        ignore_labels=(0,),
    )


def pair_annotator_boundaries(
    boundaries_a: list[Boundary],
    boundaries_b: list[Boundary],
    ontology: PhaseOntology,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, int]], list[str]]:
    """Monotonic match per transition; A and B are symmetric raters."""
    warnings: list[str] = []
    paired: list[dict[str, Any]] = []
    counts: dict[str, dict[str, int]] = {}
    keys = sorted(allowed_transition_keys(ontology))
    by_a: dict[str, list[Boundary]] = {k: [] for k in keys}
    by_b: dict[str, list[Boundary]] = {k: [] for k in keys}
    for b in boundaries_a:
        by_a.setdefault(b.transition_key, []).append(b)
    for b in boundaries_b:
        by_b.setdefault(b.transition_key, []).append(b)
    for key in sorted(set(by_a) | set(by_b)):
        matching = match_boundaries_monotonic(by_a.get(key, []), by_b.get(key, []), transition_key=key)
        counts[key] = {
            "n_matched": matching.num_matched,
            "n_only_annotator1": matching.num_missed,
            "n_only_annotator2": matching.num_extra,
        }
        for match in matching.matches:
            abs_err = abs(match.ground_truth.frame_index - match.predicted.frame_index)
            paired.append(
                {
                    "video_relpath": match.ground_truth.video_id,
                    "transition_key": key,
                    "frame_annotator1": int(match.ground_truth.frame_index),
                    "frame_annotator2": int(match.predicted.frame_index),
                    "abs_diff_frames": int(abs_err),
                }
            )
    return paired, counts, warnings


def compute_iaa(
    segments_a: pd.DataFrame,
    segments_b: pd.DataFrame,
    video_relpaths: list[str],
    *,
    ontology: PhaseOntology | None = None,
    fps: float = 25.0,
) -> IAAResult:
    ontology = ontology or load_ontology()
    all_paired: list[dict[str, Any]] = []
    per_counts: dict[str, dict[str, int]] = {
        k: {"n_matched": 0, "n_only_annotator1": 0, "n_only_annotator2": 0}
        for k in sorted(allowed_transition_keys(ontology))
    }
    warnings: list[str] = []

    for vr in video_relpaths:
        ba, wa = extract_video_boundaries(segments_a, vr, ontology)
        bb, wb = extract_video_boundaries(segments_b, vr, ontology)
        warnings.extend(wa)
        warnings.extend(wb)
        paired, counts, w = pair_annotator_boundaries(ba, bb, ontology)
        warnings.extend(w)
        all_paired.extend(paired)
        for key, c in counts.items():
            bucket = per_counts.setdefault(
                key, {"n_matched": 0, "n_only_annotator1": 0, "n_only_annotator2": 0}
            )
            for field_name in bucket:
                bucket[field_name] += c[field_name]

    for row in all_paired:
        row["abs_diff_ms"] = float(row["abs_diff_frames"]) * 1000.0 / fps

    global_frames = summarize_absolute_differences(r["abs_diff_frames"] for r in all_paired)
    global_ms = summarize_absolute_differences(r["abs_diff_ms"] for r in all_paired)
    if all_paired:
        ratings = np.asarray(
            [[r["frame_annotator1"], r["frame_annotator2"]] for r in all_paired],
            dtype=np.float64,
        )
        global_icc = icc_2_1_absolute(ratings)
    else:
        global_icc = ICCResult(icc=None, n_targets=0, note="no matched boundaries")

    per_transition: dict[str, TransitionAgreement] = {}
    for key in sorted(per_counts):
        rows = [r for r in all_paired if r["transition_key"] == key]
        abs_f = summarize_absolute_differences(r["abs_diff_frames"] for r in rows)
        abs_m = summarize_absolute_differences(r["abs_diff_ms"] for r in rows)
        if rows:
            ratings = np.asarray(
                [[r["frame_annotator1"], r["frame_annotator2"]] for r in rows],
                dtype=np.float64,
            )
            icc = icc_2_1_absolute(ratings)
        else:
            icc = ICCResult(icc=None, n_targets=0, note="no matched boundaries")
        c = per_counts[key]
        per_transition[key] = TransitionAgreement(
            transition_key=key,
            n_matched=c["n_matched"],
            n_only_annotator1=c["n_only_annotator1"],
            n_only_annotator2=c["n_only_annotator2"],
            abs_diff_frames=abs_f,
            abs_diff_ms=abs_m,
            icc=icc,
        )

    return IAAResult(
        n_videos=len(video_relpaths),
        fps=fps,
        global_abs_diff_frames=global_frames,
        global_abs_diff_ms=global_ms,
        global_icc=global_icc,
        per_transition=per_transition,
        paired_rows=all_paired,
        warnings=warnings,
    )


def latex_escape(text: str) -> str:
    return (
        text.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("#", "\\#")
        .replace("->", "$\\rightarrow$")
    )


def format_optional(value: float | None, fmt: str = "{:.3f}") -> str:
    if value is None:
        return "---"
    return fmt.format(value)


def render_global_markdown_table(result: IAAResult) -> str:
    g = result.global_abs_diff_frames
    gm = result.global_abs_diff_ms
    lines = [
        "| Metric | Frames | Milliseconds (25 fps) |",
        "|--------|-------:|----------------------:|",
        f"| N paired boundaries | {g.n} | {gm.n} |",
        f"| Mean absolute difference | {format_optional(g.mean)} | {format_optional(gm.mean)} |",
        f"| Median absolute difference | {format_optional(g.median)} | {format_optional(gm.median)} |",
        f"| 95th percentile absolute difference | {format_optional(g.p95)} | {format_optional(gm.p95)} |",
        f"| ICC(2,1) absolute agreement | {format_optional(result.global_icc.icc)} | — |",
    ]
    return "\n".join(lines)


def render_transition_markdown_table(result: IAAResult) -> str:
    lines = [
        "| Transition | N | Mean |abs| | Median |abs| | P95 |abs| | ICC(2,1) | Only A1 | Only A2 |",
        "|------------|--:|----------:|------------:|--------:|---------:|--------:|--------:|",
    ]
    for key, tr in result.per_transition.items():
        lines.append(
            f"| `{key}` | {tr.n_matched} | "
            f"{format_optional(tr.abs_diff_frames.mean)} | "
            f"{format_optional(tr.abs_diff_frames.median)} | "
            f"{format_optional(tr.abs_diff_frames.p95)} | "
            f"{format_optional(tr.icc.icc)} | "
            f"{tr.n_only_annotator1} | {tr.n_only_annotator2} |"
        )
    return "\n".join(lines)


def render_global_latex_table(result: IAAResult, label: str = "tab:iaa-global") -> str:
    g = result.global_abs_diff_frames
    gm = result.global_abs_diff_ms
    return "\n".join(
        [
            "\\begin{table}[t]",
            "\\centering",
            "\\caption{Inter-annotator boundary agreement on the IAA subset "
            "(paired transitions present for both annotators).}",
            f"\\label{{{label}}}",
            "\\begin{tabular}{lrr}",
            "\\toprule",
            "Metric & Frames & ms (25\\,fps) \\\\",
            "\\midrule",
            f"N paired boundaries & {g.n} & {gm.n} \\\\",
            f"Mean absolute difference & {format_optional(g.mean)} & {format_optional(gm.mean)} \\\\",
            f"Median absolute difference & {format_optional(g.median)} & {format_optional(gm.median)} \\\\",
            f"95th percentile absolute difference & {format_optional(g.p95)} & {format_optional(gm.p95)} \\\\",
            f"ICC(2,1) absolute agreement & {format_optional(result.global_icc.icc)} & --- \\\\",
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            "",
        ]
    )


def render_transition_latex_table(result: IAAResult, label: str = "tab:iaa-transitions") -> str:
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Per-transition inter-annotator absolute boundary differences (frames).}",
        f"\\label{{{label}}}",
        "\\begin{tabular}{lrrrrrr}",
        "\\toprule",
        "Transition & N & Mean & Median & P95 & ICC & Only A1 / A2 \\\\",
        "\\midrule",
    ]
    for key, tr in result.per_transition.items():
        lines.append(
            f"{latex_escape(key)} & {tr.n_matched} & "
            f"{format_optional(tr.abs_diff_frames.mean)} & "
            f"{format_optional(tr.abs_diff_frames.median)} & "
            f"{format_optional(tr.abs_diff_frames.p95)} & "
            f"{format_optional(tr.icc.icc)} & "
            f"{tr.n_only_annotator1}/{tr.n_only_annotator2} \\\\"
        )
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            "",
        ]
    )
    return "\n".join(lines)
