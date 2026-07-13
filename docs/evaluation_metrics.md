# Evaluation metric definitions

This document defines metrics implemented or planned in `snatch_phase_bench.evaluation.metrics`.

## Window-level classification (frozen baseline protocol)

Given window predictions \(\hat{y}_i\) and labels \(y_i\) for \(i = 1,\ldots,N\):

- **Accuracy:** \(\mathrm{Acc} = \frac{1}{N}\sum_i \mathbf{1}[\hat{y}_i = y_i]\)
- **Macro precision / recall / F1:** unweighted mean over classes \(c\):

\[
\mathrm{F1}_c = \frac{2\,\mathrm{Prec}_c\,\mathrm{Rec}_c}{\mathrm{Prec}_c + \mathrm{Rec}_c}
\]

- **Weighted F1:** support-weighted mean of per-class F1.

This matches `sklearn.metrics.classification_report` used by the frozen baseline.

## Frame-level aggregation

Given per-frame predictions obtained by aggregating overlapping windows (e.g. majority vote at each center frame):

- Same classification metrics as above, computed on unique frames \((\text{video}, t)\).

**Note:** Frame-level metrics are generally lower-correlated than window-level when stride \(<\) window size.

## Segment-level

Ground-truth and predicted segments are intervals \([s, e]\) with class label \(c\) on a discrete timeline \(t = 0,\ldots,T-1\).

### Temporal IoU

For segments \(A = [s_a, e_a]\), \(B = [s_b, e_b]\):

\[
\mathrm{IoU}(A, B) = \frac{|[s_a, e_a] \cap [s_b, e_b]|}{|[s_a, e_a] \cup [s_b, e_b]|}
\]

### Segmental F1 at IoU threshold \(\tau\)

A predicted segment \(\hat{S}\) matches ground truth \(S\) if same class and \(\mathrm{IoU}(\hat{S}, S) \ge \tau\).

Compute precision/recall/F1 over matched segments (Hungarian or greedy matching). Report F1@10, F1@25, F1@50 for \(\tau \in \{0.10, 0.25, 0.50\}\).

### Edit score (Levenshtein)

Convert GT and predicted segment label sequences to strings of contiguous segments. Let \(d\) be Levenshtein distance, \(n = \max(|\text{GT}|, |\text{Pred}|)\):

\[
\mathrm{Edit} = 1 - \frac{d}{n}
\]

Higher is better; equals 1 when segment sequences match exactly.

## Boundary metrics (planned — benchmark differentiator)

Literature foundation (Part 3.6, 6.4) recommends **millisecond-scale boundary evaluation** per phase transition, especially Second Pull→Turnover.

For each ground-truth transition frame \(t^\*\) and predicted transition \(\hat{t}\):

- **Mean absolute boundary error (frames):** \(\mathrm{MAE}_b = |t^\* - \hat{t}|\)
- **Mean absolute boundary error (ms):** \(\mathrm{MAE}_b^{ms} = \mathrm{MAE}_b \cdot 1000 / \mathrm{fps}\)
- **Boundary within tolerance:** fraction of boundaries with \(|\hat{t} - t^\*| \le \tau\) for \(\tau \in \{1, 2, 3\}\) frames
- **Boundary F1:** match predicted boundaries to GT within ±\(b\) frames

Report **per transition type** (not only aggregated), e.g. transition→second_pull, second_pull→turnover.

Implementation: `boundary.py` (TODO). See [`benchmark/BENCHMARK_PLAN.md`](benchmark/BENCHMARK_PLAN.md).

## Status

| Metric | Module | Status |
|--------|--------|--------|
| Window accuracy / F1 | `window.py` | Implemented |
| Frame aggregation + metrics | `frame.py` | Implemented |
| Edit score | `segment.py` | Implemented |
| Segmental F1@IoU | `segment.py` | Implemented |
| Boundary MAE (frames/ms) | `boundary.py` | TODO — **P0 for benchmark** |
| Boundary within-τ | `boundary.py` | TODO |
| Per-transition breakdown | `boundary.py` + ontology | TODO |

Phase ontologies and the seven→five mapping for B0 are defined in `configs/ontology/` and loaded via `snatch_phase_bench.ontology`.
