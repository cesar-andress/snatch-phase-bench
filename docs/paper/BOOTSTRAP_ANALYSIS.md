# Athlete-paired bootstrap: MS-TCN (B2) vs ASFormer (B3)

**Date:** 2026-07-22
**Experimental unit:** athlete (test split; n = 11)
**Seeds averaged per athlete before resampling:** [42, 123, 456]
**Bootstrap:** 10000 paired resamples with replacement; `numpy` Generator seed = 42
**Predictions:** frozen campaign `outputs/benchmark/{ms_tcn,asformer}/seed*/predictions_test.json`

---

## Method

1. For each model, seed, and test athlete, evaluate that athlete's videos with the canonical evaluator (`evaluate_dataset_videos`).
2. Frame macro-F1 is computed on pooled frames of the athlete (ignore `unlabeled`).
3. Segment F1@10/@25/@50 use macro-over-videos within the athlete; boundary MAE uses micro-over-videos within the athlete (same keys as the campaign aggregate).
4. Average the three seed values to obtain one score per athlete per model.
5. Draw 10{,}000 athlete bootstrap samples with replacement; for each sample compute the mean of B2, B3, and B3−B2.
6. Report bootstrap mean, SD, median, and 95% percentile CI.

This estimates uncertainty from **which athletes** are in the fixed test cohort. It does **not** retrain models and does **not** replace leave-one-athlete-out.

---

## Per-athlete point estimates (mean over seeds)

| Athlete | B2 F1@50 | B3 F1@50 | Δ F1@50 | B2 MAE | B3 MAE | Δ MAE |
|---------|---------:|---------:|--------:|------:|------:|------:|
| `bardalez` | 0.796 | 0.838 | +0.042 | 1.407 | 0.981 | -0.426 |
| `friedrich` | 0.909 | 0.911 | +0.001 | 1.211 | 1.022 | -0.189 |
| `genc` | 0.830 | 0.814 | -0.015 | 0.880 | 0.491 | -0.389 |
| `he` | 0.833 | 0.870 | +0.037 | 1.222 | 0.815 | -0.407 |
| `lo` | 0.815 | 0.812 | -0.003 | 0.963 | 0.778 | -0.185 |
| `mego` | 0.837 | 0.783 | -0.054 | 1.019 | 0.963 | -0.056 |
| `moeini` | 0.458 | 0.497 | +0.039 | 2.759 | 2.222 | -0.537 |
| `montero` | 0.826 | 0.838 | +0.012 | 0.917 | 0.787 | -0.130 |
| `nasar` | 0.742 | 0.747 | +0.005 | 1.341 | 0.885 | -0.456 |
| `ozbek` | 0.740 | 0.793 | +0.052 | 1.759 | 1.111 | -0.648 |
| `rustamov` | 0.736 | 0.783 | +0.048 | 1.065 | 0.694 | -0.370 |

---

## Bootstrap summaries

### MS-TCN (B2)

| Metric | Mean | SD | Median | 95% CI |
|--------|-----:|---:|-------:|--------|
| Frame macro-F1 | 0.9050 | 0.0074 | 0.9053 | [0.8898, 0.9187] |
| Segment F1@10 | 0.9027 | 0.0324 | 0.9053 | [0.8301, 0.9478] |
| Segment F1@25 | 0.8719 | 0.0309 | 0.8751 | [0.8040, 0.9196] |
| Segment F1@50 | 0.7752 | 0.0338 | 0.7784 | [0.7012, 0.8301] |
| Boundary MAE (frames) | 1.3193 | 0.1547 | 1.3027 | [1.0714, 1.6562] |

### ASFormer (B3)

| Metric | Mean | SD | Median | 95% CI |
|--------|-----:|---:|-------:|--------|
| Frame macro-F1 | 0.9052 | 0.0089 | 0.9059 | [0.8862, 0.9205] |
| Segment F1@10 | 0.9069 | 0.0335 | 0.9081 | [0.8333, 0.9497] |
| Segment F1@25 | 0.8618 | 0.0320 | 0.8651 | [0.7915, 0.9129] |
| Segment F1@50 | 0.7901 | 0.0309 | 0.7928 | [0.7220, 0.8401] |
| Boundary MAE (frames) | 0.9752 | 0.1276 | 0.9625 | [0.7764, 1.2613] |

### Paired difference B3 − B2

| Metric | Mean Δ | SD | Median Δ | 95% CI | Includes 0? |
|--------|-------:|---:|---------:|--------|:-----------:|
| Frame macro-F1 | +0.0002 | 0.0071 | +0.0006 | [-0.0148, +0.0131] | yes |
| Segment F1@10 | +0.0042 | 0.0056 | +0.0041 | [-0.0065, +0.0156] | yes |
| Segment F1@25 | -0.0102 | 0.0067 | -0.0101 | [-0.0232, +0.0030] | yes |
| Segment F1@50 | +0.0148 | 0.0093 | +0.0151 | [-0.0040, +0.0324] | yes |
| Boundary MAE (frames) | -0.3441 | 0.0529 | -0.3441 | [-0.4478, -0.2418] | no |

---

## Interpretation for the manuscript

Under athlete-paired bootstrap on the fixed 11-athlete test split:

- **Segment F1@50:** mean Δ = +0.015 with 95% CI [-0.004, +0.032], which **includes zero**. The observed B3 advantage on this endpoint should be interpreted **cautiously**; it is compatible with no athlete-level mean difference under resampling of the test cohort.

- **Boundary MAE (frames):** mean Δ = -0.344 with 95% CI [-0.448, -0.242] (excludes zero; negative Δ favors B3). Scope remains the present test athletes.

- **Frame macro-F1:** mean Δ = +0.000, 95% CI [-0.015, +0.013] (includes zero), consistent with nearly matched frame scores in the campaign tables.

**Recommended manuscript language:** prefer “descriptive seed-level means” plus this athlete-bootstrap CI for B3−B2; avoid “significantly outperforms” unless a CI excludes zero **and** the claim is scoped to this split.

**Limits:** n = 11 athletes; no retraining; no leave-one-athlete-out; seed averaging precedes bootstrap (training stochasticity is not separately bootstrapped).

---

## Artifacts

| Path | Content |
|------|---------|
| `analysis/bootstrap/per_athlete_seed_metrics.json` | Raw per-seed athlete metrics |
| `analysis/bootstrap/per_athlete_mean_metrics.json` | Seed-averaged athlete scores |
| `analysis/bootstrap/bootstrap_summaries.json` | Bootstrap means / CIs |
| `analysis/bootstrap/bootstrap_diff_samples.npz` | Difference bootstrap draws (regenerable; often gitignored) |
| `analysis/bootstrap/bootstrap_diff_distributions.png` / `.pdf` | Histograms of Δ |
| `analysis/bootstrap/bootstrap_diff_forest.png` / `.pdf` | CI forest plot of Δ |

*End of bootstrap analysis.*
