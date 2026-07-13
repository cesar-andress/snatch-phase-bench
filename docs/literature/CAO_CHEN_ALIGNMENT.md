# Cao–Chen alignment with SnatchPhaseBench

**Status:** Canonical literature-alignment reference  
**Date:** 2026-07-14  
**Purpose:** Document how the SnatchPhaseBench seven-class ontology and annotation protocol relate to the primary scientific sources used during MSc dataset construction (Cao et al., 2022; Chen et al., 2022), author clarifications, and the frozen benchmark artifacts.

**Policy:** The released dataset annotations remain canonical. This document **justifies** design choices; it does **not** redefine the ontology, protocol, or labels.

**Primary sources (read in full):**

| Source | File | Role |
|--------|------|------|
| Cao et al. (2022) | `/home/cesar/papers/Paper_TFM-main/Cao 2022.pdf` | Operational six-phase (M1–M6) division from 3D barbell + lower-limb kinematics |
| Chen et al. (2022) | `/home/cesar/papers/Paper_TFM-main/Chen 2022.pdf` | Six-phase CV vocabulary for competition barbell-trajectory analysis |
| Author clarifications | `docs/reproduction/AUTHOR_CLARIFICATIONS.md` | Dataset construction decisions (Adrián Cardona Ruiz) |
| Ontology | `configs/ontology/seven_phase_v1.yaml` | Frozen seven-class benchmark labels |

---

## Executive summary

SnatchPhaseBench adopts the **six-phase computer-vision decomposition** shared by Cao et al. and Chen et al., adds an explicit **Setup** phase, and keeps **Turnover** and **Catch** as separate supervised classes. Phase names align with Chen's coaching/CV vocabulary; several **boundary operationalizations** follow Cao's barbell-and-joint kinematic events, but annotations were produced by **expert visual inspection** on monocular competition video—not by re-implementing Cao's SIMI pipeline or Chen's barbell tracker.

**Verdict:** The benchmark ontology and protocol are **scientifically justified** as a CV-motivated, coaching-aligned extension of established snatch phase literature. Documented differences from Cao/Chen are **intentional** (Setup phase, seven-class granularity, MediaPipe-only inputs, multi-athlete competition footage) and do not invalidate the frozen labels.

---

## 1. Phase taxonomy comparison

### 1.1 Cao et al. (2022) — six phases M1–M6

Cao et al. divide the snatch into **six movement phases** according to **barbell trajectory and lower-limb joint angles**, analysed on a single world-record athlete with 3D SIMI motion capture (50 Hz, 17 body markers) during the 2019 World Championships.

| Code | Phase (paper) | Primary segmentation logic |
|------|---------------|----------------------------|
| M1 | First pulling stage | Start position → **first maximal knee extension angle** |
| M2 | Transition / double-knee-bend | Knee angle from **maximum to minimum** |
| M3 | Second pull (explosive) | End of M2 → **maximal vertical rising velocity of barbell** |
| M4 | Turnover / flight (implicit) | End of M3 → **maximal vertical height of barbell** |
| M5 | Catch descent (implicit) | End of M4 → **maximal vertical falling velocity of barbell** |
| M6 | Receiving / squat | End of M5 → **squat position** |

Cao does **not** name phases with coaching strings (`first pull`, etc.) but maps them in discussion to first pull, second pull (M3), and catch (M5–M6). M1 **includes** the static start position; there is no separate pre-pull Setup class.

### 1.2 Chen et al. (2022) — six named phases

Chen et al. cite Baumann et al. (1988) and prior barbell-trajectory work and list six **named** phases used in kinematic analysis:

1. **First pull**
2. **Transition phase**
3. **Second pull**
4. **Turnover phase**
5. **Catch phase**
6. **Stand phase**

Their contribution is **not** phase annotation: they build a VGG16 classifier on **barbell trajectory images** to predict four expert categories (goodlift/nolift × good/normal posture) from 481 women's competition attempts. The six phases appear as **conceptual scaffolding** for barbell kinematics (Figure 1); the paper does **not** define frame-wise boundaries, release a phase-labelled dataset, or specify transition events.

### 1.3 SnatchPhaseBench — seven supervised phases (+ unlabeled)

| ID | Phase | Primary source | Notes |
|----|-------|----------------|-------|
| 0 | `unlabeled` | Adrián (annotation utility) | Excluded at window center during B1 training |
| 1 | `setup` | **Adrián** | Active coached start before bar separation; not a separate class in Cao/Chen |
| 2 | `first_pull` | Cao M1 + Chen | Bar separation through first-pull mechanics |
| 3 | `transition` | Cao M2 + Chen | Double-knee-bend / scoop |
| 4 | `second_pull` | Cao M3 + Chen | Explosive extension; ontology text cites maximal upward bar velocity (Cao M3 end) |
| 5 | `turnover` | Cao M4–M5 + Chen | Bar flight and arm rotation under the bar |
| 6 | `catch` | Cao M5–M6 + Chen | Overhead receipt and fixation |
| 7 | `recovery` | Cao M6 + Chen **stand phase** | Stand-up; Adrián extends until full hip/knee extension with bar stabilized |

