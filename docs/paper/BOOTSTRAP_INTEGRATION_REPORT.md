# Bootstrap and video-metadata integration report

**Date:** 2026-07-22  
**Manuscript root:** `~/papers/snatch-phase-bench/paper/`  
**Evidence sources (read-only; not recomputed):**
- `docs/dataset/VIDEO_METADATA_AUDIT.md`
- `docs/paper/BOOTSTRAP_ANALYSIS.md`
- `analysis/bootstrap/bootstrap_summaries.json`

**Policy:** No new analyses; no fabricated numbers; IAA results not inserted (labels still pending).

---

## 1. Sections modified

| Section | File | Change type |
|---------|------|-------------|
| Abstract | `main.tex` | FPS audit + bootstrap summary; IAA left open |
| Introduction (contributions) | `sections/01_introduction.tex` | ms reading; bootstrap mention |
| Dataset (videos) | `sections/03_dataset.tex` | Audited 25 fps CFR; 40 ms/frame; resolution counts |
| Dataset table | `tables/tab_dataset_stats.tex` | Replace `\pending` FPS/resolution with audited values |
| Experimental protocol (boundary) | `sections/05_experimental_protocol.tex` | Allow ms conversion from audit |
| Experimental protocol (stats) | `sections/05_experimental_protocol.tex` | Document athlete-paired bootstrap procedure |
| Results (ASFormer deltas) | `sections/06_results.tex` | Label seed deltas as descriptive |
| Results (boundary) | `sections/06_results.tex` | Frames + ms equivalence |
| Results (new) | `sections/06_results.tex` + `tables/tab_bootstrap_b3_minus_b2.tex` | Bootstrap CIs |
| Discussion (interpretation) | `sections/07_discussion.tex` | Frame / segment / boundary reading of bootstrap |
| Discussion (threats + future) | `sections/07_discussion.tex` | Remove unknown-FPS threat; keep IAA/LOAO |
| Limitations | `sections/08_limitations.tex` | FPS audited; bootstrap scoped; IAA pending |
| Conclusion | `sections/09_conclusion.tex` | Evidence-proportional wording (no “significantly”) |
| Appendix A | `appendices/A_dataset.tex` | Timing metadata subsection |

---

## 2. Statements changed (substance)

### Removed / replaced
- “Native frame rate … not yet verified”
- “milliseconds … must not be reported … until metadata are confirmed”
- “athlete-level significance tests are not reported” (replaced by bootstrap CI reporting)
- “verified FPS” as future work
- Limitations claim that FPS is incomplete (resolution/demographics remain incomplete)

### Added (numbers only from repo artifacts)
- 208 clips; H.264; CFR; 25 fps; 1 frame = 40 ms; 190×1080p + 18×720p; no corrupt/dup/VFR
- Bootstrap: $n{=}11$, 10{,}000 paired resamples, seed 42
- B3−B2 95% CIs: frame F1 and segment F1@10/25/50 **include 0**; boundary MAE **excludes 0** (mean Δ −0.344 frames ≈ −13.8 ms)

### Language discipline
- Distinguishes **descriptive seed means** vs **athlete-bootstrap uncertainty**
- Avoids “significantly outperforms”
- Scopes boundary advantage to the present test cohort
- Keeps the **benchmark protocol** as the primary contribution

---

## 3. New citations / cross-refs inserted

| Target | Role |
|--------|------|
| `\Cref{sec:dataset:videos}` | FPS audit facts |
| `\Cref{sec:protocol:stats}` | Bootstrap method |
| `\Cref{sec:results:bootstrap}` | Bootstrap results |
| `\Cref{tab:bootstrap_b3_minus_b2}` | CI table |
| Repo paths in prose | `VIDEO_METADATA_AUDIT.md`, `BOOTSTRAP_ANALYSIS.md` |

No new bibliographic entries were required (audit/bootstrap are in-repo artifacts).

---

## 4. Remaining limitations (unchanged honesty)

- Single annotator; IAA labels not yet available (protocol/pipeline ready)
- No leave-one-athlete-out / multi-split analysis
- Bootstrap does not retrain; $n{=}11$ test athletes only
- MediaPipe pose error unquantified on this footage
- Camera angles / demographics incomplete
- Raw-video legal release pending
- B0 / MS-TCN++ / DiffAct / encoder heads not evaluated

The manuscript is **ready to absorb IAA tables** once `python scripts/run_iaa_pipeline.py` succeeds (insert under Dataset/Methods reliability without rewriting the bootstrap narrative).

---

## 5. Final scientific consistency check

| Check | Status |
|-------|--------|
| FPS unknown language removed from Dataset, Protocol, Results, Threats, Limitations, Appendix | Pass |
| Bootstrap numbers match `bootstrap_summaries.json` (rounded) | Pass |
| Seed-level campaign tables still labeled descriptive | Pass |
| No “significant” ranking language for ASFormer | Pass |
| Frame/segment CI-includes-zero stated explicitly | Pass |
| Boundary CI-excludes-zero scoped to test cohort | Pass |
| IAA not fabricated | Pass |
| Primary contribution = benchmark, not architecture win | Pass |

---

*End of integration report.*
