# Inter-annotator agreement (IAA) protocol — SnatchPhaseBench

**Status:** subset frozen; **agreement not computed** (annotator-2 labels pending).  
**Study id:** `snatchphasebench_iaa_v1`  
**Date frozen:** 2026-07-22  

This document prepares the reliability study. It does **not** report agreement numbers.

Canonical subset file: [`analysis/iaa/subset_manifest.json`](../../analysis/iaa/subset_manifest.json).

---

## 0. Scientific goal

Measure **inter-annotator agreement on temporal phase boundaries** for a representative subset of snatch attempts.

Labels in the released benchmark were produced by a **single expert annotator**. Boundary MAE is a primary model endpoint; without a reliability study, that endpoint’s ceiling is unknown. This protocol defines how a second annotator will label the subset and how agreement will be computed **after** those labels exist.

**Experimental emphasis:** boundary timing (continuous frame indices), not frame-wise categorical agreement on long homogeneous phases.

---

## 1. Video list (n = 20)

Selection maximises diversity across athletes, weight classes / broadcast-session proxies (clip-id buckets), outcomes (`ok` / `fail`), movement quality, and difficulty, and spans train / val / test athlete splits. Competition name is not stored as metadata; weight class + clip-id range are used as session proxies from Weightlifting House extractions.

| # | `video_relpath` | Split | Class | Outcome | Difficulty | Why selected |
|--:|-----------------|-------|-------|---------|------------|--------------|
| 1 | `campbell/snatch_-+86kg_campbell_emily_jade_i1_ok_000168.mp4` | val | -+86kg | ok | easy | Long women’s superheavy success (11 s, 1080p); clear catch. |
| 2 | `ficco/snatch_-88kg_ficco_cristiano_giuseppe_i1_ok_000021.mp4` | train | -88kg | ok | easy | Clean men’s -88 kg complete lift; early session proxy. |
| 3 | `cambei/snatch_-53kg_cambei_mihaela_valentina_i1_ok_000118.mp4` | train | -53kg | ok | easy | Women’s -53 kg success; mid session proxy. |
| 4 | `koanda/snatch_-86kg_koanda_solfrid_eila_amena_i1_ok_000200.mp4` | train | -86kg | ok | easy | Women’s -86 kg success; late clip-id session. |
| 5 | `montero/snatch_-48kg_montero_ramos_ludia_m_i2_ok_000149.mp4` | test | -48kg | ok | easy | Lightest women’s class; held-out test athlete. |
| 6 | `he/snatch_-71kg_he_yueji_i2_ok_000077.mp4` | test | -71kg | ok | easy | Women’s -71 kg complete test-split success. |
| 7 | `sahakyan/snatch_-71kg_sahakyan_gor_i3_ok_000077.mp4` | val | -71kg | ok | easy | Men’s -71 kg long success; sex-matched pair with `he`. |
| 8 | `mosquera/snatch_-65kg_mosquera_valencia_f_i1_ok_000079.mp4` | val | -65kg | ok | easy | Successful -65 kg counterpart to a failed -65 kg clip. |
| 9 | `moeini/snatch_-94kg_moeini_sedeh_alireza_i3_ok_000018.mp4` | test | -94kg | ok | hard | Difficult athlete for models; 720p; atypical timing. |
| 10 | `friedrich/snatch_-94kg_friedich_raphael_i1_ok_000001.mp4` | test | -94kg | ok | hard | 720p; incomplete supervised-phase coverage on an `ok` lift. |
| 11 | `mueller/snatch_-88kg_mueller_lucas_i2_ok_000026.mp4` | val | -88kg | ok | hard | `ok` but only five supervised phases; 2-frame transition. |
| 12 | `ozkan/snatch_-53kg_ozkan_cansel_i2_fail_000122.mp4` | train | -53kg | fail | mixed | Fail that still contains all seven supervised phases. |
| 13 | `abokhala/snatch_-94kg_abokhala_karim_i3_fail_000005.mp4` | train | -94kg | fail | hard | Short 720p truncated fail. |
| 14 | `chen/snatch_-53kg_chen_guan_ling_i2_fail_000119.mp4` | train | -53kg | fail | hard | Shortest clip (3 s); 2-frame transition. |
| 15 | `muthupandi/snatch_-65kg_muthupandi_raja_i1_fail_000081.mp4` | train | -65kg | fail | hard | Failed -65 kg with 2-frame transition. |
| 16 | `rivas/snatch_-86kg_rivas_mosquera_valeria_i3_fail_000196.mp4` | train | -86kg | fail | hard | Late-session women’s -86 kg truncated fail. |
| 17 | `adventino/snatch_-65kg_adventino_geovani_leonardo_i2_fail_000097.mp4` | val | -65kg | fail | hard | Val-split failed -65 kg pair for `mosquera`. |
| 18 | `alipour/snatch_-94kg_alipour_ali_i1_fail_000006.mp4` | val | -94kg | fail | hard | 720p truncated fail in val. |
| 19 | `karapetyan/snatch_-88k_karapetyan_andranik_i1_fail_000042.mp4` | train | -88k | fail | hard | Weight-class spelling variant; truncated fail. |
| 20 | `rustamov/snatch_-71k_rustamov_isa_i2_fail_000057.mp4` | test | -71k | fail | hard | Test-split truncated fail; `-71k` spelling variant. |

