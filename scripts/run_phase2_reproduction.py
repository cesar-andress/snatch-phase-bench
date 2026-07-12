#!/usr/bin/env python3
"""Run Phase 2 baseline reproduction pipeline."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from snatch_phase_bench.config import load_config, output_path, resolve_path
from snatch_phase_bench.data.dataset_builder import build_phase_dataset
from snatch_phase_bench.evaluation.checkpoint_eval import evaluate_checkpoint, is_lfs_pointer
from snatch_phase_bench.reproduction.artifact_inventory import (
    artifacts_to_json,
    artifacts_to_markdown,
    inspect_required_artifacts,
)
from snatch_phase_bench.reproduction.dataset_audit import (
    audit_dataset,
    audit_to_json,
    audit_to_markdown,
    compare_arrays,
)
from snatch_phase_bench.reproduction.split_validation import (
    load_split,
    report_to_json as split_to_json,
    report_to_markdown as split_to_markdown,
    validate_split,
)
from snatch_phase_bench.reproduction.temporal_autocorrelation import (
    analyze_temporal_autocorrelation,
    report_to_json as autocorr_to_json,
    report_to_markdown as autocorr_to_markdown,
)
from snatch_phase_bench.training.lstm_trainer import train_lstm_baseline


def record_environment(project_root: Path) -> dict:
    env: dict = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count(),
        "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "packages": {},
    }
    for name in ["numpy", "pandas", "torch", "sklearn", "scipy", "yaml"]:
        try:
            mod = __import__(name if name != "sklearn" else "sklearn")
            env["packages"][name] = getattr(mod, "__version__", "unknown")
        except ImportError:
            env["packages"][name] = "not installed"
    (project_root / "docs/reproduction/reports").mkdir(parents=True, exist_ok=True)
    path = project_root / "docs/reproduction/reports/environment.json"
    path.write_text(json.dumps(env, indent=2), encoding="utf-8")
    return env


def main() -> None:
    config = load_config()
    project_root = Path(config["project_root"])
    snapshot_root = Path(config["snapshot_root"])
    reports_dir = project_root / "docs/reproduction/reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    env = record_environment(project_root)
    print("Environment recorded:", env["python_version"], env["platform"])

    manifest_path = resolve_path(config, "baseline_manifest_json")
    reconstructable = {
        "data/processed/X.npy": "Rebuild from keypoints + master_frame_labels.csv",
        "data/processed/y.npy": "Rebuild from keypoints + master_frame_labels.csv",
        "outputs/lstm_phases/best_model.pt": "Retrain LSTM with original hyperparameters",
        "models/pose_landmarker_full.task": "Not required for keypoint-based reproduction",
    }
    artifacts = inspect_required_artifacts(
        snapshot_root,
        manifest_path,
        [
            "data/processed/X.npy",
            "data/processed/y.npy",
            "outputs/lstm_phases/best_model.pt",
            "models/pose_landmarker_full.task",
        ],
        reconstructable=reconstructable,
    )
    (project_root / "docs/reproduction/artifact_inventory.md").write_text(
        artifacts_to_markdown(artifacts), encoding="utf-8"
    )
    (reports_dir / "artifact_inventory.json").write_text(artifacts_to_json(artifacts), encoding="utf-8")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    meta_manifest = next(
        (a for a in manifest.get("artifacts", []) if a["path"] == "data/processed/meta.csv"),
        None,
    )

    baseline_meta = resolve_path(config, "baseline_meta_csv")
    meta_df = pd.read_csv(baseline_meta)
    split = load_split(resolve_path(config, "athlete_split_json"))
    keypoints_dir = resolve_path(config, "keypoints_dir")

    audit = audit_dataset(
        labels_csv=resolve_path(config, "labels_csv"),
        keypoints_dir=keypoints_dir,
        segment_labels_dir=snapshot_root / "data/annotations/segment_labels",
        baseline_meta_csv=baseline_meta,
        manifest_meta=meta_manifest,
        window_size=config["dataset"]["window_size"],
        stride=config["dataset"]["stride"],
    )
    (reports_dir / "dataset_audit.json").write_text(audit_to_json(audit), encoding="utf-8")
    (reports_dir / "dataset_audit.md").write_text(audit_to_markdown(audit), encoding="utf-8")

    split_report = validate_split(
        meta_df,
        split,
        keypoints_dir=keypoints_dir,
        expected=config.get("expected"),
    )
    (reports_dir / "split_validation.json").write_text(split_to_json(split_report), encoding="utf-8")
    (reports_dir / "split_validation.md").write_text(split_to_markdown(split_report), encoding="utf-8")
    if not split_report.passed:
        raise RuntimeError("Split validation failed.")

    processed_dir = output_path(config, "processed_dir")
    t0 = time.perf_counter()
    build_result = build_phase_dataset(
        labels_csv=resolve_path(config, "labels_csv"),
        keypoints_dir=keypoints_dir,
        output_dir=processed_dir,
        window_size=config["dataset"]["window_size"],
        stride=config["dataset"]["stride"],
        use_z=config["dataset"]["use_z"],
        use_visibility=config["dataset"]["use_visibility"],
        drop_unlabeled=config["dataset"]["drop_unlabeled"],
    )
    rebuild_seconds = time.perf_counter() - t0
    rebuilt_meta = pd.read_csv(processed_dir / "meta.csv")

    rebuild_audit = audit_dataset(
        labels_csv=resolve_path(config, "labels_csv"),
        keypoints_dir=keypoints_dir,
        segment_labels_dir=snapshot_root / "data/annotations/segment_labels",
        baseline_meta_csv=baseline_meta,
        manifest_meta=meta_manifest,
        rebuilt_meta_csv=processed_dir / "meta.csv",
        rebuilt_X_path=processed_dir / "X.npy",
        window_size=config["dataset"]["window_size"],
        stride=config["dataset"]["stride"],
    )
    (reports_dir / "rebuild_audit.json").write_text(audit_to_json(rebuild_audit), encoding="utf-8")

    meta_matches = meta_df.equals(rebuilt_meta)
    y_matches = False
    y_detail = "baseline y.npy unavailable (LFS pointer)"
    if not is_lfs_pointer(resolve_path(config, "baseline_y_npy")):
        y_matches, y_detail = compare_arrays(
            resolve_path(config, "baseline_y_npy"), processed_dir / "y.npy"
        )
    x_matches = False
    x_detail = "baseline X.npy unavailable (LFS pointer)"
    if not is_lfs_pointer(resolve_path(config, "baseline_X_npy")):
        x_matches, x_detail = compare_arrays(
            resolve_path(config, "baseline_X_npy"), processed_dir / "X.npy"
        )

    autocorr = analyze_temporal_autocorrelation(
        rebuilt_meta,
        window_size=config["dataset"]["window_size"],
        stride=config["dataset"]["stride"],
    )
    (project_root / "docs/reproduction/temporal_autocorrelation.md").write_text(
        autocorr_to_markdown(autocorr), encoding="utf-8"
    )
    (reports_dir / "temporal_autocorrelation.json").write_text(
        autocorr_to_json(autocorr), encoding="utf-8"
    )

    thesis_report = json.loads(resolve_path(config, "baseline_report_json").read_text(encoding="utf-8"))
    results: dict = {
        "rebuild": {
            **build_result,
            "runtime_seconds": rebuild_seconds,
            "meta_csv_matches_baseline": bool(meta_matches),
            "X_matches_baseline": x_matches,
            "X_compare_detail": x_detail,
            "y_matches_baseline": y_matches,
            "y_compare_detail": y_detail,
        },
        "checkpoint_evaluation": None,
        "retraining": None,
    }

    checkpoint_path = resolve_path(config, "baseline_checkpoint")
    eval_dir = output_path(config, "baseline_eval_dir")
    eval_dir.mkdir(parents=True, exist_ok=True)

    if not is_lfs_pointer(checkpoint_path) and not is_lfs_pointer(processed_dir / "X.npy"):
        ckpt_eval = evaluate_checkpoint(
            data_dir=processed_dir,
            checkpoint_path=checkpoint_path,
            split_json=resolve_path(config, "athlete_split_json"),
            device="cpu",
            baseline_report_json=resolve_path(config, "baseline_report_json"),
        )
        results["checkpoint_evaluation"] = ckpt_eval
        (eval_dir / "checkpoint_evaluation.json").write_text(json.dumps(ckpt_eval, indent=2), encoding="utf-8")
    else:
        print("Checkpoint or baseline X unavailable — running LSTM retraining reproduction.")
        train_cfg = config["training"]
        retrain_dir = output_path(config, "retrain_dir")
        retrain_result = train_lstm_baseline(
            data_dir=processed_dir,
            output_dir=retrain_dir,
            split_json=resolve_path(config, "athlete_split_json"),
            seed=train_cfg["seed"],
            batch_size=train_cfg["batch_size"],
            epochs=train_cfg["epochs"],
            learning_rate=train_cfg["learning_rate"],
            weight_decay=train_cfg["weight_decay"],
            hidden_size=train_cfg["hidden_size"],
            num_layers=train_cfg["num_layers"],
            dropout=train_cfg["dropout"],
            patience=train_cfg["patience"],
            device="auto",
        )
        results["retraining"] = retrain_result
        (retrain_dir / "retraining_summary.json").write_text(
            json.dumps(retrain_result, indent=2), encoding="utf-8"
        )

    # Comparison table
    reproduced = results.get("checkpoint_evaluation") or results.get("retraining") or {}
    rep_report = reproduced.get("classification_report", thesis_report)
    comparison_rows = []
    metrics = [
        ("accuracy", None, "accuracy"),
        ("macro_precision", "macro avg", "precision"),
        ("macro_recall", "macro avg", "recall"),
        ("macro_f1", "macro avg", "f1-score"),
        ("weighted_f1", "weighted avg", "f1-score"),
        ("test_samples", None, None),
    ]
    for label, section, key in metrics:
        if label == "test_samples":
            thesis_val = thesis_report.get("macro avg", {}).get("support")
            repro_val = reproduced.get("test_samples")
        elif section:
            thesis_val = thesis_report[section][key]
            repro_val = rep_report[section][key] if section in rep_report else None
        else:
            thesis_val = thesis_report.get(key)
            repro_val = rep_report.get(key) if isinstance(rep_report, dict) else None
        diff = None
        status = "not_run"
        if thesis_val is not None and repro_val is not None:
            diff = float(repro_val) - float(thesis_val)
            status = "exact" if reproduced.get("mode") == "checkpoint_evaluation" and reproduced.get("matches_saved_report") else "approximate"
        comparison_rows.append(
            {
                "metric": label,
                "thesis": thesis_val,
                "reproduced": repro_val,
                "absolute_difference": diff,
                "status": status,
            }
        )

    per_class = []
    for phase in ["setup", "first_pull", "transition", "second_pull", "turnover", "catch", "recovery"]:
        if phase in thesis_report and phase in rep_report:
            per_class.append(
                {
                    "phase": phase,
                    "thesis_f1": thesis_report[phase]["f1-score"],
                    "reproduced_f1": rep_report[phase]["f1-score"],
                    "absolute_difference": float(rep_report[phase]["f1-score"]) - float(thesis_report[phase]["f1-score"]),
                }
            )

    comparison = {
        "reproduction_mode": reproduced.get("mode", "none"),
        "global_metrics": comparison_rows,
        "per_class_f1": per_class,
        "confusion_matrix_shape": reproduced.get("confusion_matrix_shape"),
    }
    (reports_dir / "metrics_comparison.json").write_text(json.dumps(comparison, indent=2), encoding="utf-8")

    summary_lines = [
        "# Reproduction Summary",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Modes",
        f"- Checkpoint evaluation: {'yes' if results['checkpoint_evaluation'] else 'no (LFS pointer or missing data)'}",
        f"- Retraining reproduction: {'yes' if results['retraining'] else 'no'}",
        "",
        "## Dataset rebuild",
        f"- Runtime (s): {rebuild_seconds:.2f}",
        f"- Rebuilt shape: {build_result['X_shape']}",
        f"- meta.csv matches baseline: {meta_matches}",
        f"- X.npy matches baseline: {x_matches} ({x_detail})",
        f"- y.npy matches baseline: {y_matches} ({y_detail})",
        "",
        "## Metrics comparison",
        "",
        "| Metric | Thesis | Reproduced | Diff | Status |",
        "|--------|--------|------------|------|--------|",
    ]
    for row in comparison_rows:
        summary_lines.append(
            f"| {row['metric']} | {row['thesis']} | {row['reproduced']} | {row['absolute_difference']} | {row['status']} |"
        )
    (project_root / "docs/reproduction/REPRODUCTION_SUMMARY.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )
    (reports_dir / "phase2_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
