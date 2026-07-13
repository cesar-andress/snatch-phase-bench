#!/usr/bin/env python3
"""Aggregate MS-TCN multi-seed test results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from snatch_phase_bench.benchmark.aggregate_results import aggregate_seed_results
from snatch_phase_bench.benchmark.experiment_metadata import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate MS-TCN seed results.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/benchmark/ms_tcn"))
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    parser.add_argument("--split", default="test")
    args = parser.parse_args()

    seed_dirs = {seed: args.output_dir / f"seed{seed}" for seed in args.seeds}
    aggregated = aggregate_seed_results(seed_dirs, split=args.split)
    out_path = args.output_dir / "aggregate" / f"{args.split}_metrics_aggregate.json"
    write_json(out_path, aggregated)
    print(json.dumps({"output": str(out_path), "aggregate": aggregated["aggregate"]}, indent=2))


if __name__ == "__main__":
    main()