**Diversity snapshot:** 20 athletes; 10 weight-class strings; 11 `ok` / 9 `fail`; splits ≈ 9 train / 6 val / 5 test; includes 720p and 1080p.

Prepare the annotator-2 work package (blank templates, **no** ground-truth labels):

```bash
python scripts/prepare_iaa_workpack.py
```

---

## 2. Annotation instructions (annotator 2)

### 2.1 Independence (mandatory)

1. Work **independently**.
2. Do **not** view existing SnatchPhaseBench labels (`master_*`, per-athlete CSVs, thesis figures with GT overlays).
3. Do **not** view model predictions, confusion plots, or failure analyses for these videos.
4. Do **not** discuss specific frame decisions with annotator 1 until the subset is fully labelled and files are deposited.
5. You may read this protocol and the ontology definitions below.

### 2.2 Ontology (seven supervised phases + unlabeled)

| ID | Name | Meaning |
|---:|------|---------|
| 0 | `unlabeled` | Pre-roll / post-roll / undefined; not a coached phase |
| 1 | `setup` | Active braced start **before** barbell leaves the platform |
| 2 | `first_pull` | From bar separation through first knee-extension peak region |
| 3 | `transition` | Scoop / double-knee-bend between pulls |
| 4 | `second_pull` | Explosive extension toward flight |
| 5 | `turnover` | Bar flight and arm rotation under the bar |
| 6 | `catch` | Overhead receipt and fixation before stand-up |
| 7 | `recovery` | Stand-up until full hip/knee extension with bar stable overhead |

Canonical config: `configs/ontology/seven_phase_v1.yaml`.  
Literature anchors: `docs/literature/CAO_CHEN_ALIGNMENT.md`, `docs/reproduction/AUTHOR_CLARIFICATIONS.md`.

### 2.3 Boundary criteria (visual events)

Place each boundary on the **first frame of the destination phase**.

| Transition | Place boundary when… |
|------------|----------------------|
| `setup` → `first_pull` | Barbell **separates** from the platform |
| `first_pull` → `transition` | First clear **knee-extension reversal** toward flexion (scoop onset) |
| `transition` → `second_pull` | Deepest knee/hip flexion; explosive second pull begins |
| `second_pull` → `turnover` | Explosive extension complete; bar path inflects toward flight (priority coaching boundary) |
| `turnover` → `catch` | Bar is **received** overhead in the catch position |
| `catch` → `recovery` | Fixation complete; **stand-up begins** |

**Recovery ends** only when hips and knees are fully extended and the bar is stable overhead—not at first squat receipt.

If a transition is visually ambiguous, choose the **closest frame that is consistent with the biomechanical cue**, then move on. Do not leave gaps between consecutive supervised phases except via `unlabeled` outside the attempt.

### 2.4 Failed / incomplete lifts

- Label **only phases that visibly occur**.
- If the lift fails before a catch, do **not** invent `catch` or `recovery`.
- Use `unlabeled` for frames after the attempt ends or when the phase is undefined.
- Short transitions (1–3 frames) are allowed when the motion is truly brief.

### 2.5 Practical workflow

1. Open the trimmed clip from the raw-video root (see work package).
2. Scrub frame-by-frame around candidate events (all videos are **25 fps CFR**; 1 frame = 40 ms).
3. Record inclusive segment intervals (Section 3).
4. Self-check: supervised phases should be contiguous in the natural order when present; invalid skips (e.g. `setup` → `turnover`) are errors unless intervening frames are `unlabeled` for a clear reason.

### 2.6 Time budget (guidance)

Expect roughly **10–20 minutes per video** on average (hard fails and short transitions take longer). Total subset ≈ **4–7 hours** plus breaks.

---

## 3. Output format

Deposit finished files under:

```text
analysis/iaa/annotator2/segments/<athlete>/<video_basename>.csv
```

Alternatively, a single combined file:

```text
analysis/iaa/annotator2/segments/master_segment_labels_annotator2.csv
```

### 3.1 CSV schema (match annotator 1)

Columns (exact names):

```text
video,video_relpath,start_frame,end_frame,phase_id,phase_name
```

- `video`: basename (e.g. `snatch_-53kg_cambei_mihaela_valentina_i1_ok_000118.mp4`)
- `video_relpath`: `athlete/basename.mp4` (must match the subset list exactly)
- `start_frame`, `end_frame`: **inclusive** integer frame indices (0-based), same convention as `master_segment_labels.csv`
- `phase_id` / `phase_name`: consistent with the ontology table above

Example rows (illustrative only — **not** a real label):

```text
video,video_relpath,start_frame,end_frame,phase_id,phase_name
snatch_example.mp4,athlete/snatch_example.mp4,0,20,0,unlabeled
snatch_example.mp4,athlete/snatch_example.mp4,21,40,1,setup
```

