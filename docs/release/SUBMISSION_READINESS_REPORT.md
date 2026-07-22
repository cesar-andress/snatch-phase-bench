# Submission readiness report — SnatchPhaseBench

**Date:** 2026-07-22  
**Scope:** Software repo `snatch-phase-bench/` + sibling manuscript `~/papers/snatch-phase-bench/paper/`  
**Audit type:** Global scientific / reproducibility / manuscript / release (read-only on frozen B1–B3 artifacts)  
**Frozen baselines (do not retrain):** B1 LSTM · B2 MS-TCN · B3 ASFormer  
**HEAD at audit:** `5e28377` (`origin/main`)

This document is an audit, not a rewrite. No frozen benchmark results were modified.

---

## 1. Executive summary

SnatchPhaseBench has a **mature technical core**: canonical ontology, shared athlete-disjoint split, shared evaluator, frozen B1 checkpoint validation, and three-seed RTX 4090 campaigns for **MS-TCN (B2)** and **ASFormer (B3)** with versioned JSON/CSV/figures under `docs/benchmark/results/`.

It is **not ready for journal submission** as a complete manuscript + public research artifact.

Primary blockers:

1. **Manuscript front/back matter contradicts Results** (Abstract, Intro, Limitations, Conclusion still deny multi-model results; Discussion is outline-only).
2. **Legal / license / citation metadata unfinished** (`LICENSE`, `CITATION.cff`, no Zenodo metadata).
3. **External reproduction incomplete** (data not redistributable; absolute local paths; RTX 4090 hard-gate; README still “Phase 1”).
4. **No statistical testing** for B2 vs B3 deltas reported as numeric improvements.
5. **Stale documentation** across `docs/` still claims Phase 3 / boundary / MS-TCN “not started”.

**Final recommendation:** **Not ready** for journal submission.  
**Confidence in that recommendation:** **92%**.  
**Estimated submission-readiness of the current package:** **38 / 100**.

---

## 2. Scientific strengths

| Strength | Evidence |
|----------|----------|
| Clear primary contribution framing (dataset + protocol, not a new architecture) | `docs/release/PUBLICATION_STRATEGY.md` |
| Athlete-disjoint 49/10/11 split; no athlete leakage | Ontology + split configs; manuscript §3/§5 |
| Canonical seven-phase ontology with Cao–Chen alignment documented | `configs/ontology/seven_phase_v1.yaml`, `docs/literature/CAO_CHEN_ALIGNMENT.md` |
| Shared evaluation stack (frame / segment / boundary) | `src/snatch_phase_bench/evaluation/` |
| B1 exact checkpoint reproduction gate | Results §6 + reproduction docs |
| B2 and B3 implemented faithfully with design audits | `MS_TCN_DESIGN.md`, `ASFORMER_DESIGN.md` |
| Three fixed seeds, shared early-stop monitor (`val_segmental_f1_at_50`), same hardware | Protocol freeze JSONs |
| Canonical results tracked in Git (not only gitignored `outputs/`) | `docs/benchmark/results/{ms_tcn_m3,asformer_b3}/` |
| Strong unit/integration test suite | **161 passed** (2026-07-22) |
| Honest documentation of paper vs code deviations (ASFormer J, λ, mask fix) | `ASFORMER_DESIGN.md` |
| Boundary MAE reported in **frames** with explicit FPS caveat | Protocol + Results |

---

## 3. Scientific weaknesses

| Weakness | Severity |
|----------|----------|
| Single annotator; no IAA | High (gold-standard quality) |
| FPS / resolution metadata unverified → no boundary-ms claims | High for biomechanics venues |
| No LOAO / multi-split uncertainty | High for generalization claims |
| B2 vs B3 compared with mean±std over **3 seeds only** (not athlete bootstrap / paired tests) | High if ranking language stays |
| B0 rule-based baseline never implemented (empty leaderboard row) | Medium–High vs story sentence in publication strategy |
| Window-level LSTM not comparable to dense TAS endpoints | Medium (already warned; still confuses readers) |
| Ablations empty; encoder contrasts (CTR-GCN / PoseC3D) not run | Medium |
| Leaderboard still lists unevaluated models (MS-TCN++, DiffAct, CTR-GCN) as empty rows | Medium (looks unfinished) |
| Qualitative figures largely placeholders in LaTeX | Medium |
| Dataset not publicly releasable yet | High for “benchmark” claim |

