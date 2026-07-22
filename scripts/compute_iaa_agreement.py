#!/usr/bin/env python3
"""Compute inter-annotator agreement once annotator2 labels exist.

Refuses to fabricate results: exits non-zero if the IAA subset is incomplete.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from snatch_phase_bench.evaluation.iaa import (
    compute_iaa,
    load_annotator2_directory,
    load_segment_csv,
    render_global_latex_table,
    render_global_markdown_table,
    render_transition_latex_table,
    render_transition_markdown_table,
)


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_videos(segments: pd.DataFrame, required: list[str]) -> list[str]:
    present = set(segments["video_relpath"].astype(str).unique())
    return [vr for vr in required if vr not in present]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=_default_repo_root())
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="IAA subset manifest (default: analysis/iaa/subset_manifest.json)",
    )
    parser.add_argument(
        "--annotator1",
        type=Path,
        default=None,
        help="Primary annotator segment CSV (default: Paper_TFM master_segment_labels.csv)",
    )
    parser.add_argument(
        "--annotator2-dir",
        type=Path,
        default=None,
        help="Directory with annotator2 segment CSVs",
    )
    parser.add_argument("--fps", type=float, default=25.0)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Compute on the intersection only (not for manuscript tables).",
    )
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    manifest_path = args.manifest or (repo / "analysis" / "iaa" / "subset_manifest.json")
    manifest = _load_manifest(manifest_path)
    videos = [item["video_relpath"] for item in manifest["videos"]]

    annotator1_path = args.annotator1 or Path(
        "~/papers/Paper_TFM-main/data/annotations/master_segment_labels.csv"
    ).expanduser()
    annotator2_dir = args.annotator2_dir or (
        repo / "analysis" / "iaa" / "annotator2" / "segments"
    )
    out_dir = repo / "analysis" / "iaa" / "results"
    tables_dir = repo / "analysis" / "iaa" / "tables"

    if not annotator1_path.exists():
        print(f"ERROR: annotator1 CSV not found: {annotator1_path}", file=sys.stderr)
        return 2

    try:
        segments_b = load_annotator2_directory(annotator2_dir)
    except FileNotFoundError as exc:
        print(
            "Annotator-2 labels are not available yet.\n"
            f"Expected CSVs under: {annotator2_dir}\n"
            "See docs/annotation/IAA_PROTOCOL.md — do not invent agreement numbers.\n"
            f"Detail: {exc}",
            file=sys.stderr,
        )
        return 3

    segments_a = load_segment_csv(annotator1_path)
    # Restrict annotator1 to subset rows for clarity.
    segments_a = segments_a[segments_a["video_relpath"].isin(videos)].copy()
    segments_b = segments_b[segments_b["video_relpath"].isin(videos)].copy()

    missing_a = _missing_videos(segments_a, videos)
    missing_b = _missing_videos(segments_b, videos)
    if missing_a:
        print("ERROR: annotator1 missing subset videos:", file=sys.stderr)
        for vr in missing_a:
            print(f"  - {vr}", file=sys.stderr)
        return 4
    if missing_b and not args.allow_partial:
        print(
            "Annotator-2 coverage incomplete; refusing to publish agreement tables.\n"
            "Missing videos:",
            file=sys.stderr,
        )
        for vr in missing_b:
            print(f"  - {vr}", file=sys.stderr)
        print(
            f"\nProgress: {len(videos) - len(missing_b)}/{len(videos)}. "
            "Re-run after all segment CSVs are deposited.",
            file=sys.stderr,
        )
        return 5

    use_videos = [vr for vr in videos if vr not in missing_b]
    result = compute_iaa(segments_a, segments_b, use_videos, fps=args.fps)

    out_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "status": "computed",
        "manifest": str(manifest_path),
        "annotator1": str(annotator1_path),
        "annotator2_dir": str(annotator2_dir),
        "partial": bool(missing_b),
        "videos_used": use_videos,
        "result": result.to_dict(),
        "paired_boundaries": result.paired_rows,
    }
    (out_dir / "iaa_agreement.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    pd.DataFrame(result.paired_rows).to_csv(out_dir / "paired_boundaries.csv", index=False)

    md = "\n".join(
        [
            "# Inter-annotator agreement results",
            "",
            f"**Videos used:** {len(use_videos)} / {len(videos)}",
            f"**Partial run:** {bool(missing_b)}",
            "",
            "## Global agreement",
            "",
            render_global_markdown_table(result),
            "",
            "## Per-transition agreement",
            "",
            render_transition_markdown_table(result),
            "",
        ]
    )
    (out_dir / "IAA_RESULTS.md").write_text(md, encoding="utf-8")
    (tables_dir / "iaa_global.tex").write_text(render_global_latex_table(result), encoding="utf-8")
    (tables_dir / "iaa_per_transition.tex").write_text(
        render_transition_latex_table(result), encoding="utf-8"
    )
    (tables_dir / "iaa_global.md").write_text(render_global_markdown_table(result) + "\n", encoding="utf-8")
    (tables_dir / "iaa_per_transition.md").write_text(
        render_transition_markdown_table(result) + "\n", encoding="utf-8"
    )

    print(f"Wrote {out_dir / 'iaa_agreement.json'}")
    print(f"Wrote publication tables under {tables_dir}")
    if missing_b:
        print("WARNING: partial subset; do not use for manuscript without disclosure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
