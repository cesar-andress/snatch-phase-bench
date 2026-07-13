# B0 implementation specification (blocked)

**Date:** 2026-07-13  
**Status:** **BLOCKED — do not implement until open decisions resolved**  
**Evidence audit:** [`B0_EVIDENCE_MATRIX.md`](B0_EVIDENCE_MATRIX.md)

This document specifies the **intended** rule-based baseline architecture. It intentionally **excludes numeric thresholds** and other unsupported parameters.

---

## 1. Implementation gate

B0 coding may begin only when **all** items in §8 are resolved with documented evidence or signed benchmark decisions.

Until then, the repository contains:

- Ontology + mapping (`configs/ontology/`)
- Metric evaluator (`evaluation/metrics/boundary.py`, `evaluation/evaluate.py`)
- **No** `rule_knee_angle` model or `configs/benchmark/rule_knee_angle.yaml`

---

## 2. Purpose

| Item | Specification |
|------|---------------|
| Tier | B0 — primary non-learned comparator |
| Scientific role | Test whether learned segmenters improve over knee-angle **event heuristics** used in biomechanics literature |
| Output ontology | `five_phase_knee_angle_v1` (six supervised labels including setup) |
| Comparison to dataset | Mapped evaluation via `seven_to_five_knee_angle_v1`; seven-class labels **never modified** |
| Inputs | Precomputed MediaPipe 0.10.30 Full CSVs (same as B1/B2) |

---

## 3. Inputs

| Input | Source | Notes |
|-------|--------|-------|
| Pose landmarks | `keypoints/<athlete>/*.csv` | 33 × (x, y, z) per frame |
| Video id | `video_relpath` | One sequence per evaluation |
| Ontology | `configs/ontology/five_phase_knee_angle_v1.yaml` | Output phase names |
| Optional mapping | Only for evaluation against seven-class GT | Applied in metric layer, not in B0 labeller |

**Not available as inputs:** barbell position, multi-view geometry, MOCAP, instrumented force.

---

## 4. Outputs

| Output | Format |
|--------|--------|
| Per-frame phase labels | Integer ids under `five_phase_knee_angle_v1` |
| Per-frame confidence (recommended) | Optional scalar per frame marking low-confidence segments |
| Boundary events | Derived via `evaluation.boundaries.extract_boundaries_from_labels` |
| Evaluation JSON | `evaluation.results.BenchmarkEvaluationResult` with `model_identifier: b0_rule_knee_angle_v*` |

---

## 5. Required landmarks (proposed — OD-2 unresolved)

MediaPipe BlazePose indices (project convention to be fixed):

| Joint chain | Landmark indices (L / R) |
|-------------|--------------------------|
| Knee angle | Hip 23/24, knee 25/26, ankle 27/28 |
| Hip angle (optional) | Shoulder 11/12, hip 23/24, knee 25/26 |
| Ankle angle (optional) | Knee 25/26, ankle 27/28, foot index 31/32 |

**Open decisions:**

- Single leg vs bilateral average vs max deviation
- 2D angle in image plane vs use of z coordinate
- Handling missing/occluded landmarks (frozen baseline uses interpolation — apply same or stricter?)

---

## 6. Required preprocessing

| Step | Requirement | Status |
|------|-------------|--------|
| Align frame indices with label CSVs | Same timeline as dataset | **Defined** |
| Gap filling | Match frozen pipeline or document divergence | **Unresolved** |
| Root normalization | Not used in frozen B1 features; B0 may use raw or hip-centered angles | **Unresolved** |
| Temporal smoothing | Required before derivatives/extrema | **Parameters missing** |
| FPS | Not required for frame-based B0; ms metrics need explicit FPS per video | **Policy defined** in `benchmark.yaml` |

---

## 7. Signal processing (no numeric values)

### Primary signal

- **Knee flexion/extension angle** time series θ_knee(t)

### Derived signals (optional)

- First derivative dθ/dt for sign-change detection (extension ↔ flexion)
- Local extrema detection for max flexion / max extension events

### Event types aligned with literature (no thresholds)

| Event | Detection pattern | Literature basis |
|-------|-------------------|------------------|
| Transition onset | Sign change: knee extension → flexion | Thiele et al.; manuscript §2 |
| End of transition | Local **minimum** knee angle | Thiele et al.; manuscript §2 |
| End of second pull | Local **maximum** knee angle (second peak) | Thiele et al.; manuscript §2 |

**Explicitly not supported without bar tracking:**

- Bar separation (setup → first_pull) per author/Cao
- Bar velocity peak (Cao M3 end)
- Bar stabilization (turnover end)

---

## 8. State machine (conceptual)