Blank templates: `python scripts/prepare_iaa_workpack.py` → `analysis/iaa/annotator2_workpack/`.

### 3.2 What not to submit

- Frame-label CSVs only (unless also converted to segments with the same schema)
- Edited copies of annotator-1 files
- Predictions from any model

---

## 4. Agreement metrics (to be computed later)

Primary analysis is **boundary-centric**. After annotator-2 files are complete, run:

```bash
python scripts/run_iaa_pipeline.py
```

(`scripts/compute_iaa_agreement.py` is a thin wrapper of the same entry point.)

The script **refuses** to write manuscript tables/figures if any of the 20 videos is missing.

### 4.1 Recommended metrics

For every ontology transition present in **both** annotations (monotonic one-to-one match per transition type):

| Metric | Definition |
|--------|------------|
| **ICC(2,1)** | Two-way random, single-measure, **absolute agreement** on boundary frame indices (Shrout & Fleiss) |
| **Mean absolute boundary difference** | \(\mathrm{mean}_i \|f_i^{(1)} - f_i^{(2)}\|\) (frames and ms at 25 fps) |
| **Median absolute boundary difference** | Median of the same absolute differences |
| **95th percentile absolute difference** | 95th percentile of absolute differences (tail disagreement) |

Report:

1. **Global agreement** — all paired boundaries pooled  
2. **Per-transition agreement** — each of the six ontology transitions  
3. Counts of transitions present for only one annotator (coverage mismatch on fails)

Outputs (when available):

- `analysis/iaa/results/iaa_agreement.json`
- `analysis/iaa/results/IAA_RESULTS.md`
- `analysis/iaa/tables/iaa_global.tex` / `.md`
- `analysis/iaa/tables/iaa_per_transition.tex` / `.md`

### 4.2 Why Cohen’s kappa is not preferred for temporal boundaries

Cohen’s κ (and related categorical frame-wise coefficients) treat each frame as an independent nominal classification. In snatch phase labelling:

1. **Severe temporal autocorrelation** — long `setup` / `recovery` stretches dominate the confusion matrix and inflate chance-corrected agreement even when **boundaries** disagree by several frames.
2. **The scientific endpoint is boundary timing** — model ranking uses boundary MAE; reliability should target the same construct (event times), not majority-phase accuracy.
3. **Class imbalance** — brief `transition` phases contribute few frames; κ can look “good” while scoop timing is unreliable.
4. **Failed lifts** change which classes exist; frame-κ mixes structural disagreement with timing disagreement.

κ may be reported later as a **secondary** descriptive statistic if desired, but it must not be the headline reliability metric for this benchmark.

### 4.3 Interpretation rules (for the manuscript, after results exist)

- Prefer absolute differences in **frames and milliseconds** plus ICC with explicit \(n\).
- Do **not** claim “excellent reliability” from a single optimistic summary if per-transition P95 is large or ICC is unstable for sparse transitions.
- If confidence intervals or bootstrap intervals on differences later include large errors on `catch→recovery`, state that this boundary remains ambiguous under dual annotation.
- Never invent numbers before annotator-2 completion.

---

## 5. Automated computation pipeline

| Step | Command / artifact | When |
|------|-------------------|------|
| Freeze subset | `analysis/iaa/subset_manifest.json` | Done |
| Build work package | `python scripts/prepare_iaa_workpack.py` | Before annotator 2 starts |
| Annotator 2 labels | `analysis/iaa/annotator2/segments/**` | Pending |
| Compute agreement + tables + figures | `python scripts/run_iaa_pipeline.py` | After all 20 CSVs exist |
| Pipeline documentation | [`IAA_PIPELINE.md`](IAA_PIPELINE.md) | Ready |
| Implementation | `src/snatch_phase_bench/evaluation/iaa.py`, `iaa_pipeline.py` | Ready |
| Unit tests | `tests/test_iaa.py`, `tests/test_iaa_pipeline.py` | Synthetic only (no fabricated study results) |

Annotator-1 path default: `~/papers/Paper_TFM-main/data/annotations/master_segment_labels.csv` (read-only snapshot).

---

## 6. Manuscript placement (planned)

Once results exist, add a short **Annotation reliability** subsection (Dataset or Methods) with:

- subset size and diversity criteria (cite this protocol)
- global mean / median / P95 absolute boundary difference
- ICC(2,1)
- per-transition table (especially `second_pull→turnover` and `catch→recovery`)

Until then, the manuscript should continue to state that labels are single-annotator and that IAA is in progress—not completed.

---

## 7. Checklist

- [x] Representative 20-video subset frozen with rationales  
- [x] Annotator-2 instructions written  
- [x] Output schema defined  
- [x] Metrics + anti-κ rationale documented  
- [x] Computation script ready (no fabricated results)  
- [ ] Annotator 2 recruited / briefed  
- [ ] 20 segment CSVs deposited  
- [ ] `python scripts/run_iaa_pipeline.py` run successfully  
- [ ] Tables/figures inserted into the manuscript  

---

*End of IAA protocol.*
