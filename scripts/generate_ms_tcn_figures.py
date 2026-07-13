#!/usr/bin/env python3
"""Generate reproducible MS-TCN benchmark figures from canonical JSON artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from snatch_phase_bench.benchmark.aggregate_results import aggregate_seed_results


PHASE_NAMES = {
    1: "setup",
    2: "first_pull",
    3: "transition",
    4: "second_pull",
    5: "turnover",
    6: "catch",
    7: "recovery",
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def plot_training_curves(output_dir: Path, seeds: list[int], figures_dir: Path) -> None:
    for seed in seeds:
        history_path = output_dir / f"seed{seed}" / "history.json"
        if not history_path.exists():
            continue
        history = _load_json(history_path)
        epochs = [entry["epoch"] for entry in history]
        train_loss = [entry["train"]["loss_total"] for entry in history]
        val_loss = [entry["val"]["loss_total"] for entry in history]
        val_f1 = [entry["val"].get("segmental_f1_at_50", entry["val"]["macro_f1"]) for entry in history]

        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        axes[0].plot(epochs, train_loss, label="train")
        axes[0].plot(epochs, val_loss, label="val")
        axes[0].set_title(f"Loss (seed {seed})")
        axes[0].legend()
        axes[1].plot(epochs, val_f1, label="val segment F1@50")
        axes[1].set_title(f"Validation monitor (seed {seed})")
        axes[1].legend()
        fig.tight_layout()
        fig.savefig(figures_dir / f"training_curves_seed{seed}.png", dpi=150)
        plt.close(fig)


def plot_aggregate_stability(output_dir: Path, seeds: list[int], figures_dir: Path) -> None:
    seed_dirs = {seed: output_dir / f"seed{seed}" for seed in seeds}
    aggregated = aggregate_seed_results(seed_dirs, split="test")
    metrics = aggregated["aggregate"]
    names = [k for k, v in metrics.items() if v["mean"] is not None]
    means = [metrics[k]["mean"] for k in names]
    stds = [metrics[k]["std"] for k in names]

    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(names))
    ax.bar(x, means, yerr=stds, capsize=4)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=30, ha="right")
    ax.set_title("Aggregate test metrics (mean ± std across seeds)")
    fig.tight_layout()
    fig.savefig(figures_dir / "aggregate_seed_stability.png", dpi=150)
    plt.close(fig)


def plot_confusion_matrix(output_dir: Path, seed: int, figures_dir: Path) -> None:
    eval_payload = _load_json(output_dir / f"seed{seed}" / "eval_test.json")
    cm_payload = eval_payload.get("confusion_matrix")
    if not cm_payload:
        return
    matrix = np.asarray(cm_payload["matrix"])
    labels = [PHASE_NAMES.get(int(l), str(l)) for l in cm_payload["labels"]]
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title(f"Frame confusion matrix (seed {seed}, test)")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(figures_dir / f"confusion_matrix_seed{seed}.png", dpi=150)
    plt.close(fig)


def plot_qualitative_timeline(output_dir: Path, seed: int, figures_dir: Path) -> None:
    predictions = _load_json(output_dir / f"seed{seed}" / "predictions_test.json")
    if not predictions["videos"]:
        return
    video = predictions["videos"][0]
    frames = np.arange(len(video["y_true"]))
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.step(frames, video["y_true"], where="post", label="ground truth", linewidth=1.5)
    ax.step(frames, video["y_pred"], where="post", label="prediction", linewidth=1.0, alpha=0.8)
    ax.set_yticks(list(PHASE_NAMES.keys()))
    ax.set_yticklabels([PHASE_NAMES[k] for k in PHASE_NAMES])
    ax.set_xlabel("Frame")
    ax.set_title(f"Qualitative timeline: {video['video_relpath']} (seed {seed})")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(figures_dir / f"qualitative_timeline_seed{seed}.png", dpi=150)
    plt.close(fig)


def write_metric_tables(output_dir: Path, seeds: list[int], figures_dir: Path) -> None:
    seed_dirs = {seed: output_dir / f"seed{seed}" for seed in seeds}
    aggregated = aggregate_seed_results(seed_dirs, split="test")
    lines = ["# MS-TCN figure companion tables", ""]
    lines.append("## Segment metrics")
    lines.append("| Seed | F1@10 | F1@25 | F1@50 | Edit |")
    lines.append("|------|-------|-------|-------|------|")
    for seed in seeds:
        metrics = aggregated["per_seed"][str(seed)]["metrics"]
        lines.append(
            f"| {seed} | {metrics.get('segmental_f1_at_10', 'NA')} | "
            f"{metrics.get('segmental_f1_at_25', 'NA')} | {metrics.get('segmental_f1_at_50', 'NA')} | "
            f"{metrics.get('edit_score', 'NA')} |"
        )
    (figures_dir / "metric_tables.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MS-TCN benchmark figures.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/benchmark/ms_tcn"))
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    args = parser.parse_args()

    figures_dir = args.output_dir / "aggregate" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    plot_training_curves(args.output_dir, args.seeds, figures_dir)
    plot_aggregate_stability(args.output_dir, args.seeds, figures_dir)
    for seed in args.seeds:
        plot_confusion_matrix(args.output_dir, seed, figures_dir)
        plot_qualitative_timeline(args.output_dir, seed, figures_dir)
    write_metric_tables(args.output_dir, args.seeds, figures_dir)
    print(json.dumps({"figures_dir": str(figures_dir)}, indent=2))


if __name__ == "__main__":
    main()
