"""Temporal window overlap / autocorrelation analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class TemporalAutocorrelationReport:
    window_size: int
    stride: int
    shared_frames_per_adjacent_window: int
    overlap_fraction: float
    total_windows: int
    total_videos: int
    windows_per_video_mean: float
    windows_per_video_median: float
    approximate_independent_samples_stride_window: int
    approximate_independent_samples: int
    ratio_reported_to_approx_independent: float
    notes: list[str]


def analyze_temporal_autocorrelation(
    meta_df: pd.DataFrame,
    window_size: int = 31,
    stride: int = 1,
) -> TemporalAutocorrelationReport:
    if window_size < 2:
        raise ValueError("window_size must be >= 2")
    if stride < 1:
        raise ValueError("stride must be >= 1")

    shared = window_size - stride
    overlap_fraction = shared / window_size if window_size else 0.0

    per_video_counts = meta_df.groupby("video_relpath").size()
    total_windows = int(len(meta_df))
    total_videos = int(meta_df["video_relpath"].nunique())

    approx_stride = window_size  # non-overlapping windows as conservative approximation
    approx_independent = 0
    for _video, group in meta_df.groupby("video_relpath"):
        n_frames = len(group)
        if n_frames >= window_size:
            approx_independent += 1 + max(0, (n_frames - window_size) // approx_stride)

    ratio = total_windows / approx_independent if approx_independent else float("inf")

    notes = [
        "Adjacent windows share shared_frames_per_adjacent_window of window_size frames.",
        "Approximate independent samples uses non-overlapping windows of size window_size per video.",
        "This quantifies temporal autocorrelation; it is not equivalent to cross-split leakage.",
    ]

    return TemporalAutocorrelationReport(
        window_size=window_size,
        stride=stride,
        shared_frames_per_adjacent_window=shared,
        overlap_fraction=overlap_fraction,
        total_windows=total_windows,
        total_videos=total_videos,
        windows_per_video_mean=float(per_video_counts.mean()),
        windows_per_video_median=float(per_video_counts.median()),
        approximate_independent_samples_stride_window=approx_stride,
        approximate_independent_samples=int(approx_independent),
        ratio_reported_to_approx_independent=float(ratio),
        notes=notes,
    )


def report_to_markdown(report: TemporalAutocorrelationReport) -> str:
    lines = [
        "# Temporal Autocorrelation Analysis",
        "",
        "## Window overlap",
        f"- Window size: {report.window_size}",
        f"- Stride: {report.stride}",
        f"- Shared frames between consecutive windows: {report.shared_frames_per_adjacent_window}",
        f"- Overlap fraction: {report.overlap_fraction:.4f} ({report.overlap_fraction * 100:.2f}%)",
        "",
        "## Dataset coverage",
        f"- Total windows: {report.total_windows}",
        f"- Total videos: {report.total_videos}",
        f"- Windows per video (mean): {report.windows_per_video_mean:.2f}",
        f"- Windows per video (median): {report.windows_per_video_median:.1f}",
        "",
        "## Approximate independent temporal samples",
        f"- Non-overlapping window stride used: {report.approximate_independent_samples_stride_window}",
        f"- Approximate independent samples: {report.approximate_independent_samples}",
        f"- Ratio reported windows / approximate independent: {report.ratio_reported_to_approx_independent:.2f}",
        "",
        "## Notes",
    ]
    lines.extend(f"- {note}" for note in report.notes)
    return "\n".join(lines) + "\n"


def report_to_json(report: TemporalAutocorrelationReport) -> str:
    import json

    return json.dumps(asdict(report), indent=2)
