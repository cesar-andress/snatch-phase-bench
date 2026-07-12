# Literature integration index

SnatchPhaseBench scientific knowledge is **distributed across this repository** so that software, benchmark, and manuscript evolve together.

The external knowledge base remains the authoritative reference for literature citations and reviewer strategy:

**External (read-only, do not edit):** [`SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md)

> Path from repository root: [`../SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md)

## How knowledge is distributed

| Topic | Primary repository document |
|-------|----------------------------|
| Gap analysis vs. current repo | [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) |
| Scientific goals and contribution framing | [`../research_design.md`](../research_design.md) |
| Benchmark philosophy and model tiers | [`../benchmark/BENCHMARK_PLAN.md`](../benchmark/BENCHMARK_PLAN.md) |
| Metric definitions (TAS + boundary) | [`../evaluation_metrics.md`](../evaluation_metrics.md) |
| Dataset and phase ontology | [`../dataset/dataset.md`](../dataset/dataset.md) |
| Reviewer risks and mitigations | [`../paper/REVIEWER_CHECKLIST.md`](../paper/REVIEWER_CHECKLIST.md) |
| Manuscript action items | [`../paper/PAPER_TODO.md`](../paper/PAPER_TODO.md) |
| Software ↔ science synchronization | [`../SCIENTIFIC_WORKFLOW.md`](../SCIENTIFIC_WORKFLOW.md) |
| Publication venue strategy | [`../release/PUBLICATION_STRATEGY.md`](../release/PUBLICATION_STRATEGY.md) |
| Reproduction status (frozen baseline) | [`../reproduction/REPRODUCTION_SUMMARY.md`](../reproduction/REPRODUCTION_SUMMARY.md) |
| Living manuscript (LaTeX, external) | `~/papers/snatch-phase-bench/paper/` — see [`../paper/MANUSCRIPT_LOCATION.md`](../paper/MANUSCRIPT_LOCATION.md) |

## Citation policy (from literature foundation)

1. **Never paste citations from memory.** Open each source and confirm bibliographic metadata before adding to `~/papers/snatch-phase-bench/paper/bibliography.bib`.
2. **Verification tiers** in the external document: `[V]` verified, `[K]` high-confidence canonical, `[?]` must confirm — treat all as unverified until you personally check.
3. **No methodological novelty claims** unless supported by new experiments. The defensible contribution is dataset + benchmark + domain formalization.

## Major scientific topics (summary)

The external foundation organizes research into seven nested areas:

1. Human pose estimation (input layer — upstream, not our contribution)
2. Markerless motion analysis (metrological validity; rule-based knee-angle threat)
3. Skeleton-based action recognition (encoders, not end-to-end segmenters)
4. Temporal action segmentation (core task family)
5. Sports analytics / sports biomechanics (evaluation stakes, reviewer expectations)
6. Olympic weightlifting analysis (phase ontology, prior art gap)
7. Reproducibility and benchmark culture (OpenCap, PoseBench3D lessons)

SnatchPhaseBench position (honest framing):

> Fine-grained, single-actor, short-horizon temporal action segmentation on skeleton input, in a sports-biomechanics domain where phase boundaries have kinematic meaning.

See [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) for alignment with the current codebase.
