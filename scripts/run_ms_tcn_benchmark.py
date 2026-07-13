#!/usr/bin/env python3
"""Run the M3 MS-TCN multi-seed benchmark (preflight, train, eval, aggregate)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import yaml

from snatch_phase_bench.benchmark.aggregate_results import aggregate_seed_results
from snatch_phase_bench.benchmark.experiment_metadata import build_protocol_freeze, write_json
from snatch_phase_bench.benchmark.preflight import run_preflight, write_preflight_report
from snatch_phase_bench.benchmark.registry import load_model_experiment_config
from snatch_phase_bench.experiments.config_loader import get_section
from snatch_phase_bench.utils.logging import setup_logging

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SEEDS = [42, 123, 456]


def _run_command(cmd: list[str], *, cwd: Path) -> None:
    print(f"[run] {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run MS-TCN M3 benchmark protocol.")
    parser.add_argument("--config", type=Path, default=Path("configs/benchmark/ms_tcn.yaml"))
    parser.add_argument("--seeds", type=int, nargs="+", default=DEFAULT_SEEDS)
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--skip-train", action="store_true")
    parser.add_argument("--skip-eval", action="store_true")
    parser.add_argument("--skip-aggregate", action="store_true")
    parser.add_argument("--skip-figures", action="store_true")
    parser.add_argument("--skip-failure-analysis", action="store_true")
    parser.add_argument("--seed", type=int, default=None, help="Run a single seed only.")
    args = parser.parse_args()

    setup_logging()
    config = load_model_experiment_config(args.config)
    output_cfg = get_section(config, "output")
    train_cfg = get_section(config, "training")
    early_stop_cfg = train_cfg.get("early_stopping", {})
    base_output = Path(str(output_cfg["checkpoint_dir"]))
    aggregate_dir = base_output / "aggregate"
    aggregate_dir.mkdir(parents=True, exist_ok=True)

    seeds = [args.seed] if args.seed is not None else list(args.seeds)
    monitor = str(early_stop_cfg.get("monitor", "val_segmental_f1_at_50"))

    if not args.skip_preflight:
        report = run_preflight()
        preflight_path = aggregate_dir / "preflight_report.json"
        write_preflight_report(preflight_path, report)
        print(json.dumps({"preflight": str(preflight_path), "passed": report.passed}, indent=2))
        if not report.passed:
            print("Preflight failed. Aborting benchmark run.", file=sys.stderr)
            sys.exit(1)

    protocol = build_protocol_freeze(
        config_path=Path(str(config["config_path"])),
        manifest_path=REPO_ROOT / "configs" / "benchmark.yaml",
        seeds=seeds,
        early_stopping_monitor=monitor,
        repo_root=REPO_ROOT,
    )
    write_json(aggregate_dir / "protocol_freeze.json", protocol)

    benchmark_log: dict[str, object] = {
        "seeds": seeds,
        "started_at": time.time(),
        "seed_runs": {},
    }

    for seed in seeds:
        seed_dir = base_output / f"seed{seed}"
        seed_dir.mkdir(parents=True, exist_ok=True)
        seed_log: dict[str, object] = {"seed": seed}
        train_start = time.perf_counter()

        if not args.skip_train:
            _run_command(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "train_ms_tcn.py"),
                    "--config",
                    str(args.config),
                    "--seed",
                    str(seed),
                ],
                cwd=REPO_ROOT,
            )
            seed_log["train_runtime_seconds"] = time.perf_counter() - train_start

            checkpoint = seed_dir / "best_model.pt"
            if not checkpoint.exists():
                raise FileNotFoundError(f"Missing checkpoint after training: {checkpoint}")

            if not args.skip_eval:
                _run_command(
                    [
                        sys.executable,
                        str(REPO_ROOT / "scripts" / "eval_ms_tcn.py"),
                        "--config",
                        str(args.config),
                        "--checkpoint",
                        str(checkpoint),
                        "--split",
                        "test",
                    ],
                    cwd=REPO_ROOT,
                )
        elif not args.skip_eval:
            checkpoint = seed_dir / "best_model.pt"
            if not checkpoint.exists():
                raise FileNotFoundError(f"Missing checkpoint for eval: {checkpoint}")
            _run_command(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "eval_ms_tcn.py"),
                    "--config",
                    str(args.config),
                    "--checkpoint",
                    str(checkpoint),
                    "--split",
                    "test",
                ],
                cwd=REPO_ROOT,
            )
        benchmark_log["seed_runs"][str(seed)] = seed_log

    if not args.skip_aggregate:
        seed_dirs = {seed: base_output / f"seed{seed}" for seed in seeds}
        aggregated = aggregate_seed_results(seed_dirs, split="test")
        write_json(aggregate_dir / "test_metrics_aggregate.json", aggregated)

        # Lightweight markdown summary for docs (no large artifacts)
        lines = [
            "# MS-TCN M3 aggregate test metrics",
            "",
            f"Seeds: {', '.join(str(s) for s in seeds)}",
            f"Early-stopping monitor: `{monitor}`",
            "",
            "| Metric | Mean | Std | Median | Min | Max |",
            "|--------|------|-----|--------|-----|-----|",
        ]
        for metric, stats in aggregated["aggregate"].items():
            if stats["mean"] is None:
                continue
            lines.append(
                f"| {metric} | {stats['mean']:.4f} | {stats['std']:.4f} | "
                f"{stats['median']:.4f} | {stats['min']:.4f} | {stats['max']:.4f} |"
            )
        (aggregate_dir / "test_metrics_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if not args.skip_failure_analysis:
        _run_command(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "ms_tcn_failure_analysis.py"),
                "--output-dir",
                str(base_output),
                "--seeds",
                *[str(s) for s in seeds],
            ],
            cwd=REPO_ROOT,
        )

    if not args.skip_figures:
        _run_command(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "generate_ms_tcn_figures.py"),
                "--output-dir",
                str(base_output),
                "--seeds",
                *[str(s) for s in seeds],
            ],
            cwd=REPO_ROOT,
        )

    benchmark_log["finished_at"] = time.time()
    write_json(aggregate_dir / "benchmark_run_log.json", benchmark_log)
    print(json.dumps({"aggregate_dir": str(aggregate_dir), "seeds": seeds}, indent=2))


if __name__ == "__main__":
    main()
