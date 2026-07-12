"""Dataset verification and comparison utilities."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class DatasetAuditReport:
    keypoint_files: int
    annotation_frame_rows: int
    annotation_videos: int
    segment_label_files: int
    meta_rows: int | None
    meta_videos: int | None
    meta_athletes: int | None
    rebuilt_samples: int | None
    rebuilt_shape: list[int] | None
    window_size: int
    stride: int
    num_classes_labeled: int
    class_distribution: dict[str, int]
    space_filename_keypoints: list[str]
    baseline_meta_bytes: int | None
    baseline_meta_sha256: str | None
    manifest_meta_bytes: int | None
    manifest_meta_sha256: str | None
    meta_size_discrepancy_bytes: int | None
    warnings: list[str]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_files(root: Path, pattern: str) -> list[Path]:
    return sorted(root.rglob(pattern)) if root.exists() else []


def audit_dataset(
    *,
    labels_csv: Path,
    keypoints_dir: Path,
    segment_labels_dir: Path | None,
    baseline_meta_csv: Path | None,
    manifest_meta: dict[str, Any] | None,
    rebuilt_meta_csv: Path | None = None,
    rebuilt_X_path: Path | None = None,
    window_size: int = 31,
    stride: int = 1,
) -> DatasetAuditReport:
    warnings: list[str] = []

    labels = pd.read_csv(labels_csv)
    keypoint_files = count_files(keypoints_dir, "*.csv")
    space_files = [str(p.relative_to(keypoints_dir)) for p in keypoint_files if p.name.endswith(" .csv")]

    segment_count = len(count_files(segment_labels_dir, "*.csv")) if segment_labels_dir else 0

    class_distribution: dict[str, int] = {}
    meta_rows = meta_videos = meta_athletes = None

    source_meta = rebuilt_meta_csv if rebuilt_meta_csv and rebuilt_meta_csv.exists() else baseline_meta_csv
    if source_meta and source_meta.exists():
        meta_df = pd.read_csv(source_meta)
        meta_rows = len(meta_df)
        meta_videos = int(meta_df["video_relpath"].nunique())
        meta_athletes = int(meta_df["athlete"].nunique())
        if "phase_name" in meta_df.columns:
            class_distribution = meta_df["phase_name"].value_counts().astype(int).to_dict()

    baseline_meta_bytes = baseline_meta_sha = None
    manifest_meta_bytes = manifest_meta_sha = None
    meta_size_discrepancy = None

    if baseline_meta_csv and baseline_meta_csv.exists():
        baseline_meta_bytes = baseline_meta_csv.stat().st_size
        baseline_meta_sha = sha256_file(baseline_meta_csv)
    if manifest_meta:
        manifest_meta_bytes = manifest_meta.get("size_bytes")
        manifest_meta_sha = manifest_meta.get("sha256")
        if baseline_meta_bytes and manifest_meta_bytes:
            meta_size_discrepancy = int(manifest_meta_bytes) - baseline_meta_bytes
            if meta_size_discrepancy != 0:
                warnings.append(
                    f"baseline meta.csv size differs from manifest by {meta_size_discrepancy} bytes"
                )
        if baseline_meta_sha and manifest_meta_sha and baseline_meta_sha != manifest_meta_sha:
            warnings.append("baseline meta.csv SHA-256 differs from manifest entry")

    rebuilt_samples = rebuilt_shape = None
    if rebuilt_X_path and rebuilt_X_path.exists():
        X = np.load(rebuilt_X_path, mmap_mode="r")
        rebuilt_shape = list(X.shape)
        rebuilt_samples = int(X.shape[0])

    labeled_classes = labels[labels["phase_id"] > 0]["phase_name"].nunique() if "phase_id" in labels else 0

    if space_files:
        warnings.append(
            f"{len(space_files)} keypoint files contain a space before .csv; "
            "labels use matching spaced .mp4 paths — rebuild should still resolve them."
        )

    return DatasetAuditReport(
        keypoint_files=len(keypoint_files),
        annotation_frame_rows=len(labels),
        annotation_videos=int(labels["video_relpath"].nunique()),
        segment_label_files=segment_count,
        meta_rows=meta_rows,
        meta_videos=meta_videos,
        meta_athletes=meta_athletes,
        rebuilt_samples=rebuilt_samples,
        rebuilt_shape=rebuilt_shape,
        window_size=window_size,
        stride=stride,
        num_classes_labeled=int(labeled_classes),
        class_distribution=class_distribution,
        space_filename_keypoints=space_files,
        baseline_meta_bytes=baseline_meta_bytes,
        baseline_meta_sha256=baseline_meta_sha,
        manifest_meta_bytes=manifest_meta_bytes,
        manifest_meta_sha256=manifest_meta_sha,
        meta_size_discrepancy_bytes=meta_size_discrepancy,
        warnings=warnings,
    )


def compare_arrays(path_a: Path, path_b: Path, chunk_size: int = 1024) -> tuple[bool, str]:
    if not path_a.exists() or not path_b.exists():
        return False, "one or both files missing"
    a = np.load(path_a, mmap_mode="r")
    b = np.load(path_b, mmap_mode="r")
    if a.shape != b.shape or a.dtype != b.dtype:
        return False, f"shape/dtype mismatch {a.shape}/{a.dtype} vs {b.shape}/{b.dtype}"
    for start in range(0, len(a), chunk_size):
        end = min(start + chunk_size, len(a))
        if not np.array_equal(a[start:end], b[start:end]):
            return False, f"values differ at samples {start}:{end}"
    return True, f"exact match {a.shape} {a.dtype}"


def audit_to_markdown(report: DatasetAuditReport) -> str:
    lines = [
        "# Dataset Audit Report",
        "",
        "## File counts",
        f"- Keypoint CSV files: {report.keypoint_files}",
        f"- Frame annotation rows: {report.annotation_frame_rows}",
        f"- Annotated videos: {report.annotation_videos}",
        f"- Segment label files: {report.segment_label_files}",
        "",
        "## Processed dataset",
        f"- Meta rows: {report.meta_rows}",
        f"- Meta videos: {report.meta_videos}",
        f"- Meta athletes: {report.meta_athletes}",
        f"- Window size: {report.window_size}",
        f"- Stride: {report.stride}",
        f"- Rebuilt samples: {report.rebuilt_samples}",
        f"- Rebuilt X shape: {report.rebuilt_shape}",
        "",
        "## meta.csv vs manifest",
        f"- Baseline meta bytes: {report.baseline_meta_bytes}",
        f"- Manifest expected bytes: {report.manifest_meta_bytes}",
        f"- Discrepancy: {report.meta_size_discrepancy_bytes}",
        f"- Baseline SHA-256: {report.baseline_meta_sha256}",
        f"- Manifest SHA-256: {report.manifest_meta_sha256}",
        "",
        "## Class distribution (processed meta)",
    ]
    for name, count in sorted(report.class_distribution.items()):
        lines.append(f"- {name}: {count}")
    if report.space_filename_keypoints:
        lines.extend(["", "## Filenames with space before .csv"])
        for name in report.space_filename_keypoints:
            lines.append(f"- `{name}`")
    if report.warnings:
        lines.extend(["", "## Warnings"])
        lines.extend(f"- {w}" for w in report.warnings)
    return "\n".join(lines) + "\n"


def audit_to_json(report: DatasetAuditReport) -> str:
    import json

    return json.dumps(asdict(report), indent=2)
