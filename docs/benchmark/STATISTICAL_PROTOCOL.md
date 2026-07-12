# SnatchPhaseBench — Statistical Protocol

**Parent document:** [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md)  
**Status:** Design only — apply at implementation and manuscript writing  
**Version:** stats-v1.0-draft

---

## 1. Purpose

Define **mandatory** and **recommended** statistical analyses so benchmark comparisons are defensible in a Q1 journal. This protocol addresses:

- Window overlap (non-independent samples)
- Small test cohort (11 athletes, 208 videos)
- Multiple model comparisons (B0 vs several B2 models)
- Multiple metrics (boundary, segment, frame)

**Principle:** Prefer ** athlete-level or video-level paired units** over window-level tests.

---

## 2. Units of analysis

| Unit | Use | Avoid for |
|------|-----|-----------|
| **Video** (attempt) | Primary paired comparisons of boundary MAE | — |
| **Athlete** | LOAO aggregates; between-athlete variance | Window-level t-tests |
| **Transition event** | Per-transition boundary MAE breakdown | Independence assumed across transitions within same video without correction |
| **Window** | B1 reproduction only | Significance testing between models |

When reporting window-level metrics (B1), describe as **descriptive**; do not attach p-values from window-level tests.

---

## 3. Random seeds and repeated runs

### 3.1 Mandatory (B2 learned models)

| Parameter | Specification |
|-----------|---------------|
| **Seeds per model** | **Minimum 3**; **recommended 5** |
| **Seed list** | Fixed and published: e.g. `{42, 123, 456, 789, 1024}` |
| **What varies** | Weight init, minibatch order, dropout masks |
| **What is fixed** | Split, preprocessing, hyperparameter search protocol |
| **Report** | Mean ± SD across seeds on test set |

### 3.2 Deterministic models

| Model | Runs |
|-------|------|
| B0 (rule-based) | **1** — deterministic given inputs |
| B1 (frozen checkpoint) | **1** — frozen weights |

### 3.3 Cross-athlete uncertainty (mandatory for submission)

| Protocol | Specification |
|----------|---------------|
| **Grouped LOAO** | Train/val on N−1 athletes; test on held-out athlete; repeat for all 70 athletes |
| **Aggregation** | Mean ± SD of per-athlete test metrics |
| **Primary use** | Confidence intervals on boundary MAE and segment-F1@50 |

Alternative: **5-fold grouped k-fold by athlete** if LOAO compute is prohibitive — document choice in Methods; LOAO preferred.

---

## 4. Point estimates and confidence intervals

### 4.1 Reporting format

All primary tables:

```text
metric = mean ± std   [95% CI_low, CI_high]
```

### 4.2 Bootstrap CI (mandatory for LOAO / small N)

| Setting | Value |
|---------|-------|
| Resampling unit | **Athletes** (or videos if athlete-level LOAO already aggregated) |
| Replicates | **10,000** bootstrap samples |
| CI level | **95%** |
| Method | Percentile bootstrap |
| Implementation | `scipy.stats.bootstrap` or equivalent; seed fixed |

Use bootstrap CI when:

- Reporting LOAO aggregates
- N_test athletes = 11 (too small for normal approximation)

### 4.3 Seed-based SD

Across random seeds on the **fixed test split**, report SD as dispersion of training stochasticity—not a substitute for LOAO.

---

## 5. Hypothesis tests

### 5.1 When tests are required

Inferential tests are **mandatory** when the manuscript claims:

- “Model X **significantly** outperforms B0”
- “Improvement over the heuristic”
- Rank ordering with statistical superiority

If the paper uses **descriptive comparison only** (“X achieved lower MAE than B0”), tests are recommended but language must avoid “significant.”

### 5.2 Primary paired test (mandatory when claiming superiority)

Compare each **B2 model** vs **B0** on **per-video boundary MAE** (mean across transitions per video):

| Test | Wilcoxon signed-rank (paired) |
|------|------------------------------|
| Pairing | Same test video, same GT |
| Alternative | Two-sided |
| α | 0.05 |
| Effect size | Rank-biserial correlation **r** or Cohen's **d** on video MAE differences |

**Rationale:** Boundary errors are rarely normal; Wilcoxon is robust for small N_videos.

### 5.3 Secondary paired tests

| Comparison | Test | Unit |
|------------|------|------|
| B2 vs B2 (e.g. ASFormer vs MS-TCN) | Wilcoxon paired | Per-video boundary MAE |
| Segment-F1@50 | Wilcoxon paired | Per-video F1 |
| Frame MoF | Wilcoxon paired (descriptive priority lower) | Per-video MoF |

### 5.4 LOAO fold comparisons

For LOAO distributions (one score per athlete):

- Compare models with **Wilcoxon signed-rank** on paired athlete scores
- Report **median difference** and bootstrap 95% CI

---

## 6. Multiple comparison correction

### 6.1 Mandatory correction

When testing **K** B2 models against B0 on **M** primary endpoints:

