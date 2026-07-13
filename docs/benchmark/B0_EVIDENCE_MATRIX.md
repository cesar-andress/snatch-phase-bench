# B0 evidence matrix — biomechanical audit

**Date:** 2026-07-13 (outcome accepted 2026-07-14)  
**Status:** **Accepted audit outcome — B0 frozen as exploratory reference**  
**Policy:** [`B0_EXPLORATORY_REFERENCE.md`](B0_EXPLORATORY_REFERENCE.md)  
**Purpose:** Document evidence reviewed before freezing B0 (no implementation).

**Authoritative sources used (project only):**

- [`docs/reproduction/AUTHOR_CLARIFICATIONS.md`](../reproduction/AUTHOR_CLARIFICATIONS.md)
- [`SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md) Part 5.1
- [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md) §7, EXP-B0, OD-1/OD-2
- [`configs/ontology/five_phase_knee_angle_v1.yaml`](../../configs/ontology/five_phase_knee_angle_v1.yaml)
- [`configs/ontology/seven_phase_v1.yaml`](../../configs/ontology/seven_phase_v1.yaml)
- Manuscript (`paper/sections/02_related_work.tex`, `03_dataset.tex`, `bibliography.bib`)
- Thesis integration notes (`docs/thesis/THESIS_INTEGRATION_REVIEW.md`, `MISSING_FROM_THESIS.md`)

**Not used:** external literature search, numeric thresholds not present in the above.

---

## 1. Evaluation ontologies

| Ontology | Transitions evaluated | Role for B0 |
|----------|----------------------|-------------|
| `five_phase_knee_angle_v1` | 5 (`setup→first_pull` … `turnover→recovery`) | **Target B0 output** per benchmark protocol |
| `seven_phase_v1` | 6 (includes separate `turnover→catch`, `catch→recovery`) | **Dataset ground truth**; B0 compared via mapped evaluation |

B0 is **not** expected to reproduce seven-class labels directly. Catch is merged into Turnover for five-phase comparison ([`seven_to_five_knee_angle_v1.yaml`](../../configs/ontology/seven_to_five_knee_angle_v1.yaml)).

---

## 2. Transition evidence matrix (five-phase B0 target)

Confidence levels: **High** = event type explicitly named in cited project literature; **Medium** = inferable but incomplete operational detail; **Low** = requires cues not available from MediaPipe pose alone; **None** = no project evidence for automated rule.

| Transition | Biomechanical event (project sources) | Landmarks / signals | Knee angle sufficient? | Hip required? | Bar required? | Shoulder required? | Confidence |
|------------|--------------------------------------|---------------------|------------------------|---------------|---------------|-------------------|------------|
| **setup → first_pull** | Onset of first pull / barbell separation from platform (author clarifications; Cao M1 begins at start position toward first maximal knee extension) | Knee extension onset; bar vertical motion | **Partial** — extension trend may precede visible separation | Possibly — whole-body lift | **Preferred** — author cites “bar separation”; Thiele literature in manuscript references bar-initiated timing | No | **Low** |
| **first_pull → transition** | Knee extension reverses to flexion (double-knee-bend / scoop onset). Thiele et al.: knees shift from extension to flexion. Cao M2: knee angle maximum → minimum | Hip–knee–ankle angle, angular velocity sign change | **Yes (event type)** — reversal/extremum logic | Helpful for stability | No for event definition | No | **High** (event); **Low** (fixed threshold) |
| **transition → second_pull** | Maximum knee flexion reached; second pull begins. Thiele et al.: transition completes at maximum knee flexion. Cao M2 end / M3 start | Knee flexion **maximum** (extremum) | **Yes (event type)** | Helpful | No for definition | No | **High** (event); **Low** (fixed threshold) |
| **second_pull → turnover** | Second maximal knee extension / explosive extension end. Thiele et al.: second pull ends at second maximum knee extension. Cao M3 ends at maximal vertical bar **velocity** (bar cue) | Knee extension **maximum**; alternatively bar velocity peak (unavailable) | **Partial** — literature also uses bar velocity (Cao); Thiele notes markerless error in second pull | Helpful | **Alternative cue in Cao** — not in MediaPipe | No | **Medium** (knee extremum); **Low** if bar velocity required |
| **turnover → recovery** | Overhead receipt, bar stabilized, then stand-up. Thiele/manuscript: turnover ends when bar stabilized in catch; knees extend after stabilization. Author: recovery after full hip/knee extension with bar stabilized overhead | Knee extension after catch; hip extension; overhead arm position | **Partial** — late extension only | **Yes** for recovery end (author) | **Yes** for turnover end (stabilization) | **Yes** for overhead fixation proxy | **Low** |

### Seven-phase-only transitions (not in five-phase B0 output)

| Transition | Event (project sources) | Knee-only? | Bar / shoulder? | Confidence for knee-only B0 |
|------------|-------------------------|------------|-----------------|---------------------------|
| **turnover → catch** | Bar flight, arm rotation, overhead receipt separated by author; Cao M4–M5 use bar height / falling velocity | No | **Bar path essential in Cao**; author uses visual receipt | **None** |
| **catch → recovery** | Fixation overhead before stand-up; author requires hip/knee extension + bar stable | Partial | Bar stability + hip extension | **Low** |

---

## 3. Source-specific findings

### Author clarifications (dataset labels)

- Boundaries were set by **manual visual identification** of multi-cue events (bar separation, knee reversals, bar path, overhead fixation)—**not** by an automated knee-angle rule.
- No numeric thresholds, joint triple, or smoothing parameters were documented.
- **Implication:** Dataset GT is **not** guaranteed to match any knee-only automaton; B0 is a **comparator heuristic**, not a label generator.

### Cao et al. (2022) — six-phase CV model

- Phases M1–M6 use **barbell kinematics and lower-limb joint angles** (author clarifications; manuscript §3).
- Documented M1 boundary: start position → first maximal knee extension.
- M3 boundary uses **maximal vertical bar velocity**; M4/M5 use **bar height / falling velocity** (project summary from integrated citation—not bar-free).
- **Implication:** Full Cao-style segmentation **cannot** be reproduced from MediaPipe pose alone without bar tracking.

### Chen et al. (2022)

- Project citation: competition-video **barbell-trajectory** analysis tradition (author clarifications; manuscript §3).
- **No phase boundary definitions or knee-angle rules** appear in project documentation.
- **Implication:** Chen et al. **does not support B0 threshold design**; contextual motivation only.

### Thiele et al. (2024) — cited in manuscript/bibliography

Manuscript and related work state that phase boundaries are operationalized through **knee-angle events**, including:

- Transition onset: extension → flexion.
- Transition end: maximum knee flexion.
- Second pull end: second maximum knee extension.
- Turnover end: related to bar stabilization in catch before knee re-extension.

**Not present in project files:** exact joint definitions, left/right selection, angle computation convention, numeric thresholds, smoothing, or pseudocode.

### Harbili & Alptekin (2014) — classical reference

- Cited as biomechanical reference for snatch phase vocabulary and kinematics (manuscript, literature foundation).
- **No operational automated boundary rules** extracted in project documentation.

### MSc thesis (integration review)

- **No rule-based / knee-angle baseline** was implemented.
- Future work mentions derived angles/velocities/bar path (M20)—**not realized** in thesis code.
- **Implication:** Thesis provides **no B0 thresholds or implementation evidence**.

### Benchmark protocol

- B0 = “rule-based **knee-angle threshold** segmenter” (wording in protocol).
- **OD-2 (OPEN):** exact joint triple + thresholds require biomechanics sign-off.
- Hypothesis: B0 degrades at turnover/catch and oblique views—acknowledges pose limits.

---

## 4. Measurable signals from MediaPipe Full (33 landmarks)

| Quantity | Computable from bundled keypoints? | Reliability (project evidence) |
|----------|-----------------------------------|------------------------------|
| Knee angle (hip–knee–ankle) | Yes — e.g. L: 23–25–27, R: 24–26–28 | Manuscript: markerless knee waveforms “recoverable to within a few degrees”; Thiele: **systematic offsets in second pull** |
| Hip angle (shoulder–hip–knee or trunk–thigh) | Yes — partial proxy | Hip/out-of-plane errors noted in markerless validity literature (manuscript §2) |
| Ankle angle | Yes — knee–ankle–foot indices | Same monocular limitations |
| Shoulder / elbow angles | Yes | Useful for overhead phases; **not defined as B0 boundaries** in project sources |
| Barbell position / velocity | **No** — not in MediaPipe pose CSVs | Required by Cao boundaries and author “bar separation / stabilization” cues |
| Center-of-mass proxy | Hip midpoint (approximate) | Not used in any project B0 rule |
| Angular velocity / acceleration | Temporal derivative of angles | **Requires smoothing** — parameters not documented |
| Vertical displacement (hip y) | Yes (image coordinates) | Not validated as phase boundary proxy in project sources |

---

## 5. Observability classification (MediaPipe Full only)

| Transition | Class | Why |
|------------|-------|-----|
| setup → first_pull | **Indirectly observable** | Extension trend detectable; true bar separation is **not** observable without bar |
| first_pull → transition | **Directly observable** (with error) | Knee extension→flexion reversal explicitly in Thiele/manuscript |
| transition → second_pull | **Directly observable** (with error) | Max knee flexion extremum explicitly in Thiele/manuscript |
| second_pull → turnover | **Indirectly observable** | Knee extension maximum supported; Cao prefers bar velocity peak |
| turnover → recovery (5-phase) | **Not observable** (knee-only) | Requires bar stabilization + merged catch/turnover semantics |
| turnover → catch (7-phase) | **Not observable** | Bar flight and receipt cues dominate (author, Cao) |
| catch → recovery (7-phase) | **Indirectly observable** | Hip/knee extension partially visible; bar stability **not** in pose |

---

## 6. B0 scope determination

### Can B0 detect all five phases?

**No — not with defensible knee-only rules alone** using only project evidence.

### Supported subset (event types only, not yet implementable without open decisions)

| Phase / transition | Support level |
|--------------------|---------------|
| Middle pull: `first_pull → transition → second_pull → turnover` (knee extrema / reversals) | **Partial** — event definitions supported; numeric/operational parameters **missing** |
| `setup` and `setup → first_pull` | **Weak** — lacks knee-only literature rule |
| `turnover → recovery` and late overhead phases | **Weak / not observable** without bar and stabilization cues |

### Recommended honest B0 scope (if implemented after decisions)

1. **Primary:** knee-angle **event detector** for three middle transitions (extension reversal, max flexion, max extension).
2. **Secondary / optional:** heuristic setup and recovery labelling with explicit **low-confidence** flag.
3. **Explicit non-claims:** B0 does **not** reproduce seven-phase catch/turnover split; comparison uses mapped five-phase evaluation.

---

## 7. Threshold evidence audit

| Proposed decision | Evidence class | Verdict |
|-------------------|----------------|---------|
| Use knee **extrema** (max/min) rather than fixed ° thresholds | Thiele operationalization in manuscript (max flexion, max extension events) | **Supported (event type)** |
| Any fixed knee angle in degrees (e.g., 90°, 120°) | — | **Arbitrary — REJECT** |
| Sign reversal (extension → flexion) for transition onset | Thiele/manuscript | **Supported (event type)** |
| Smoothing window / cutoff frequency | — | **Unresolved** |
| Left vs right vs average knee angle | — | **Unresolved (OD-2)** |
| 2D image-plane vs 3D landmark angle | MediaPipe z documented as 2.5D; limitations in manuscript | **Unresolved** |
| Bar velocity peak for second_pull → turnover | Cao et al. | **Supported in literature but NOT feasible** on pose-only inputs |
| Bar stabilization for turnover end | Thiele/manuscript + author | **Required event — NOT feasible** on pose-only inputs |

---

## 8. Verdict

| Question | Answer |
|----------|--------|
| Is there biomechanical motivation for B0? | **Yes** — benchmark protocol + Thiele/Harbili framing |
| Are phase **event types** for middle pull supported? | **Partially yes** |
| Are **numeric thresholds** supported? | **No** |
| Can B0 be implemented **now** without arbitrary choices? | **No — STOP before coding** |
| Minimum missing evidence | OD-2 joint definition; smoothing; setup/onset rule; late-phase rule without bar; validation against mapped labels |

---

## 9. Reviewer #2 — “Why trust this baseline?”

**Draft answer (honest):**

> B0 is included not as ground truth but as the heuristic the biomechanics literature already uses to *define* phase vocabulary: knee-extension reversals and extrema during the pull (Thiele et al., 2024; Harbili & Alptekin, 2014). SnatchPhaseBench fixes the same MediaPipe inputs and athlete-disjoint splits for learned models and reports **where** a transparent knee-angle event detector agrees or disagrees with expert visual labels—especially at setup onset and overhead phases where bar and stabilization cues dominate. We do **not** claim B0 matches the seven-class expert annotations phase-for-phase; five-phase mapped evaluation makes that comparison explicit. If B0 ties or beats learned models on boundary timing, that is a scientifically important finding, not a failure of the benchmark.

---

## Related documents

- [`B0_IMPLEMENTATION_SPECIFICATION.md`](B0_IMPLEMENTATION_SPECIFICATION.md) — blocked spec (no thresholds)
- [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md) — OD-2 open decision
