#!/usr/bin/env python3
"""First-pass ASFormer benchmark failure analysis across seeds."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from snatch_phase_bench.benchmark.experiment_metadata import write_json


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def analyze_seed(seed_dir: Path) -> dict:
    eval_payload = _load(seed_dir / "eval_test.json")
    predictions = _load(seed_dir / "predictions_test.json")

    per_class_recall = eval_payload.get("per_class_recall", {})
    lowest_recall = sorted(per_class_recall.items(), key=lambda item: item[1])[:3]

    transition_mae: list[tuple[str, float]] = []
    for key, payload in eval_payload.get("per_transition", {}).items():
        mae = payload.get("boundary_mae_frames_macro_over_videos")
        if mae is not None:
            transition_mae.append((key, float(mae)))
    transition_mae.sort(key=lambda item: item[1], reverse=True)

    over_segmentation = 0
    missing_short_phases = 0
    extra_fragments = 0
    length_effects: list[dict] = []

    for video in predictions["videos"]:
        gt = video["y_true"]
        pred = video["y_pred"]
        gt_segments = _count_segments(gt)
        pred_segments = _count_segments(pred)
        if pred_segments > gt_segments + 2:
            over_segmentation += 1
        if pred_segments > gt_segments:
            extra_fragments += pred_segments - gt_segments
        if gt_segments >= 5 and pred_segments < gt_segments - 1:
            missing_short_phases += 1
        length_effects.append(
            {
                "video_relpath": video["video_relpath"],
                "num_frames": video["num_frames"],
                "gt_segments": gt_segments,
                "pred_segments": pred_segments,
                "segment_delta": pred_segments - gt_segments,
            }
        )

    length_effects.sort(key=lambda item: abs(item["segment_delta"]), reverse=True)

    return {
        "lowest_recall_classes": lowest_recall,
        "highest_boundary_error_transitions": transition_mae[:5],
        "over_segmentation_videos": over_segmentation,
        "missing_short_phase_videos": missing_short_phases,
        "total_extra_fragments": extra_fragments,
        "top_length_effects": length_effects[:10],
        "edit_score": eval_payload.get("aggregate", {}).get("segment_macro_over_videos", {}).get("edit_score"),
    }


def _count_segments(labels: list[int]) -> int:
    if not labels:
        return 0
    segments = 1
    for idx in range(1, len(labels)):
        if labels[idx] != labels[idx - 1]:
            segments += 1
    return segments


def compare_seed_disagreement(output_dir: Path, seeds: list[int]) -> dict:
    """Videos where predicted class sequences differ across seeds."""
    by_video: dict[str, list[str]] = defaultdict(list)
    for seed in seeds:
        seed_dir = output_dir / f"seed{seed}"
        payload = _load(seed_dir / "predictions_test.json")
        for video in payload["videos"]:
            signature = _phase_signature(video["y_pred"])
            by_video[video["video_relpath"]].append(signature)

    unstable = []
    for video, signatures in by_video.items():
        if len(set(signatures)) > 1:
            unstable.append({"video_relpath": video, "signatures": signatures})
    unstable.sort(key=lambda item: len(set(item["signatures"])), reverse=True)
    return {
        "unstable_video_count": len(unstable),
        "examples": unstable[:15],
    }


def _phase_signature(labels: list[int]) -> str:
    segments: list[str] = []
    if not labels:
        return ""
    current = labels[0]
    length = 1
    for label in labels[1:]:
        if label == current:
            length += 1
        else:
            segments.append(f"{current}:{length}")
            current = label
            length = 1
    segments.append(f"{current}:{length}")
    return "|".join(segments)


def main() -> None:
    parser = argparse.ArgumentParser(description="ASFormer failure analysis.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/benchmark/asformer"))
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    args = parser.parse_args()

    per_seed = {str(seed): analyze_seed(args.output_dir / f"seed{seed}") for seed in args.seeds}
    disagreement = compare_seed_disagreement(args.output_dir, args.seeds)

    edit_scores = [payload["edit_score"] for payload in per_seed.values() if payload.get("edit_score") is not None]
    report = {
        "seeds": args.seeds,
        "per_seed": per_seed,
        "cross_seed_disagreement": disagreement,
        "edit_score_mean": float(mean(edit_scores)) if edit_scores else None,
        "notes": [
            "Boundary errors are reported from canonical evaluator per-transition aggregates.",
            "Over-segmentation proxy: predicted contiguous segments exceed GT by >2.",
            "Causal interpretation requires qualitative review; this is a first-pass diagnostic.",
        ],
    }
    out_path = args.output_dir / "aggregate" / "failure_analysis.json"
    write_json(out_path, report)
    (args.output_dir / "aggregate" / "failure_analysis.md").write_text(
        _render_markdown(report),
        encoding="utf-8",
    )
    print(json.dumps({"output": str(out_path)}, indent=2))


def _render_markdown(report: dict) -> str:
    lines = ["# ASFormer failure analysis (B3)", ""]
    for seed, payload in report["per_seed"].items():
        lines.append(f"## Seed {seed}")
        lines.append(f"- Over-segmentation videos: {payload['over_segmentation_videos']}")
        lines.append(f"- Missing short-phase videos: {payload['missing_short_phase_videos']}")
        lines.append(f"- Extra fragments (total): {payload['total_extra_fragments']}")
        lines.append(f"- Lowest recall classes: {payload['lowest_recall_classes']}")
        lines.append(f"- Highest boundary MAE transitions: {payload['highest_boundary_error_transitions']}")
        lines.append("")
    lines.append("## Cross-seed instability")
    lines.append(f"- Unstable videos: {report['cross_seed_disagreement']['unstable_video_count']}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
