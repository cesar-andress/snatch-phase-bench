# Evaluation metric definitions

Operational reference for `snatch_phase_bench.evaluation`.
Configuration contract: [`configs/benchmark.yaml`](../configs/benchmark.yaml).

## Interval convention

Segments use the **half-open** convention **`[start_frame, end_frame)`**:
`start_frame` is inclusive, `end_frame` is exclusive.
Canonical type: `evaluation.segments.CanonicalSegment`.

## Window-level classification (frozen baseline protocol)

Given window predictions \(\hat{y}_i\) and labels \(y_i\) for \(i = 1,\ldots,N\):

- **Accuracy:** \(\mathrm{Acc} = \frac{1}{N}\sum_i \mathbf{1}[\hat{y}_i = y_i]\)
- **Macro precision / recall / F1:** unweighted mean over classes.

Implementation: `evaluation.metrics.window`.

## Frame-level aggregation

Overlapping window predictions collapse to unique `(video, frame)` pairs via majority vote or center-frame selection.
Implementation: `evaluation.metrics.frame`.

## Segment-level metrics

### Temporal IoU

For segments \(A = [s_a, e_a)\), \(B = [s_b, e_b)\):

\[
\mathrm{IoU}(A, B) = \frac{|[s_a, e_a) \cap [s_b, e_b)|}{|[s_a, e_a) \cup [s_b, e_b)|}
\]

### Segmental F1 at IoU threshold \(\tau\)

**Matching algorithm (greedy, class-aware, one-to-one):**

1. Convert frame labels to contiguous segments (ignored labels omitted).
2. Iterate predicted segments in order.
3. Match each prediction to the highest-IoU unmatched ground-truth segment of the **same class** if IoU \(\ge \tau\).
4. Compute precision/recall/F1 from TP/FP/FN counts.

This is **not** Hungarian matching.

Report F1@10, F1@25, F1@50 for \(\tau \in \{0.10, 0.25, 0.50\}\).
Per-class and per-video outputs: `compute_segment_metrics_detailed()`.

### Edit score

After collapsing consecutive duplicate labels:

\[
\mathrm{Edit} = 1 - \frac{d}{\max(n_{\mathrm{gt}}, n_{\mathrm{pred}}, 1)}
\]

where \(d\) is Levenshtein distance between segment label sequences.
Range: \([0, 1]\). Also returns raw Levenshtein distance.

Implementation: `evaluation.metrics.segment`.

## Boundary metrics

### Extraction

Boundaries are extracted from frame labels using the configured ontology transitions.
Each boundary record includes video id, `from_phase`, `to_phase`, frame index (first frame of destination phase), and ontology version.

Invalid transitions produce warnings; they are not silently accepted.

### Matching

**Monotonic one-to-one matching per transition type:**

For each transition key (e.g. `second_pull->turnover`):

1. Sort ground-truth and predicted boundaries by frame index.
2. Match each GT boundary to the nearest unused predicted boundary at or after the previous match.
3. Unmatched GT → missed; unmatched predictions → extra.

Transition types never cross-match.

### Reported boundary metrics (frames are canonical)

| Metric | Description |
|--------|-------------|
| MAE | Mean absolute frame error on matched boundaries |
| Median AE | Median absolute frame error |
| Std / max AE | Dispersion on matched boundaries |
| Matched / missed / extra counts | Detection counts per transition |
| Precision / recall / F1 | Boundary detection rates |
| Tolerance hit rate | Fraction of matched boundaries within ±\(\tau\) frames |

Aggregate **macro** (mean of per-transition MAE) and **micro** (pooled errors) values are both reported.

### FPS and milliseconds

**Policy:** `explicit_required_for_ms` (see `benchmark.yaml`).

- Frame errors are always valid.
- Millisecond conversion requires an **explicit per-video FPS** and provenance string.
- If FPS is absent, millisecond fields are omitted and `FpsRequiredError` is raised when conversion is requested directly.
- **Do not publish millisecond benchmark results until native FPS metadata are verified.**

Formula: \(\mathrm{ms} = \mathrm{frames} \times 1000 / \mathrm{fps}\).

Implementation: `evaluation.metrics.boundary`.

## Ontology integration

- Canonical evaluation ontology: `configs/ontology/seven_phase_v1.yaml`
- Derived B0 ontology: `configs/ontology/five_phase_knee_angle_v1.yaml`
- Mapping: `configs/ontology/seven_to_five_knee_angle_v1.yaml`

Original label arrays are never modified; mappings produce derived evaluations only.

High-level API: `evaluation.evaluate.evaluate_dataset_videos()`.

## Machine-readable output

JSON schema version `1.0.0`: `evaluation.results.BenchmarkEvaluationResult`.

Example:

```python
from snatch_phase_bench.evaluation.evaluate import evaluate_dataset_videos

result = evaluate_dataset_videos(
    {
        "athlete/clip.mp4": {
            "y_true": gt_labels,
            "y_pred": pred_labels,
            # "fps": 25.0,           # optional; required for ms fields
            # "fps_source": "manual", # required with fps
        },
    },
    model_identifier="ms_tcn_seed42",
)
print(result.to_json())
```

## Status

| Metric | Module | Status |
|--------|--------|--------|
| Window accuracy / F1 | `window.py` | Implemented |
| Frame aggregation + metrics | `frame.py` | Implemented |
| Edit score | `segment.py` | Implemented |
| Segmental F1@IoU | `segment.py` | Implemented |
| Boundary MAE (frames) | `boundary.py` | **Implemented** |
| Boundary MAE (ms) | `boundary.py` | Implemented (requires explicit FPS) |
| Boundary tolerance / P/R/F1 | `boundary.py` | **Implemented** |
| Per-transition breakdown | `boundary.py` + ontology | **Implemented** |
| JSON result schema | `results.py` | **Implemented** |