| Method | Holm-Bonferroni |
|--------|-----------------|
| Family 1 | Boundary MAE (ms) — primary |
| Family 2 | Segment-F1@50 |
| Family 3 | Edit score |

Apply Holm correction **within each family** across K comparisons. Do not pool unrelated metrics into one family.

### 6.2 Per-transition exploratory tests

Per-transition boundary MAE (6 transitions × K models):

- Label as **exploratory**
- Use Holm correction within each transition family **or** report uncorrected p with explicit exploratory caveat
- Prefer **effect sizes + CIs** over p-value fishing

---

## 7. Effect sizes (mandatory alongside p-values)

| Metric | Effect size |
|--------|-------------|
| Boundary MAE difference | Mean/median Δ ms + **Cohen's d** (paired) |
| Segment-F1 difference | Δ F1 (absolute pp) + **r** from Wilcoxon |
| Win rate | Fraction of test videos where model A beats B |

Report effect sizes even when p > 0.05 — benchmark honesty requires magnitude, not only significance.

---

## 8. Metric-specific guidance

### 8.1 Boundary MAE (primary)

- **Primary endpoint** for superiority claims
- Aggregate: mean over all transitions and videos
- Secondary: per-transition table (exploratory)
- Units: **milliseconds** in main text; frames in appendix

### 8.2 Segment-F1@50

- Co-primary with boundary for TAS literature alignment
- Hungarian/greedy matching per video — compute F1 per video, then aggregate

### 8.3 Edit score

- Descriptive + paired Wilcoxon if claimed
- Sensitive to over-segmentation — interpret with qualitative examples

### 8.4 Frame accuracy (MoF)

- **Descriptive only** in main claims unless explicitly justified
- Known saturation from long phases (`setup`, `recovery`)

### 8.5 Window-level (B1 only)

- No inferential tests vs B2 (different output protocols)
- Report as reproduction artifact

---

## 9. Window overlap and independence

Stride-1 windows share 30/31 frames ([`../reproduction/temporal_autocorrelation.md`](../reproduction/temporal_autocorrelation.md)).

| Rule | Action |
|------|--------|
| **Forbidden** | Window-level t-test / χ² for model comparison |
| **Required** | Frame/segment/boundary metrics derived from consolidated per-frame predictions |
| **Discussion** | State effective dependence; cite autocorrelation analysis |

---

## 10. Power and sample size (honest reporting)

With **11 test athletes** and **208 videos** total:

- Detecting **small** improvements (< 5 ms boundary MAE) may be **underpowered**
- LOAO with 70 folds provides structure but not large-N asymptotics
- **Mandatory:** report CIs and effect sizes; avoid over-claiming from single split
- Optional: post-hoc sensitivity analysis excluding outlier athletes (pre-specify exclusion rules)

Do **not** invent power analysis numbers not computed from data.

---

## 11. Analysis workflow (implementation checklist)

```text
1. Collect per-video, per-metric scores for each model × seed
2. Aggregate seeds → mean per video
3. LOAO (optional path) → per-athlete scores → bootstrap CI
4. Paired Wilcoxon vs B0 on video-level boundary MAE
5. Holm correction within metric family
6. Compute Cohen's d / rank-biserial r
7. Write results JSON + manuscript table
```

---

## 12. Software and logging

| Output | Path |
|--------|------|
| Raw per-video scores | `outputs/benchmark/<model>/stats/per_video.json` |
| Test results | `outputs/benchmark/<model>/stats/inferential.json` |
| Config | `configs/benchmark/<model>.yaml` includes `seeds:` list |

Pin `scipy`, `numpy`, `pandas` versions in environment log.

---

## 13. Mandatory vs recommended summary

| Analysis | Status |
|----------|--------|
| ≥3 seeds for B2 models | **Mandatory** |
| LOAO or grouped athlete CV | **Mandatory** for submission |
| Bootstrap 95% CI (athlete level) | **Mandatory** |
| Per-video paired Wilcoxon vs B0 | **Mandatory** if claiming superiority |
| Holm correction | **Mandatory** across B2 comparisons per endpoint |
| Effect sizes | **Mandatory** |
| Bootstrap on windows | **Forbidden** |
| Window-level significance tests | **Forbidden** |
| Friedman + Nemenyi across all models | Recommended for multi-model ranking |
| Bayesian optional analysis | Optional — not required |

---

## 14. Manuscript text requirements

Methods § must state:

1. Unit of analysis (video-level pairing)
2. Seed count and values
3. LOAO protocol
4. Test names (Wilcoxon signed-rank)
5. Correction method (Holm)
6. CI method (bootstrap, 10k, athlete-level)
7. Software version

Results § must pair every “significantly better” claim with **Δ metric**, **CI**, **p_corrected**, and **effect size**.

---

## 15. Related documents

- [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md) §9 — metric definitions
- [`../evaluation_metrics.md`](../evaluation_metrics.md) — mathematical definitions
- [`../paper/REVIEWER_CHECKLIST.md`](../paper/REVIEWER_CHECKLIST.md) #7, #12