### 1.4 Provenance matrix

| Design element | Cao et al. | Chen et al. | Adrián / SnatchPhaseBench |
|----------------|------------|-------------|---------------------------|
| Six-phase CV vocabulary | Defines M1–M6 operationally | Names six phases (Figure 1) | Adopted as backbone |
| Explicit Setup class | No (start within M1) | No | **Added** — coached active start before separation |
| Turnover vs catch split | M4/M5 bar-kinematic substeps | Separate named phases | **Kept separate** in seven-class labels |
| Stand / recovery | M6 → squat position | Stand phase | `recovery` with stricter end criterion (full extension + bar stable) |
| Frame-wise phase labels | Case study parameters only | Not provided | **208 videos**, expert visual annotation |
| Input modality | 3D markers + bar CoG | 2D barbell trajectory | **MediaPipe pose** (fixed upstream) |

---

## 2. Phase boundary definitions

### 2.1 Cao et al. — kinematic boundaries (bar + joints)

From Cao Figure 3 and Table 1 captions (Applied Sciences 12:9679):

| Boundary | Operational definition (Cao) |
|----------|------------------------------|
| Start → M1 | Implicit: lift begins from start position |
| M1 → M2 | **First maximal knee extension angle** |
| M2 → M3 | **Knee angle minimum** (end of double-knee-bend) |
| M3 → M4 | **Maximal vertical rising velocity of barbell** |
| M4 → M5 | **Maximal vertical height of barbell** |
| M5 → M6 | **Maximal vertical falling velocity of barbell** |
| M6 end | **Squat position** (receiving depth) |

Cao boundaries are **continuous kinematic extrema** on synchronised bar and joint signals. They require bar centre-of-gravity tracking and calibrated 3D joint angles.

### 2.2 Chen et al. — no operational boundaries

Chen et al. do not specify how to place boundaries between the six phases. They rely on prior biomechanics literature (reference [2]: Baumann et al., 1988) for the phase list and focus expert effort on **trajectory quality scoring**, not temporal segmentation.

### 2.3 SnatchPhaseBench — visual biomechanical boundaries

From `AUTHOR_CLARIFICATIONS.md` and `seven_phase_v1.yaml`:

| Transition | Benchmark boundary criterion | Literature anchor |
|------------|------------------------------|-------------------|
| `setup` → `first_pull` | **Onset of barbell separation** from platform | Adrián; Cao M1 spans start → first max knee extension (separation is earlier) |
| `first_pull` → `transition` | **First knee-extension reversal** toward flexion (scoop onset) | Cao M1→M2; Chen transition; Kim/Lee extension–flexion–extension pattern cited by Cao |
| `transition` → `second_pull` | **Maximum knee flexion** / second pull onset | Cao M2 end; aligns with double-knee-bend minimum |
| `second_pull` → `turnover` | Explosive extension complete; **bar path inflection toward flight** (priority boundary) | Cao M3 end (max rising bar velocity); also discussed as second knee extension maximum in validation literature |
| `turnover` → `catch` | **Overhead receipt** — bar stabilized in catch position | Cao M4–M5 region (height peak → falling velocity peak); Chen catch phase |
| `catch` → `recovery` | Fixation complete; **stand-up begins** | Cao M5→M6; Chen stand phase onset |
| End of `recovery` | **Full hip and knee extension** with bar stabilized overhead | Adrián stricter than Cao M6 squat position alone |

**Annotation method:** one expert annotator, frame-by-frame, visually identifying multi-cue events; cross-athlete consistency prioritised over clip-local optima; ambiguous frames resolved to the nearest visually consistent neighbour.

### 2.4 Intentional differences from Cao boundaries

| Topic | Cao | SnatchPhaseBench | Justified? |
|-------|-----|------------------|------------|
| Setup onset | Included in M1 | Separate `setup` ending at bar separation | **Yes** — coaching distinguishes braced start from first pull |
| M3 vs M4 split | Bar velocity peak vs height peak | `second_pull` → `turnover` at explosive-extension / flight onset | **Yes** — finer coaching granularity; ontology cites Cao M3 end conceptually |
| M5 vs M6 split | Falling-velocity peak vs squat | Separate `catch` and `recovery` | **Yes** — Chen names both; Adrián separates receipt from stand-up |
| Recovery end | Squat position | Full extension + bar stable | **Yes** — aligns with IWF “arms and legs straight” and coaching stand completion |
| Signal source | 3D bar + joints | Monocular video, visual cues | **Yes** — benchmark constraint; labels are expert visual GT, not Cao automaton output |