---

## 4. Reproducibility assessment

### What an external researcher can do today

| Step | Status |
|------|--------|
| Clone GitHub software repo | Yes |
| `pip install -e ".[dev]"` + run unit tests | Yes (needs deps; no lockfile) |
| Re-read frozen B2/B3 JSON/CSV/figures | Yes (`docs/benchmark/results/`) |
| Re-run B2/B3 end-to-end without private data | **No** |

### Manual steps still required (must stay explicit)

1. Obtain thesis snapshot / keypoints / labels (`Paper_TFM-main` or equivalent transfer).
2. Set `configs/reproduction.yaml` `snapshot_root` (currently absolute `/home/cesar/...`).
3. Install CUDA stack matching campaign (`torch==2.10.0+cu128`, Python 3.12 observed).
4. Pass hardware preflight (**NVIDIA GeForce RTX 4090** name-checked by runners).
5. Run:
   - `python scripts/run_ms_tcn_benchmark.py --config configs/benchmark/ms_tcn.yaml`
   - `python scripts/run_asformer_benchmark.py --config configs/benchmark/asformer.yaml`
6. Optionally promote aggregates from gitignored `outputs/benchmark/...` into `docs/benchmark/results/` (process not in root README).

### Reproducibility grade

| Axis | Grade | Notes |
|------|-------|-------|
| Internal (authors) | **A−** | Protocols + freezes + tests |
| External (public) | **D+** | Data/license/paths/README |
| Metric archival | **A** | JSON/CSV match paper (see § Result consistency) |
| Environment pin | **C** | `pyproject` good; `requirements.txt` / `environment.yml` stale; no lockfile |

Protocol freeze commits:

- B2 freeze recorded at `6b1d7f0…` in `ms_tcn_m3/protocol_freeze.json`
- B3 freeze recorded at `14483a5…` in `asformer_b3/protocol_freeze.json`

---

## 5. Software quality assessment

| Area | Assessment |
|------|------------|
| Package structure | Good (`models/`, `training/`, `evaluation/`, `benchmark/`) |
| B2/B3 scripts | Present and wired; B3 lacks a standalone usage doc equivalent to `MS_TCN_USAGE.md` |
| Tests | Strong for metrics/models; weak for full GPU campaign / dataset checksum CI |
| Dead / stub code | `experiments/runner.py` (`NotImplementedError`); `tas_trainer.py` stub; `spb-run-experiment` entry |
| Naming debt | `evaluator.py` (window legacy) vs `evaluate.py` (canonical TAS) |
| Config debt | `ms_tcn_pp` listed in `configs/benchmark.yaml` but YAML file missing |
| Docs debt | Multiple Phase-1 / “not started” documents still live (see cleanup) |
| README | **Blocking**: still “Phase 1… No experimental results are claimed” |
| CI | Not present in repo audit |

---

## 6. Benchmark quality assessment

| Criterion | B1 | B2 | B3 |
|-----------|----|----|----|
| Frozen | Yes | Yes | Yes |
| Design audit | Thesis repro docs | `MS_TCN_DESIGN.md` | `ASFORMER_DESIGN.md` |
| Three seeds | N/A (frozen ckpt) | Yes | Yes |
| Canonical JSON in Git | Partial (repro docs) | Yes | Yes |
| Fair shared protocol vs peers | Window-only | Yes | Yes |
| Hyperparameter retune after test peek | No | No | No |

**Comparability lock (B2↔B3):** dataset, split, ontology, evaluator, seeds, hardware, early-stop policy — **satisfied**.

**Story gap:** publication strategy story sentence still promises improvement over a **biomechanical heuristic (B0)** that was never run.

---

## 7. Manuscript quality assessment (Reviewer #2)

### Section-by-section (compressed)