```text
[SETUP] --(onset rule TBD)--> [FIRST_PULL]
[FIRST_PULL] --(knee ext->flex reversal)--> [TRANSITION]
[TRANSITION] --(knee flexion minimum)--> [SECOND_PULL]
[SECOND_PULL] --(knee extension maximum)--> [TURNOVER]
[TURNOVER+Catch merged] --(recovery rule TBD)--> [RECOVERY]
```

| State | Entry condition | Evidence status |
|-------|-----------------|-----------------|
| SETUP | Clip start until first-pull onset | **Unresolved onset rule** |
| FIRST_PULL | After onset until extension→flexion reversal | **Event supported** |
| TRANSITION | Reversal until max flexion | **Event supported** |
| SECOND_PULL | Max flexion until max extension | **Event supported** |
| TURNOVER | Max extension until recovery rule fires | **Partial** — extension end supported; exit **not** supported knee-only |
| RECOVERY | Until clip end | **Weak** — author defines end by hip/knee extension + bar stable (bar N/A) |

---

## 9. Failure modes (expected)

| Mode | Cause | Mitigation in reporting |
|------|-------|-------------------------|
| Oblique camera | Knee angle projection error | Per-view analysis; benchmark protocol robustness EXP |
| Occlusion at catch | Landmark dropout | Confidence flags; known limitation in protocol hypothesis |
| Second-pull timing error | Thiele: markerless offset in second pull | Highlight `second_pull→turnover` boundary MAE |
| Double extrema / noise | Short-phase athlete variability | Smoothing + minimum prominence (parameters TBD) |
| Setup misalignment | No bar signal | Report setup transition separately; expect high error |
| Phase collapse | Missing late-phase rule | Document low recall for turnover/recovery |

---

## 10. Known limitations (must appear in paper)

1. B0 uses **pose-only** signals; literature and author labels also use **bar path** and visual stabilization.
2. Expert dataset labels are **visual multi-cue**, not knee-automaton outputs.
3. Seven-class catch/turnover split is **not** produced by B0; evaluation is **mapped**.
4. No numeric thresholds are justified yet; implementation would otherwise be arbitrary.
5. Millisecond boundary metrics require verified FPS (not available dataset-wide).

---

## 11. Configuration file (placeholder)

When unblocked, create `configs/benchmark/rule_knee_angle.yaml`:

```yaml
# PLACEHOLDER — do not populate thresholds until B0_EVIDENCE_MATRIX gaps closed
model:
  registry: rule_knee_angle
  version: B0-v0.0.0-blocked
ontology: five_phase_knee_angle_v1
signals:
  primary: knee_angle
  # joint_triple: TBD
  # leg_policy: TBD
smoothing:
  # method: TBD
  # window: TBD
events:
  # extremum_prominence: TBD
  # min_phase_duration_frames: TBD
onset:
  # setup_to_first_pull: TBD  # requires decision — not knee-only in literature
recovery:
  # turnover_to_recovery: TBD  # requires bar/stabilization proxy or weak knee-only fallback
```

---

## 12. Testing plan (when unblocked)

| Test | Type |
|------|------|
| Synthetic angle waveforms with known extrema | Unit |
| Middle-pull transitions on mini ontology fixtures | Unit |
| Full five-phase sequence vs mapped GT (small hand-checked clip) | Integration |
| Determinism | Unit |
| Original seven-class labels unchanged after evaluation mapping | Regression |
| No default FPS in ms metrics | Regression |

---

## 13. Open decisions blocking implementation

| ID | Decision | Owner | Evidence needed |
|----|----------|-------|-----------------|
| OD-2a | Joint triple + 2D/3D angle definition | Biomechanics + benchmark | Written rule + citation or calibration note |
| OD-2b | Leg selection / aggregation | Benchmark | Sensitivity analysis or literature convention |
| OD-2c | Smoothing / extremum detection parameters | Benchmark | Reproducible defaults; not arbitrary |
| OD-B0-1 | Setup → first_pull onset without bar | Domain expert | Accept knee-only proxy **or** defer B0 start to first supported transition |
| OD-B0-2 | Turnover → recovery without bar stabilization | Domain expert | Accept knee re-extension only **or** mark late phases unsupported |
| OD-B0-3 | Validation against mapped labels | Benchmark | Agreement study on subset; expected failure regions documented |

---

## 14. Verdict

**B0 cannot be implemented in the repository today** without introducing unsupported numeric or procedural choices.

**Next step:** Resolve §13 through domain sign-off or a deliberately narrow, explicitly limited B0 scope (e.g., middle-pull transitions only) documented as a **partial heuristic baseline**—not a full five-phase segmenter.

---

## Related documents

- [`B0_EVIDENCE_MATRIX.md`](B0_EVIDENCE_MATRIX.md)
- [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md) §7.1, OD-2
- [`REMAINING_BLOCKERS.md`](../reproduction/REMAINING_BLOCKERS.md)