---

## 3. Observable biomechanical events per transition

Events are listed as **annotator-visible cues** on competition video. Cao events marked with † require bar tracking or 3D joints not directly available in fixed MediaPipe inputs.

| Transition | Observable events (SnatchPhaseBench) | Cao et al. event | Chen et al. |
|------------|--------------------------------------|------------------|-------------|
| `setup` → `first_pull` | Bar leaves platform; hip/knee extension initiates lift | M1 begins at start; first max knee extension is **later** boundary | First pull onset (conceptual) |
| `first_pull` → `transition` | Knee extension slows/reverses; torso remains over bar; scoop posture | † M1→M2: first max knee extension | Transition phase |
| `transition` → `second_pull` | Deepest knee/hip flexion; explosive triple extension begins | M2→M3: knee minimum | Second pull onset |
| `second_pull` → `turnover` | Peak extension; bar acceleration inflects; elbows rise, feet may leave platform | † M3 end: max rising bar velocity | Turnover onset |
| `turnover` → `catch` | Arms rotate under bar; bar descends; lifter moves under bar to overhead position | † M4 peak height; M5 peak downward velocity | Catch phase |
| `catch` → `recovery` | Bar fixed overhead; squat depth achieved; upward movement to stand begins | M5→M6: max falling velocity → squat | Stand phase onset |
| End `recovery` | Hips/knees locked; bar motionless overhead | M6 end: squat position (weaker match) | Stand completion |

Cao's discussion additionally highlights **extension–flexion–extension** knee pattern in M1–M3 (5.62° knee flexion in M2) and **rapid lower-limb flexion in M5–M6** — patterns an annotator can approximate from pose even without bar CoG.

---

## 4. Implications for MediaPipe-based annotation

### 4.1 What MediaPipe provides

- 33 body landmarks × (x, y, z) per frame (MediaPipe 0.10.30 Full), fixed upstream in benchmark v1.
- **No barbell keypoints** in the shipped feature matrix.

### 4.2 Alignment with Cao/Chen signal requirements

| Literature requirement | Available in MediaPipe pose? | Impact on labels |
|------------------------|------------------------------|------------------|
| Knee/hip/ankle angles (Cao) | **Approximate** via landmark geometry | Supports pull-phase boundaries; Thiele et al. report usable knee-angle agreement with errors largest in second pull |
| Bar vertical velocity/height (Cao M3–M5) | **No** (unless inferred from wrist/elbow proxies) | Annotator uses **visual bar motion**, not Cao extrema |
| Bar–body CoG distance (Cao stability) | **No** | Not used in annotation protocol |
| Chen barbell trajectory features | **No** in v1 features | Chen motivates phase vocabulary, not pose-only rules |

### 4.3 Annotation vs automation gap

- **Dataset GT** = expert visual multi-cue labelling (`AUTHOR_CLARIFICATIONS.md`).
- **Cao automaton** = bar + joint extrema on 3D capture — cannot be reproduced knee-only or pose-only without additional assumptions (`docs/benchmark/B0_EVIDENCE_MATRIX.md`).
- **Chen pipeline** = trajectory CNN for lift quality — no phase labels to compare against.

**Conclusion:** MediaPipe is appropriate as a **fixed input representation** for learned segmenters (B2) trained to predict visually defined expert phases. It is **not** sufficient to derive Cao-identical boundaries algorithmically without bar tracking. This gap is documented and motivates freezing B0 as exploratory reference only.

### 4.4 Phase-specific pose sensitivity

| Phase | Pose reliability concern | Literature support |
|-------|-------------------------|-------------------|
| `setup` | Stable; limited motion | Low risk |
| `first_pull`, `transition`, `second_pull` | Knee-angle events partially recoverable | Cao M1–M3; Thiele knee operationalization |
| `turnover`, `catch` | Arm rotation, overhead depth, bar–body relation | Cao M4–M6 bar-dependent; Thiele notes markerless error in second pull / overhead |
| `recovery` | Extension end requires full-body + bar stability cue | Adrián criterion exceeds knee-only observability |

---

## 5. Benchmark implications

### 5.1 Ontology remains canonical

- Primary evaluation uses `seven_phase_v1.yaml` against expert frame labels.
- Six Cao/Chen phases map to IDs 2–7; `setup` is the deliberate seventh supervised class.
- No relabelling is proposed or permitted by this document.

### 5.2 Boundary metrics

