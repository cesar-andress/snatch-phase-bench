#!/usr/bin/env python3
"""Prepare the annotator-2 work package (video list + blank segment templates).

Does NOT copy ground-truth labels into the work package.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from snatch_phase_bench.evaluation.iaa import SEGMENT_COLUMNS


HEADER = ",".join(SEGMENT_COLUMNS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--raw-videos",
        type=Path,
        default=Path("/home/cesar/papers/snatch-phase-bench/raw_videos"),
    )
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    manifest_path = args.manifest or (repo / "analysis" / "iaa" / "subset_manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out = repo / "analysis" / "iaa" / "annotator2_workpack"
    templates = out / "blank_segment_templates"
    out.mkdir(parents=True, exist_ok=True)
    templates.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Annotator-2 work package",
        "",
        "Annotate ONLY the videos listed below.",
        "Do NOT open or request existing SnatchPhaseBench labels.",
        "Deposit finished CSVs under analysis/iaa/annotator2/segments/",
        "using the same relative path layout as blank_segment_templates/.",
        "",
        f"Raw video root (read-only): {args.raw_videos}",
        "",
        "| # | video_relpath | athlete | weight | outcome | tip |",
        "|--:|---------------|---------|--------|---------|-----|",
    ]
    list_paths: list[str] = []
    for i, item in enumerate(manifest["videos"], start=1):
        vr = item["video_relpath"]
        list_paths.append(vr)
        tip = item["difficulty"]
        lines.append(
            f"| {i} | `{vr}` | {item['athlete']} | {item['weight_class']} | "
            f"{item['outcome']} | {tip} |"
        )
        dest = templates / Path(vr).with_suffix(".csv")
        dest.parent.mkdir(parents=True, exist_ok=True)
        video_name = Path(vr).name
        # Header-only template; annotator fills rows.
        dest.write_text(HEADER + "\n", encoding="utf-8")
        # Also write a one-line README hint beside each athlete folder once.
        readme = dest.parent / "README.txt"
        if not readme.exists():
            readme.write_text(
                "Fill the CSV with inclusive [start_frame, end_frame] segments.\n"
                "Columns: video,video_relpath,start_frame,end_frame,phase_id,phase_name\n"
                f"Example video column value: {video_name}\n"
                f"Example video_relpath: {vr}\n",
                encoding="utf-8",
            )

    (out / "VIDEO_LIST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "VIDEO_LIST.txt").write_text("\n".join(list_paths) + "\n", encoding="utf-8")
    (out / "INSTRUCTIONS_SHORT.txt").write_text(
        "\n".join(
            [
                "1. Read docs/annotation/IAA_PROTOCOL.md (sections 2–3).",
                "2. Open each video under the raw_videos root listed in VIDEO_LIST.md.",
                "3. Fill blank_segment_templates/*.csv (inclusive frame intervals).",
                "4. Copy completed files to analysis/iaa/annotator2/segments/ mirroring paths.",
                "5. Do not look at annotator-1 labels or model predictions.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Work package written to {out}")


if __name__ == "__main__":
    main()
