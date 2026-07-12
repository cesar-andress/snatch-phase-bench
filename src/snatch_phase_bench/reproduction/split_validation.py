"""Validate athlete-level train/validation/test split."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class SplitValidationReport:
    passed: bool
    train_athletes: int
    val_athletes: int
    test_athletes: int
    train_windows: int
    val_windows: int
    test_windows: int
    train_videos: int
    val_videos: int
    test_videos: int
    athlete_overlap: list[str]
    video_overlap: list[str]
    missing_keypoint_videos: list[str]
    errors: list[str]
    warnings: list[str]


def validate_split(
    meta_df: pd.DataFrame,
    split: dict[str, Any],
    keypoints_dir: Path | None = None,
    expected: dict[str, Any] | None = None,
) -> SplitValidationReport:
    errors: list[str] = []
    warnings: list[str] = []

    train = set(map(str, split.get("train_athletes", [])))
    val = set(map(str, split.get("val_athletes", [])))
    test = set(map(str, split.get("test_athletes", [])))

    athlete_overlap = sorted((train & val) | (train & test) | (val & test))
    if athlete_overlap:
        errors.append(f"Athletes appear in multiple splits: {athlete_overlap}")

    all_athletes = set(meta_df["athlete"].astype(str).unique())
    split_union = train | val | test
    if split_union != all_athletes:
        missing = sorted(all_athletes - split_union)
        extra = sorted(split_union - all_athletes)
        if missing:
            errors.append(f"Athletes in meta but not in split: {missing[:10]}")
        if extra:
            errors.append(f"Athletes in split but not in meta: {extra[:10]}")

    train_mask = meta_df["athlete"].astype(str).isin(train)
    val_mask = meta_df["athlete"].astype(str).isin(val)
    test_mask = meta_df["athlete"].astype(str).isin(test)

    train_videos = set(meta_df.loc[train_mask, "video_relpath"].astype(str))
    val_videos = set(meta_df.loc[val_mask, "video_relpath"].astype(str))
    test_videos = set(meta_df.loc[test_mask, "video_relpath"].astype(str))

    video_overlap = sorted((train_videos & val_videos) | (train_videos & test_videos) | (val_videos & test_videos))
    if video_overlap:
        errors.append(f"Videos appear in multiple splits: {video_overlap[:10]}")

    missing_keypoints: list[str] = []
    if keypoints_dir is not None:
        for video in sorted(meta_df["video_relpath"].astype(str).unique()):
            kp = keypoints_dir / Path(video).with_suffix(".csv")
            if not kp.exists():
                missing_keypoints.append(video)
        if missing_keypoints:
            errors.append(f"Missing keypoint CSVs for {len(missing_keypoints)} videos.")

    if expected:
        if len(train) != expected.get("train_athletes"):
            warnings.append(f"Train athlete count {len(train)} != expected {expected.get('train_athletes')}")
        if len(val) != expected.get("val_athletes"):
            warnings.append(f"Val athlete count {len(val)} != expected {expected.get('val_athletes')}")
        if len(test) != expected.get("test_athletes"):
            warnings.append(f"Test athlete count {len(test)} != expected {expected.get('test_athletes')}")
        test_windows = int(test_mask.sum())
        if test_windows != expected.get("test_samples"):
            warnings.append(f"Test windows {test_windows} != expected {expected.get('test_samples')}")

    report = SplitValidationReport(
        passed=len(errors) == 0,
        train_athletes=len(train),
        val_athletes=len(val),
        test_athletes=len(test),
        train_windows=int(train_mask.sum()),
        val_windows=int(val_mask.sum()),
        test_windows=int(test_mask.sum()),
        train_videos=len(train_videos),
        val_videos=len(val_videos),
        test_videos=len(test_videos),
        athlete_overlap=athlete_overlap,
        video_overlap=video_overlap,
        missing_keypoint_videos=missing_keypoints,
        errors=errors,
        warnings=warnings,
    )
    return report


def load_split(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def report_to_markdown(report: SplitValidationReport) -> str:
    status = "PASS" if report.passed else "FAIL"
    lines = [
        "# Split Validation Report",
        "",
        f"**Status:** {status}",
        "",
        "## Counts",
        "",
        f"- Train: {report.train_athletes} athletes, {report.train_videos} videos, {report.train_windows} windows",
        f"- Val: {report.val_athletes} athletes, {report.val_videos} videos, {report.val_windows} windows",
        f"- Test: {report.test_athletes} athletes, {report.test_videos} videos, {report.test_windows} windows",
        "",
    ]
    if report.errors:
        lines.append("## Errors")
        lines.extend(f"- {err}" for err in report.errors)
        lines.append("")
    if report.warnings:
        lines.append("## Warnings")
        lines.extend(f"- {warn}" for warn in report.warnings)
        lines.append("")
    return "\n".join(lines)


def report_to_json(report: SplitValidationReport) -> str:
    return json.dumps(asdict(report), indent=2)