The six priority transitions in `seven_phase_v1.yaml` (`second_pull`→`turnover` marked `priority: true`) reflect coaching-critical timing where Cao uses bar velocity/height extrema and Adrián uses visual flight/receipt cues. Boundary MAE is the **primary B2 endpoint** because frame accuracy saturates on long phases (`BENCHMARK_PROTOCOL.md`, manuscript §5).

### 5.3 B0 (knee-angle exploratory reference)

| Transition | Cao/Chen support for knee-only rule | B0 status |
|------------|-------------------------------------|-----------|
| `first_pull` → `transition` | **High** event type (Cao M1→M2) | Exploratory only — thresholds undocumented |
| `transition` → `second_pull` | **High** (Cao M2 end) | Exploratory only |
| `second_pull` → `turnover` | **Partial** — Cao prefers bar velocity | Frozen — cannot implement without bar cue |
| `turnover` → `catch`, `catch` → `recovery` | **Low** — bar/overhead essential in Cao | Frozen |
| `setup` → `first_pull` | **Low** — bar separation preferred | Frozen |

Chen et al. **does not** support B0 threshold design.

### 5.4 Learned segmenters (B2)

MS-TCN and successors are justified to **learn mappings** from pose sequences to expert visual phases — the same pragmatic path Chen et al. take for bar trajectory quality, but with **dense phase supervision** Adrián added. Training/evaluation protocol unchanged.

### 5.5 Athlete-disjoint splits

Cao: N=1 elite athlete. Chen: 481 attempts, no athlete-disjoint phase benchmark. SnatchPhaseBench: 208 videos, 52 athletes, fixed split — necessary because inter-athlete stylistic variation is explicitly noted as a limitation in Cao's case-study design.

---

## 6. Manuscript implications

### 6.1 Claims that are now better supported

1. Seven-class taxonomy extends **Chen's six named phases** plus **Adrián's Setup**, consistent with Cao's pull-phase kinematics.
2. Turnover/catch separation is aligned with **Chen's named phases** and Cao's **M4–M6 bar-kinematic substeps**, not an arbitrary split.
3. Annotation protocol (visual biomechanical events) is the **operational substitute** for Cao's instrumented extrema when only monocular video is available — same competition context as Chen.
4. B0 freeze is justified: Cao boundaries **require bar signals**; Chen **does not define** automatable boundaries.

### 6.2 Wording to avoid

- Do **not** claim labels were generated by applying Cao's M1–M6 rules to MediaPipe.
- Do **not** cite Chen et al. as a phase-annotation protocol paper.
- Do **not** imply numerical equivalence between Cao's single-athlete extrema and multi-athlete visual boundaries.

### 6.3 Recommended manuscript touchpoints

| Section | Update |
|---------|--------|
| Related work | Distinguish Cao (operational kinematics) vs Chen (CV vocabulary + trajectory ML) vs SnatchPhaseBench (expert visual dense labels) |
| Methods / annotation | Cross-reference Cao boundary events as **literature motivation**, Adrián protocol as **canonical GT** |
| Experimental protocol | Note boundary metrics evaluate agreement with **visually defined** transitions inspired by, but not identical to, Cao extrema |

---

## Appendix A — Side-by-side phase mapping

```
Chen (6)          Cao (6)              SnatchPhaseBench (7)
────────          ───────              ──────────────────────
[implicit]        [start in M1]        setup
first pull        M1                   first_pull
transition        M2                   transition
second pull       M3                   second_pull
turnover          M4 (+ early M5)      turnover
catch             M5 (+ late M5)       catch
stand phase       M6                   recovery
```

## Appendix B — Key Cao quantitative anchors (case study)

From Cao Table 1 (single 73 kg world-record attempt): DTM1 = 0.38 s, DTM2 = 0.12 s, DTM3 = 0.16 s, VBM3 = 1.90 m/s, HBM4 = 125.10 cm, knee flexion in M2 = 5.62°. These illustrate **scale and event types** but must **not** be used as universal thresholds for the multi-athlete benchmark.

## Appendix C — Chen study scope (not phase labelling)

- 481 snatch attempts, four Taiwan women's competitions (2018–2019).
- Barbell trajectories from Hsu et al. tracking; **five experts** label **four outcome/posture categories**, not phases.
- VGG16 trajectory classifier: ~71.11% accuracy.
- Six-phase figure is **conceptual** (Baumann et al., 1988 lineage).

---

## References (internal)

- `docs/reproduction/AUTHOR_CLARIFICATIONS.md`
- `configs/ontology/seven_phase_v1.yaml`
- `docs/benchmark/B0_EVIDENCE_MATRIX.md`
- `docs/benchmark/B0_EXPLORATORY_REFERENCE.md`
- Cao, W. et al. (2022). *Applied Sciences* 12(19):9679. DOI: 10.3390/app12199679
- Chen, J.-S. et al. (2022). ICAAI 2022. DOI: 10.1145/3571560.3571567