| Section | Strengths | Weaknesses / reviewer attack |
|---------|-----------|------------------------------|
| **Title** | Domain-clear | Ensure “benchmark” vs “method” framing matches venue |
| **Abstract** | Honest reproducibility tone | **Contradicts §6**: says multi-model results not reported |
| **Introduction** | Motivation + leakage hygiene | Contributions still say segment/multi-model not reported |
| **Related Work** | Strong TAS / sports seam | Deadlift TODO; prior-art table under-sells B2/B3; strong novelty claim vs incomplete public data |
| **Dataset** | Verified counts; single-annotator honesty | FPS/metadata pending; placeholder figures; no IAA |
| **Methods** | B2/B3 concrete; B0 frozen exploratory | Opening still calls subsections placeholders; ASFormer “after campaign” stale |
| **Protocol** | Nested metrics well defined | Stats testing TODOs; opening “not populated” stale |
| **Results** | Densest verified section; numbers consistent with artifacts | Empty ablation / leaderboard rows; no significance; few figures |
| **Discussion** | Outline structure | **Outline-only**; Results defer interpretation here |
| **Limitations** | Many real limits listed | Bullet still claims benchmark “not yet evaluated” — **false** |
| **Conclusion** | Honest draft bullets | Still “pending multi-model benchmark” |
| **References** | Lean verified set | Gaps (Baumann mentioned, MediaPipe journal form, FineGym metadata risk) |
| **Appendices** | Hyperparams useful | Extra/error appendices largely pending |

### Result consistency (paper ↔ artifacts)

Checked 2026-07-22 against `docs/benchmark/results/{ms_tcn_m3,asformer_b3}/` and `outputs/.../eval_test.json`.

| Claim | Paper | JSON mean | Match |
|-------|-------|-----------|-------|
| B2 frame macro-F1 | 0.905 | 0.904811 | Yes (3 dp) |
| B2 F1@50 | 0.775 | 0.774725 | Yes |
| B2 edit | 0.850 | 0.850486 | Yes |
| B2 MAE | 1.32 | 1.322054 | Yes (2 dp) |
| B2 boundary F1 | 0.947±0.009 | 0.947380±0.008595 | Yes |
| B3 frame macro-F1 | 0.902 | 0.901935 | Yes |
| B3 F1@50 | 0.790 | 0.789655 | Yes |
| B3 edit | 0.855 | 0.854546 | Yes |
| B3 MAE | 0.98 | 0.977273 | Yes (2 dp) |
| B3 boundary F1 | 0.953±0.007 | 0.952908±0.007308 | Yes |
| B2/B3 F1@10, F1@25 | 0.902/0.872 ; 0.907/0.861 | matches outputs means | Yes |
| Per-seed seed-stability tables | — | exact 3 dp match | Yes |
| Δ F1@50 / Δ MAE in Results prose | +0.015 / −0.345 | +0.01493 / −0.34478 | Yes (reported precision) |

**No metric inconsistency requiring manuscript number edits was found.**  
Remaining risk: numbers were transcribed into LaTeX by hand; prefer a generator script before camera-ready.

### Unsupported / exaggerated / stats-sensitive claims

| Claim type | Example location | Flag |
|------------|------------------|------|
| Ranking B3 over B2 without tests | Results Δ language | **Needs stats or softening** |
| “First … benchmark” novelty | Related Work / strategy | **Needs public release + careful scoping** |
| Comparative conclusions denied in Limitations but asserted in Results | `08_limitations.tex` vs `06_results.tex` | **Internal contradiction** |
| Boundary coaching significance | catch→recovery MAE | Speculative if Discussion invents meaning — currently empty |
| Story vs missing B0 | `PUBLICATION_STRATEGY.md` story sentence | **Unsupported until B0 exists or story rewritten** |

---

## 8. Remaining risks before submission

1. Desk reject / return without review for incomplete Discussion + contradictory Abstract.
2. Legal challenge if any identifying athlete material ships without clearance.
3. Reviewer demand for IAA, FPS, and LOAO.
4. Reviewer demand for significance tests on primary endpoints.
5. Reproducibility reviewer cannot retrain B2/B3 from public materials alone.
6. Stale docs undermine trust (“Phase 1”, “MS-TCN not implemented”).
7. Empty B0 row conflicts with “beat the biomechanical heuristic” narrative.
8. Venue mismatch if pitched as methods novelty (Pattern Recognition) rather than Sensors/BSPC-style benchmark.

