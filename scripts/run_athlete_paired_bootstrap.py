#!/usr/bin/env python3
"""Paired athlete-level bootstrap comparing ASFormer (B3) vs MS-TCN (B2).

Experimental unit: athlete (not video / segment / frame).
Uses frozen campaign predictions under outputs/benchmark/{ms_tcn,asformer}/seed*.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import f1_score

from snatch_phase_bench.evaluation.evaluate import evaluate_dataset_videos

METRICS = [
    "frame_macro_f1",
    "segmental_f1_at_10",
    "segmental_f1_at_25",
    "segmental_f1_at_50",
    "boundary_mae_frames",
]

METRIC_LABELS = {
    "frame_macro_f1": "Frame macro-F1",
    "segmental_f1_at_10": "Segment F1@10",
    "segmental_f1_at_25": "Segment F1@25",
    "segmental_f1_at_50": "Segment F1@50",
    "boundary_mae_frames": "Boundary MAE (frames)",
}

SEEDS = (42, 123, 456)
MODELS = {
    "ms_tcn": "B2",
    "asformer": "B3",
}


@dataclass(frozen=True)
class BootstrapSummary:
    mean: float
    std: float
    median: float
    ci95_low: float
    ci95_high: float
    n_boot: int
    n_units: int


def _load_predictions(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _videos_payload(pred: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for video in pred["videos"]:
        out[video["video_relpath"]] = {
            "y_true": np.asarray(video["y_true"], dtype=np.int64),
            "y_pred": np.asarray(video["y_pred"], dtype=np.int64),
            "athlete_id": video["athlete_id"],
        }
    return out


def _frame_macro_f1(videos: dict[str, dict[str, Any]], *, ignore_label_id: int = 0) -> float:
    y_true: list[int] = []
    y_pred: list[int] = []
    for payload in videos.values():
        gt = np.asarray(payload["y_true"], dtype=np.int64)
        pr = np.asarray(payload["y_pred"], dtype=np.int64)
        mask = gt != ignore_label_id
        y_true.extend(gt[mask].tolist())
        y_pred.extend(pr[mask].tolist())
    if not y_true:
        return float("nan")
    return float(f1_score(y_true, y_pred, average="macro", zero_division=0))


def athlete_metrics_from_videos(
    videos: dict[str, dict[str, Any]],
    *,
    model_identifier: str,
) -> dict[str, float]:
    """Canonical segment/boundary aggregates + pooled frame macro-F1 for one athlete subset."""
    result = evaluate_dataset_videos(videos, model_identifier=model_identifier)
    aggregate = result.aggregate
    segment = aggregate.get("segment_macro_over_videos", {})
    return {
        "frame_macro_f1": _frame_macro_f1(videos),
        "segmental_f1_at_10": float(segment["segmental_f1_at_10"]),
        "segmental_f1_at_25": float(segment["segmental_f1_at_25"]),
        "segmental_f1_at_50": float(segment["segmental_f1_at_50"]),
        # Match campaign primary endpoint (micro over videos within the athlete unit).
        "boundary_mae_frames": float(aggregate["boundary_mae_frames_micro_over_videos"]),
    }


def collect_per_athlete_seed_metrics(
    repo_root: Path,
) -> tuple[list[str], dict[str, dict[int, dict[str, dict[str, float]]]]]:
    """
    Returns:
      athletes: sorted test athlete ids
      table[model_key][seed][athlete_id][metric] = float
    """
    table: dict[str, dict[int, dict[str, dict[str, float]]]] = {}
    athletes: set[str] = set()

    for model_key in MODELS:
        table[model_key] = {}
        for seed in SEEDS:
            pred_path = repo_root / "outputs" / "benchmark" / model_key / f"seed{seed}" / "predictions_test.json"
            if not pred_path.exists():
                raise FileNotFoundError(f"Missing frozen predictions: {pred_path}")
            payload = _videos_payload(_load_predictions(pred_path))
            by_athlete: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
            for video_id, video in payload.items():
                athlete = str(video["athlete_id"])
                athletes.add(athlete)
                by_athlete[athlete][video_id] = video

            seed_rows: dict[str, dict[str, float]] = {}
            for athlete, vids in sorted(by_athlete.items()):
                seed_rows[athlete] = athlete_metrics_from_videos(
                    vids,
                    model_identifier=f"{model_key}_seed{seed}_athlete_{athlete}",
                )
            table[model_key][seed] = seed_rows

    return sorted(athletes), table


def average_over_seeds(
    table: dict[str, dict[int, dict[str, dict[str, float]]]],
    athletes: list[str],
) -> dict[str, dict[str, dict[str, float]]]:
    """model -> athlete -> metric -> mean over seeds."""
    out: dict[str, dict[str, dict[str, float]]] = {}
    for model_key in MODELS:
        out[model_key] = {}
        for athlete in athletes:
            out[model_key][athlete] = {}
            for metric in METRICS:
                vals = [table[model_key][seed][athlete][metric] for seed in SEEDS]
                out[model_key][athlete][metric] = float(np.mean(vals))
    return out


def paired_bootstrap(
    values_a: np.ndarray,
    values_b: np.ndarray,
    *,
    n_boot: int,
    seed: int,
) -> tuple[BootstrapSummary, BootstrapSummary, BootstrapSummary, np.ndarray]:
    """Paired bootstrap for mean(A), mean(B), and mean(B-A). Returns summaries + boot diffs."""
    if values_a.shape != values_b.shape:
        raise ValueError("Paired arrays must share shape")
    n = values_a.shape[0]
    rng = np.random.default_rng(seed)
    boot_a = np.empty(n_boot, dtype=np.float64)
    boot_b = np.empty(n_boot, dtype=np.float64)
    boot_d = np.empty(n_boot, dtype=np.float64)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        a = values_a[idx]
        b = values_b[idx]
        boot_a[i] = float(a.mean())
        boot_b[i] = float(b.mean())
        boot_d[i] = float((b - a).mean())

    def summarize(arr: np.ndarray) -> BootstrapSummary:
        low, high = np.percentile(arr, [2.5, 97.5])
        return BootstrapSummary(
            mean=float(arr.mean()),
            std=float(arr.std(ddof=1)),
            median=float(np.median(arr)),
            ci95_low=float(low),
            ci95_high=float(high),
            n_boot=n_boot,
            n_units=n,
        )

    return summarize(boot_a), summarize(boot_b), summarize(boot_d), boot_d


def _ci_includes_zero(summary: BootstrapSummary) -> bool:
    return summary.ci95_low <= 0.0 <= summary.ci95_high


def plot_difference_histograms(
    boot_diffs: dict[str, np.ndarray],
    diff_summaries: dict[str, BootstrapSummary],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    n = len(METRICS)
    fig, axes = plt.subplots(2, 3, figsize=(12, 7), dpi=150)
    axes_flat = list(axes.ravel())
    for ax, metric in zip(axes_flat, METRICS):
        arr = boot_diffs[metric]
        summary = diff_summaries[metric]
        ax.hist(arr, bins=40, color="#4C72B0", alpha=0.85, edgecolor="white")
        ax.axvline(0.0, color="black", linestyle="--", linewidth=1.0, label="0")
        ax.axvline(summary.mean, color="#DD8452", linewidth=1.5, label="boot mean")
        ax.axvline(summary.ci95_low, color="#55A868", linestyle=":", linewidth=1.2)
        ax.axvline(summary.ci95_high, color="#55A868", linestyle=":", linewidth=1.2, label="95% CI")
        ax.set_title(METRIC_LABELS[metric])
        ax.set_xlabel(r"$\Delta$ (B3$-$B2)")
        ax.set_ylabel("Count")
    axes_flat[-1].axis("off")
    handles, labels = axes_flat[0].get_legend_handles_labels()
    axes_flat[-1].legend(handles, labels, loc="center", frameon=False)
    fig.suptitle("Paired athlete bootstrap: ASFormer (B3) $-$ MS-TCN (B2)", fontsize=12)
    fig.tight_layout()
    fig.savefig(output_dir / "bootstrap_diff_distributions.png")
    fig.savefig(output_dir / "bootstrap_diff_distributions.pdf")
    plt.close(fig)

    # Two-panel forest: F1 metrics share a scale; MAE uses its own (frames + ms twin).
    f1_keys = [
        "frame_macro_f1",
        "segmental_f1_at_10",
        "segmental_f1_at_25",
        "segmental_f1_at_50",
    ]
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(8.2, 3.6),
        dpi=200,
        gridspec_kw={"width_ratios": [1.35, 1.0]},
    )
    ax = axes[0]
    y = np.arange(len(f1_keys))
    means = [diff_summaries[m].mean for m in f1_keys]
    lows = [diff_summaries[m].ci95_low for m in f1_keys]
    highs = [diff_summaries[m].ci95_high for m in f1_keys]
    ax.axvline(0.0, color="black", linestyle="--", linewidth=1.0)
    ax.errorbar(
        means,
        y,
        xerr=[np.asarray(means) - np.asarray(lows), np.asarray(highs) - np.asarray(means)],
        fmt="o",
        color="#2F5D8C",
        ecolor="#2F5D8C",
        capsize=3,
        markersize=5,
    )
    ax.set_yticks(y)
    ax.set_yticklabels([METRIC_LABELS[m] for m in f1_keys])
    ax.set_xlabel(r"$\Delta$ F1  (B3$-$B2)")
    ax.set_title("(a) Frame / segment F1")
    ax.invert_yaxis()

    ax = axes[1]
    mae = diff_summaries["boundary_mae_frames"]
    ax.axvline(0.0, color="black", linestyle="--", linewidth=1.0)
    ax.errorbar(
        [mae.mean],
        [0],
        xerr=[[mae.mean - mae.ci95_low], [mae.ci95_high - mae.mean]],
        fmt="o",
        color="#2F5D8C",
        ecolor="#2F5D8C",
        capsize=3,
        markersize=5,
    )
    ax.set_yticks([0])
    ax.set_yticklabels(["Boundary MAE"])
    ax.set_xlabel(r"$\Delta$ MAE (frames; B3$-$B2)")
    ax.set_title("(b) Boundary MAE")
    ax2 = ax.twiny()
    ax2.set_xlim(np.asarray(ax.get_xlim()) * 40.0)
    ax2.set_xlabel(r"$\Delta$ MAE (ms at 25 fps)")
    fig.suptitle(
        r"Athlete-paired bootstrap differences ($n{=}11$; 10{,}000 resamples)",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(output_dir / "bootstrap_diff_forest.png")
    fig.savefig(output_dir / "bootstrap_diff_forest.pdf")
    plt.close(fig)


def write_markdown(
    path: Path,
    *,
    athletes: list[str],
    athlete_means: dict[str, dict[str, dict[str, float]]],
    summaries_b2: dict[str, BootstrapSummary],
    summaries_b3: dict[str, BootstrapSummary],
    summaries_diff: dict[str, BootstrapSummary],
    n_boot: int,
    seed: int,
) -> None:
    lines: list[str] = []
    A = lines.append
    A("# Athlete-paired bootstrap: MS-TCN (B2) vs ASFormer (B3)")
    A("")
    A("**Date:** 2026-07-22")
    A("**Experimental unit:** athlete (test split; n = "
      f"{len(athletes)})")
    A("**Seeds averaged per athlete before resampling:** "
      f"{list(SEEDS)}")
    A(f"**Bootstrap:** {n_boot} paired resamples with replacement; "
      f"`numpy` Generator seed = {seed}")
    A("**Predictions:** frozen campaign "
      "`outputs/benchmark/{ms_tcn,asformer}/seed*/predictions_test.json`")
    A("")
    A("---")
    A("")
    A("## Method")
    A("")
    A("1. For each model, seed, and test athlete, evaluate that athlete's videos "
      "with the canonical evaluator (`evaluate_dataset_videos`).")
    A("2. Frame macro-F1 is computed on pooled frames of the athlete "
      "(ignore `unlabeled`).")
    A("3. Segment F1@10/@25/@50 use macro-over-videos within the athlete; "
      "boundary MAE uses micro-over-videos within the athlete "
      "(same keys as the campaign aggregate).")
    A("4. Average the three seed values to obtain one score per athlete per model.")
    A("5. Draw 10{,}000 athlete bootstrap samples with replacement; for each sample "
      "compute the mean of B2, B3, and B3−B2.")
    A("6. Report bootstrap mean, SD, median, and 95% percentile CI.")
    A("")
    A("This estimates uncertainty from **which athletes** are in the fixed test "
      "cohort. It does **not** retrain models and does **not** replace leave-one-athlete-out.")
    A("")
    A("---")
    A("")
    A("## Per-athlete point estimates (mean over seeds)")
    A("")
    A("| Athlete | B2 F1@50 | B3 F1@50 | Δ F1@50 | B2 MAE | B3 MAE | Δ MAE |")
    A("|---------|---------:|---------:|--------:|------:|------:|------:|")
    for athlete in athletes:
        b2 = athlete_means["ms_tcn"][athlete]
        b3 = athlete_means["asformer"][athlete]
        A(
            f"| `{athlete}` | {b2['segmental_f1_at_50']:.3f} | "
            f"{b3['segmental_f1_at_50']:.3f} | "
            f"{b3['segmental_f1_at_50']-b2['segmental_f1_at_50']:+.3f} | "
            f"{b2['boundary_mae_frames']:.3f} | "
            f"{b3['boundary_mae_frames']:.3f} | "
            f"{b3['boundary_mae_frames']-b2['boundary_mae_frames']:+.3f} |"
        )
    A("")
    A("---")
    A("")
    A("## Bootstrap summaries")
    A("")
    A("### MS-TCN (B2)")
    A("")
    A("| Metric | Mean | SD | Median | 95% CI |")
    A("|--------|-----:|---:|-------:|--------|")
    for metric in METRICS:
        s = summaries_b2[metric]
        A(
            f"| {METRIC_LABELS[metric]} | {s.mean:.4f} | {s.std:.4f} | "
            f"{s.median:.4f} | [{s.ci95_low:.4f}, {s.ci95_high:.4f}] |"
        )
    A("")
    A("### ASFormer (B3)")
    A("")
    A("| Metric | Mean | SD | Median | 95% CI |")
    A("|--------|-----:|---:|-------:|--------|")
    for metric in METRICS:
        s = summaries_b3[metric]
        A(
            f"| {METRIC_LABELS[metric]} | {s.mean:.4f} | {s.std:.4f} | "
            f"{s.median:.4f} | [{s.ci95_low:.4f}, {s.ci95_high:.4f}] |"
        )
    A("")
    A("### Paired difference B3 − B2")
    A("")
    A("| Metric | Mean Δ | SD | Median Δ | 95% CI | Includes 0? |")
    A("|--------|-------:|---:|---------:|--------|:-----------:|")
    for metric in METRICS:
        s = summaries_diff[metric]
        A(
            f"| {METRIC_LABELS[metric]} | {s.mean:+.4f} | {s.std:.4f} | "
            f"{s.median:+.4f} | [{s.ci95_low:+.4f}, {s.ci95_high:+.4f}] | "
            f"{'yes' if _ci_includes_zero(s) else 'no'} |"
        )
    A("")
    A("---")
    A("")
    A("## Interpretation for the manuscript")
    A("")
    A("Under athlete-paired bootstrap on the fixed 11-athlete test split:")
    A("")

    f1 = summaries_diff["segmental_f1_at_50"]
    mae = summaries_diff["boundary_mae_frames"]
    frame = summaries_diff["frame_macro_f1"]

    if _ci_includes_zero(f1):
        A(
            f"- **Segment F1@50:** mean Δ = {f1.mean:+.3f} with 95% CI "
            f"[{f1.ci95_low:+.3f}, {f1.ci95_high:+.3f}], which **includes zero**. "
            "The observed B3 advantage on this endpoint should be interpreted "
            "**cautiously**; it is compatible with no athlete-level mean difference "
            "under resampling of the test cohort."
        )
    else:
        A(
            f"- **Segment F1@50:** mean Δ = {f1.mean:+.3f} with 95% CI "
            f"[{f1.ci95_low:+.3f}, {f1.ci95_high:+.3f}] (excludes zero). "
            "Still treat as uncertainty on a single fixed split, not LOAO generalization."
        )
    A("")
    if _ci_includes_zero(mae):
        A(
            f"- **Boundary MAE (frames):** mean Δ = {mae.mean:+.3f} with 95% CI "
            f"[{mae.ci95_low:+.3f}, {mae.ci95_high:+.3f}], which **includes zero**. "
            "Lower B3 MAE in the campaign means is **not** established as a stable "
            "athlete-level improvement by this bootstrap; report descriptively."
        )
    else:
        A(
            f"- **Boundary MAE (frames):** mean Δ = {mae.mean:+.3f} with 95% CI "
            f"[{mae.ci95_low:+.3f}, {mae.ci95_high:+.3f}] (excludes zero; "
            "negative Δ favors B3). Scope remains the present test athletes."
        )
    A("")
    if _ci_includes_zero(frame):
        A(
            f"- **Frame macro-F1:** mean Δ = {frame.mean:+.3f}, 95% CI "
            f"[{frame.ci95_low:+.3f}, {frame.ci95_high:+.3f}] (includes zero), "
            "consistent with nearly matched frame scores in the campaign tables."
        )
    else:
        A(
            f"- **Frame macro-F1:** mean Δ = {frame.mean:+.3f}, 95% CI "
            f"[{frame.ci95_low:+.3f}, {frame.ci95_high:+.3f}]."
        )
    A("")
    A("**Recommended manuscript language:** prefer “descriptive seed-level means” "
      "plus this athlete-bootstrap CI for B3−B2; avoid “significantly outperforms” "
      "unless a CI excludes zero **and** the claim is scoped to this split.")
    A("")
    A("**Limits:** n = 11 athletes; no retraining; no leave-one-athlete-out; "
      "seed averaging precedes bootstrap (training stochasticity is not separately "
      "bootstrapped).")
    A("")
    A("---")
    A("")
    A("## Artifacts")
    A("")
    A("| Path | Content |")
    A("|------|---------|")
    A("| `analysis/bootstrap/per_athlete_seed_metrics.json` | Raw per-seed athlete metrics |")
    A("| `analysis/bootstrap/per_athlete_mean_metrics.json` | Seed-averaged athlete scores |")
    A("| `analysis/bootstrap/bootstrap_summaries.json` | Bootstrap means / CIs |")
    A("| `analysis/bootstrap/bootstrap_diff_samples.npz` | Difference bootstrap draws (regenerable; often gitignored) |")
    A("| `analysis/bootstrap/bootstrap_diff_distributions.png` / `.pdf` | Histograms of Δ |")
    A("| `analysis/bootstrap/bootstrap_diff_forest.png` / `.pdf` | CI forest plot of Δ |")
    A("")
    A("*End of bootstrap analysis.*")
    A("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--n-boot", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    repo_root: Path = args.repo_root
    out_dir = repo_root / "analysis" / "bootstrap"
    out_dir.mkdir(parents=True, exist_ok=True)

    athletes, per_seed = collect_per_athlete_seed_metrics(repo_root)
    athlete_means = average_over_seeds(per_seed, athletes)

    summaries_b2: dict[str, BootstrapSummary] = {}
    summaries_b3: dict[str, BootstrapSummary] = {}
    summaries_diff: dict[str, BootstrapSummary] = {}
    boot_diffs: dict[str, np.ndarray] = {}

    for metric in METRICS:
        a = np.asarray(
            [athlete_means["ms_tcn"][ath][metric] for ath in athletes],
            dtype=np.float64,
        )
        b = np.asarray(
            [athlete_means["asformer"][ath][metric] for ath in athletes],
            dtype=np.float64,
        )
        s_a, s_b, s_d, diffs = paired_bootstrap(
            a, b, n_boot=args.n_boot, seed=args.seed
        )
        summaries_b2[metric] = s_a
        summaries_b3[metric] = s_b
        summaries_diff[metric] = s_d
        boot_diffs[metric] = diffs

    # Persist JSON
    (out_dir / "per_athlete_seed_metrics.json").write_text(
        json.dumps(per_seed, indent=2),
        encoding="utf-8",
    )
    (out_dir / "per_athlete_mean_metrics.json").write_text(
        json.dumps(
            {
                "athletes": athletes,
                "seeds": list(SEEDS),
                "models": MODELS,
                "metrics": athlete_means,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "bootstrap_summaries.json").write_text(
        json.dumps(
            {
                "n_boot": args.n_boot,
                "seed": args.seed,
                "athletes": athletes,
                "b2": {m: asdict(summaries_b2[m]) for m in METRICS},
                "b3": {m: asdict(summaries_b3[m]) for m in METRICS},
                "b3_minus_b2": {
                    m: {
                        **asdict(summaries_diff[m]),
                        "ci_includes_zero": _ci_includes_zero(summaries_diff[m]),
                    }
                    for m in METRICS
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    np.savez_compressed(
        out_dir / "bootstrap_diff_samples.npz",
        **{metric: boot_diffs[metric] for metric in METRICS},
        athletes=np.asarray(athletes),
    )

    plot_difference_histograms(boot_diffs, summaries_diff, out_dir)

    docs_path = repo_root / "docs" / "paper" / "BOOTSTRAP_ANALYSIS.md"
    write_markdown(
        docs_path,
        athletes=athletes,
        athlete_means=athlete_means,
        summaries_b2=summaries_b2,
        summaries_b3=summaries_b3,
        summaries_diff=summaries_diff,
        n_boot=args.n_boot,
        seed=args.seed,
    )

    print(f"Wrote artifacts under {out_dir}")
    print(f"Wrote {docs_path}")
    for metric in METRICS:
        s = summaries_diff[metric]
        print(
            f"{metric}: Δ={s.mean:+.4f} CI95=[{s.ci95_low:+.4f}, {s.ci95_high:+.4f}] "
            f"includes0={_ci_includes_zero(s)}"
        )


if __name__ == "__main__":
    main()
