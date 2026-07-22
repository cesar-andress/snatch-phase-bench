# Go / No-Go — publication readiness

**Date:** 2026-07-22  
**Assumption:** submission tomorrow.  
**Ignored:** typos, grammar, formatting.  
**Focus:** whether the scientific artifact is ready to defend as a submitted manuscript.

---

## Decision: **NO-GO**

### 1. Would you submit it today?

**No.**

### 2. If not, why not?

The paper’s central claim is a **reproducible public benchmark** for snatch phase segmentation with **boundary timing** as a primary endpoint. Tomorrow’s PDF still cannot fully cash that claim:

- Primary video is **not publicly releasable**; FPS/camera metadata remain unverified while timing is reported in frames.
- Labels are **single-annotator** with **no IAA**, yet model ranking leans on boundary MAE.
- B2 vs B3 is presented as a frozen comparison **without athlete-level uncertainty** on one fixed split.
- The main comparison table still carries **empty future tiers** and a **duplicate/mislabeled Frame MoF** column beside Macro F1.
- Closing sections **do not convert Results into a defendable takeaway**; Abstract≈Conclusion, while Limitations honestly list gaps that undercut the “benchmark” framing.

Engineering diligence (checksums, locked configs, multi-seed runs) is real. It does not substitute for release, label reliability, and clean evaluative claims.

### 3. Five highest-impact improvements still possible (before / just after submission)

| Rank | Improvement | Why it moves the needle |
|------|-------------|-------------------------|
| 1 | **Data-access + scope rewrite** — state exactly what is downloadable now; stop calling pending video a contribution; narrow “benchmark” if video stays private | Removes the #1 reject reason |
| 2 | **IAA on a boundary subset** (or explicit downgrade of boundary claims) | Makes primary endpoint credible |
| 3 | **Clean comparison table** — evaluated models only; fix/remove MoF; separate or drop incomparable LSTM columns | Stops looking unfinished |
| 4 | **Uncertainty for B2–B3** (athlete bootstrap/LOAO) **or** demote numbers to illustrative protocol demos | Aligns claims with evidence |
| 5 | **Conclusion from findings** (frame≈flat; segment/boundary differ; catch→recovery dominates) + one FPS/timing policy | Gives reviewers a paper, not a status report |

### 4. Issues reviewers are likely to raise

- Non-public / rights-pending video vs reproducibility branding  
- No inter-annotator agreement on phase boundaries  
- Architecture bake-off without significance / multi-split  
- Empty leaderboard rows; MoF vs macro-F1 confusion  
- Ontology not equivalent to Cao/Thiele yet framed as biomechanical phases  
- Unknown FPS for a timing-oriented benchmark  
- Coaching implications overstated relative to offline competition clips  

### 5. Issues that would probably never be mentioned

- Internal doc audits, `\repo{...}` path density, Paper-organization march  
- Abstract/Conclusion lexical cloning and “frozen/canonical” adjective stacking  
- TikZ landscape figure taste; contribution bullet slogan titles  
- Parallel “Across seeds…” prose symmetry between B2 and B3  
- Whether Threats vs Limitations should be merged (unless page-limited)  
- Minor caption length / decimal-precision housekeeping alone  

### 6. Confidence

**Publication-readiness confidence: 28%**  
**Confidence in this No-Go call: 85%**

---

## One-line executive summary

**No-Go for tomorrow:** strong reproducibility engineering, weak public-benchmark and label-reliability claims—fix release scope, IAA/boundary credibility, and the comparison table before submitting.

---

*End of Go/No-Go.*
