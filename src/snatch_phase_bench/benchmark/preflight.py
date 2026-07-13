"""Data-integrity preflight checks before MS-TCN benchmark training."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from snatch_phase_bench.config import load_config, resolve_path
from snatch_phase_bench.data.frame_sequence import (
    FrameSequenceRecord,
    load_frame_sequences,
    summarize_frame_sequences,
)
from snatch_phase_bench.data.splits import load_athlete_split
from snatch_phase_bench.ontology.loader import load_benchmark_manifest


PREFLIGHT_VERSION = "1.0.0"


@dataclass
class PreflightCheck:
    name: str
    passed: bool
    details: dict[str, Any] = field(default_factory=dict)
    message: str = ""


@dataclass
class PreflightReport:
    version: str
    created_at: str
    passed: bool
    checks: list[PreflightCheck]
    summary: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "created_at": self.created_at,
            "passed": self.passed,
            "checks": [asdict(c) for c in self.checks],
            "summary": self.summary,
            "warnings": self.warnings,
        }


def _resolve_paths() -> tuple[Path, Path, Path]:
    reproduction = load_config()
    labels_csv = resolve_path(reproduction, "labels_csv")
    keypoints_dir = resolve_path(reproduction, "keypoints_dir")
    split_json = resolve_path(reproduction, "athlete_split_json")
    return labels_csv, keypoints_dir, split_json


def run_preflight(*, use_z: bool = True) -> PreflightReport:
    """Run all integrity checks. Raises nothing; inspect ``report.passed``."""
    labels_csv, keypoints_dir, split_json = _resolve_paths()
    manifest = load_benchmark_manifest()
    split = load_athlete_split(split_json)
    ignore_label_id = 0

    checks: list[PreflightCheck] = []
    warnings: list[str] = []

    expected_videos = int(manifest["dataset"]["videos"])
    all_records = load_frame_sequences(
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
        use_z=use_z,
        athlete_split=split,
        split_filter="all",
    )

    # 1. All dense sequences present
    check1 = PreflightCheck(
        name="dense_sequences_count",
        passed=len(all_records) == expected_videos,
        details={"expected_videos": expected_videos, "loaded_videos": len(all_records)},
        message=f"Expected {expected_videos} videos, loaded {len(all_records)}",
    )
    checks.append(check1)

    # 2. Label/keypoint alignment (frame index continuity + equal length)
    alignment_failures: list[str] = []
    for record in all_records:
        if record.num_frames == 0:
            alignment_failures.append(f"{record.video_relpath}: empty sequence")
            continue
        if not np.array_equal(record.frames, np.arange(record.frames[0], record.frames[0] + len(record.frames))):
            alignment_failures.append(f"{record.video_relpath}: non-contiguous frame indices")
        if len(record.frames) != len(record.phase_ids):
            alignment_failures.append(f"{record.video_relpath}: frame/label length mismatch")
        if record.features.shape[0] != len(record.frames):
            alignment_failures.append(f"{record.video_relpath}: feature/label length mismatch")
    checks.append(
        PreflightCheck(
            name="label_keypoint_alignment",
            passed=len(alignment_failures) == 0,
            details={"failures": alignment_failures[:20], "failure_count": len(alignment_failures)},
            message="All labels align with keypoint frames" if not alignment_failures else f"{len(alignment_failures)} alignment failures",
        )
    )

    # 3–4. Split integrity: no test athlete in train/val
    train_athletes = set(split.train_athletes)
    val_athletes = set(split.val_athletes)
    test_athletes = set(split.test_athletes)
    overlap_tv = train_athletes & val_athletes
    overlap_tt = train_athletes & test_athletes
    overlap_vt = val_athletes & test_athletes
    split_ok = not overlap_tv and not overlap_tt and not overlap_vt
    checks.append(
        PreflightCheck(
            name="athlete_split_disjoint",
            passed=split_ok,
            details={
                "train_athletes": len(train_athletes),
                "val_athletes": len(val_athletes),
                "test_athletes": len(test_athletes),
                "overlap_train_val": sorted(overlap_tv),
                "overlap_train_test": sorted(overlap_tt),
                "overlap_val_test": sorted(overlap_vt),
            },
            message="Athlete splits are disjoint" if split_ok else "Athlete overlap detected across splits",
        )
    )

    split_mismatches: list[str] = []
    for record in all_records:
        athlete = record.athlete_id
        partition = split.partition_for_athlete(athlete)
        if partition == "train" and athlete not in train_athletes:
            split_mismatches.append(f"{record.video_relpath}: athlete {athlete} not in train list")
        if partition == "val" and athlete not in val_athletes:
            split_mismatches.append(f"{record.video_relpath}: athlete {athlete} not in val list")
        if partition == "test" and athlete not in test_athletes:
            split_mismatches.append(f"{record.video_relpath}: athlete {athlete} not in test list")
    checks.append(
        PreflightCheck(
            name="video_split_assignment",
            passed=len(split_mismatches) == 0,
            details={"mismatches": split_mismatches[:20], "mismatch_count": len(split_mismatches)},
            message="All videos assigned to correct split" if not split_mismatches else f"{len(split_mismatches)} split mismatches",
        )
    )

    # 5. Ignored-label handling
    unlabeled_counts = {
        record.video_relpath: int(np.sum(record.phase_ids == ignore_label_id))
        for record in all_records
    }
    total_unlabeled = sum(unlabeled_counts.values())
    checks.append(
        PreflightCheck(
            name="ignored_label_handling",
            passed=True,
            details={
                "ignore_label_id": ignore_label_id,
                "total_unlabeled_frames": total_unlabeled,
                "videos_with_unlabeled": sum(1 for c in unlabeled_counts.values() if c > 0),
            },
            message=f"{total_unlabeled} unlabeled frames across dataset (expected utility class)",
        )
    )

    # 6. Sequence-length distribution
    lengths = [record.num_frames for record in all_records]
    length_stats = {
        "min": int(min(lengths)) if lengths else 0,
        "max": int(max(lengths)) if lengths else 0,
        "mean": float(np.mean(lengths)) if lengths else 0.0,
        "median": float(np.median(lengths)) if lengths else 0.0,
        "std": float(np.std(lengths)) if lengths else 0.0,
        "p05": float(np.percentile(lengths, 5)) if lengths else 0.0,
        "p95": float(np.percentile(lengths, 95)) if lengths else 0.0,
    }
    checks.append(
        PreflightCheck(
            name="sequence_length_distribution",
            passed=length_stats["min"] > 0,
            details=length_stats,
            message=f"Sequence lengths: min={length_stats['min']}, max={length_stats['max']}, median={length_stats['median']:.1f}",
        )
    )

    # 7. No empty sequences
    empty = [r.video_relpath for r in all_records if r.num_frames == 0]
    checks.append(
        PreflightCheck(
            name="no_empty_sequences",
            passed=len(empty) == 0,
            details={"empty_videos": empty},
            message="No empty sequences" if not empty else f"{len(empty)} empty sequences",
        )
    )

    # 8. No NaN/Inf after loading (pre-standardization)
    nan_videos: list[str] = []
    inf_videos: list[str] = []
    for record in all_records:
        if np.isnan(record.features).any():
            nan_videos.append(record.video_relpath)
        if np.isinf(record.features).any():
            inf_videos.append(record.video_relpath)
    checks.append(
        PreflightCheck(
            name="no_nan_inf_features",
            passed=len(nan_videos) == 0 and len(inf_videos) == 0,
            details={"nan_videos": nan_videos[:20], "inf_videos": inf_videos[:20]},
            message="Features are finite" if not nan_videos and not inf_videos else "NaN/Inf detected in features",
        )
    )

    by_split = {
        name: summarize_frame_sequences(
            load_frame_sequences(
                labels_csv=labels_csv,
                keypoints_dir=keypoints_dir,
                use_z=use_z,
                athlete_split=split,
                split_filter=name,  # type: ignore[arg-type]
            )
        )
        for name in ("train", "val", "test")
    }

    passed = all(c.passed for c in checks)
    return PreflightReport(
        version=PREFLIGHT_VERSION,
        created_at=datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
        passed=passed,
        checks=checks,
        summary={
            "dataset_version": manifest["dataset"]["version"],
            "split_version": manifest["split"]["version"],
            "ontology": manifest["ontology"]["canonical"],
            "evaluator_version": manifest["evaluation"]["version"],
            "total_records": len(all_records),
            "by_split": by_split,
        },
        warnings=warnings,
    )


def write_preflight_report(path: Path, report: PreflightReport) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
