#!/usr/bin/env python3
"""Single entry point for the SnatchPhaseBench inter-annotator agreement pipeline.

Default behaviour:
  - If annotator-2 labels are incomplete: print status and exit non-zero
    without writing fabricated statistics.
  - If complete: load both annotations, align videos/boundaries, compute
    agreement, and write all publication tables and figures.

Usage:
  python scripts/run_iaa_pipeline.py              # full run or status refusal
  python scripts/run_iaa_pipeline.py --status     # readiness only
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from snatch_phase_bench.evaluation.iaa_pipeline import (
    Annotator2IncompleteError,
    PipelinePaths,
    assess_status,
    run_pipeline,
)


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=_default_repo_root())
    parser.add_argument("--annotator1", type=Path, default=None)
    parser.add_argument("--annotator2-dir", type=Path, default=None)
    parser.add_argument("--fps", type=float, default=25.0)
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print readiness JSON and exit (never fabricates results).",
    )
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Allow incomplete annotator-2 coverage (not for manuscript).",
    )
    args = parser.parse_args()

    paths = PipelinePaths.from_repo(
        args.repo_root.resolve(),
        annotator1=args.annotator1,
        annotator2_dir=args.annotator2_dir,
    )
    status = assess_status(paths)

    if args.status:
        print(json.dumps(status.to_dict(), indent=2))
        return 0 if status.ready else 1

    if not status.ready and not args.allow_partial:
        print("IAA pipeline not ready — refusing to invent agreement statistics.", file=sys.stderr)
        for msg in status.messages:
            print(f"  • {msg}", file=sys.stderr)
        if status.missing_annotator2:
            print("\nMissing annotator-2 videos:", file=sys.stderr)
            for vr in status.missing_annotator2:
                print(f"  - {vr}", file=sys.stderr)
        print(
            "\nWhen labels are deposited under "
            f"{paths.annotator2_dir}, re-run:\n"
            "  python scripts/run_iaa_pipeline.py\n"
            "See docs/annotation/IAA_PIPELINE.md",
            file=sys.stderr,
        )
        # Persist status snapshot (no numeric agreement claims).
        paths.results_dir.mkdir(parents=True, exist_ok=True)
        (paths.results_dir / "pipeline_status.json").write_text(
            json.dumps(status.to_dict(), indent=2) + "\n", encoding="utf-8"
        )
        return 3

    try:
        artifacts = run_pipeline(
            paths,
            fps=args.fps,
            allow_partial=args.allow_partial,
        )
    except Annotator2IncompleteError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Videos used: {len(artifacts.videos_used)}")
    print(f"Paired boundaries: {len(artifacts.result.paired_rows)}")
    print(f"Wrote {artifacts.results_md}")
    print(f"Wrote {len(artifacts.table_paths)} table files under {paths.tables_dir}")
    print(f"Wrote {len(artifacts.figure_paths)} figure files under {paths.figures_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