---

## 9. Mandatory fixes (P0)

Do these before any journal submission candidate:

1. **Rewrite Abstract, Intro contributions, Methods/Protocol openings, Limitations last bullet, Conclusion** so they match frozen B2/B3 Results (no contradictory “not reported” language).
2. **Write a real Discussion** interpreting B2 vs B3, boundaries, runtime, and limits — or cut ranking claims that depend on it.
3. **Add statistical protocol or soften all superiority language** (seed std ≠ athlete generalization).
4. **Resolve LICENSE + CITATION.cff** (authors, URL, license, contact) even if dataset remains restricted.
5. **Rewrite root README** to current status (B1–B3 frozen, how to eval artifacts, how to retrain if data available).
6. **Document external reproduction gaps explicitly** in one short `docs/release/REPRODUCE_B2_B3.md` (data path, hardware gate, commands).
7. **Update or quarantine obsolete docs** that deny B2/B3 existence (`docs/README.md`, `REMAINING_BLOCKERS.md`, `BENCHMARK_PROTOCOL.md` header, `GAP_ANALYSIS.md` boundary TODOs, `MS_TCN_USAGE.md` “future milestone”).
8. **Refresh `PUBLICATION_STRATEGY.md` gates** (G3 done; G2 B0 still open).
9. **Remove or clearly mark empty ablation / appendix pending tables** so camera-ready does not render TODO boxes as science.
10. **Decide B0**: implement minimal heuristic **or** rewrite story sentence to drop heuristic superiority.

---

## 10. Recommended improvements (P1)

1. Athlete-level bootstrap / paired tests for F1@50 and boundary MAE.
2. Generate paper tables/figures from JSON automatically (kill manual transcription risk).
3. Standalone `ASFORMER_USAGE.md` mirroring MS-TCN.
4. Lockfile (`uv.lock` or `pip-tools`) for torch+cu128 environment.
5. Soften RTX 4090 hard-fail to “reference hardware” with documented alternate.
6. Replace absolute `snapshot_root` with env var / relative path.
7. Populate key figures from `docs/benchmark/results/*/figures/` into manuscript includes.
8. Fix FineGym / ASFormer BibTeX metadata; cite Baumann if named; MediaPipe citation form.
9. Update `tab_prior_art_comparison` SnatchPhaseBench row to B2/B3.
10. Minimal CI: pytest on PR + schema validate aggregate JSON.

---

## 11. Nice-to-have improvements (P2)

1. MS-TCN++ / DiffAct only if venue demands fuller leaderboard (not required for first submission if scoped).
2. CTR-GCN / PoseC3D encoder ablations.
3. LOAO / k-fold athlete CV.
4. IAA on a boundary subset.
5. Zenodo DOI + `.zenodo.json` / Codemeta.
6. CONTRIBUTING / CODE_OF_CONDUCT / SECURITY.
7. Remove stub entry points or mark experimental.
8. Archive CPU pilot outputs clearly.
9. Public non-identifying keypoint release if legally cleared.
10. Version bump beyond `0.1.0` for first tagged release.

---

## 12. Repository cleanup recommendations

**Do not delete automatically.** Proposed actions:

| Item | Recommendation |
|------|----------------|
| `outputs/benchmark/**` (local) | **Keep local / gitignored**; canonical copies already in `docs/benchmark/results/` |
| `outputs/benchmark/ms_tcn_cpu_pilot_*` | **Archive** under `docs/benchmark/results/_archive/` or leave gitignored with note |
| Checkpoints `*.pt` | **Keep local**; document checksums; do not commit binaries |
| `README.md` Phase-1 text | **Rewrite** (keep) |
| `docs/audit/*` legacy | **Keep** as historical; add banner “superseded” |
| `docs/reproduction/REMAINING_BLOCKERS.md` | **Update or move to archive** |
| `docs/benchmark/BENCHMARK_PROTOCOL.md` “not started” header | **Update status banner** |
| `requirements.txt` / `environment.yml` | **Align or mark deprecated** vs `pyproject.toml` |
| `src/.../experiments/runner.py`, `tas_trainer.py` | **Keep but label stub** or remove in cleanup PR |
| `configs/benchmark.yaml` → `ms_tcn_pp` | **Keep as planned** or remove dangling path |
| Thesis review docs under `docs/thesis/` | **Keep internal**; exclude from Zenodo highlight set |
| Manuscript `paper/` | **Outside software Git** (policy); sync tracker only |

