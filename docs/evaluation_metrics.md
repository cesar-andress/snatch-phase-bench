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

## Boundary metrics (planned)

- **Boundary F1:** tolerance \(\pm b\) frames around each GT boundary.
- **Mean boundary error:** average absolute frame error at transitions.

## Status

| Metric | Module | Status |
|--------|--------|--------|
| Window accuracy / F1 | `window.py` | Implemented |
| Frame aggregation + metrics | `frame.py` | Implemented |
| Edit score | `segment.py` | Implemented |
| Segmental F1@IoU | `segment.py` | Implemented |
| Boundary F1 | `boundary.py` | TODO |