---

## 13. Release preparation checklist

| Artifact | Status | Action |
|----------|--------|--------|
| README | Obsolete | Mandatory rewrite |
| LICENSE | Placeholder | Legal + choose SPDX |
| CITATION.cff | TODO authors/URL/license | Fill before Zenodo |
| Zenodo metadata | Missing | Add `.zenodo.json` draft |
| Keywords | Present in CITATION/abstract | OK |
| Release notes | Missing | Draft for tag `v0.2.0-benchmark-b2b3` |
| Acknowledgements | Not audited in software | Add in paper + README |
| Software citation | Incomplete | Fix CITATION.cff |
| Dataset citation | Blocked legally | Document restriction |
| Benchmark citation | Same as software until paper DOI | Plan dual citation |
| Repository description (GitHub) | Not verified here | Align with abstract one-liner |

Suggested Zenodo bundle (when legal allows): code tag + `docs/benchmark/results/` + ontology/split configs + reproduction instructions + **no raw athlete videos** until cleared.

---

## 14. Final recommendation

### Ready for journal submission?

**No.**

### Confidence scores

| Question | Score |
|----------|------:|
| Confidence that submission **now** would fail editorial/reviewer screening | **92%** |
| Confidence in **technical correctness of frozen B2/B3 numbers** | **95%** |
| Overall package readiness (software + paper + release) | **38 / 100** |
| Readiness of **benchmark engineering core alone** | **78 / 100** |
| Readiness of **manuscript narrative alone** | **32 / 100** |

### What “ready” would look like (minimum bar)

- Abstract ↔ Results ↔ Limitations ↔ Conclusion consistent.
- Discussion written (factual, no speculation beyond evidence).
- LICENSE + CITATION filled; README current; one reproduction doc for B2/B3.
- Statistical language honest (or tests added).
- Placeholder/TODO density removed from camera-ready path.
- Story aligned with actually completed baselines (B0 decision made).

Until then, SnatchPhaseBench is a **strong internal research artifact** and a **weak journal submission candidate**.

---

## Appendix A — Issue inventory (audit findings)

### A.1 Paper / software mismatches

- Abstract/Intro/Limitations/Conclusion deny multi-model results; §6 reports B2/B3.
- Methods/Protocol openings still “placeholder / not populated”.
- `PUBLICATION_STRATEGY.md` G3 unchecked despite B2/B3 complete.
- Root README Phase 1 vs frozen results in `docs/benchmark/results/`.

### A.2 Obsolete documentation (candidates)

- `README.md`
- `docs/README.md`
- `docs/benchmark/BENCHMARK_PROTOCOL.md` (status header)
- `docs/benchmark/BENCHMARK_PLAN.md` (status)
- `docs/reproduction/REMAINING_BLOCKERS.md`
- `docs/literature/GAP_ANALYSIS.md` (boundary “not implemented”)
- `docs/benchmark/MS_TCN_USAGE.md` (“full runs separate milestone”)
- `docs/release/PUBLICATION_STRATEGY.md` gates
- `requirements.txt` / `environment.yml` vs `pyproject.toml`

### A.3 Incorrect / risky naming

- Eight-class logits (+ unlabeled) vs “seven-phase” prose — explain once in Methods.
- Tier labels B1/B2/B3 inconsistently used in Abstract/Intro.
- Legacy docs that called early MS-TCN “B1”.

### A.4 Hyperparameter / dataset consistency

- B2/B3 configs and design docs aligned with frozen runs (no retune detected).
- Dataset N=208 / 70 athletes / split 49–10–11 consistent across protocol freezes and Results.
- Windowed B1 tensors vs dense frame B2/B3 inputs correctly distinguished.

### A.5 Git history note

Recent history is coherent English milestone commits suitable for Zenodo provenance (`14483a5` architecture → `6cd3c7a` results → `5e28377` manuscript tracker). Continue that discipline; never force-push `main`.

---

*End of audit report.*
