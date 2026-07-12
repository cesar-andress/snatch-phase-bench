# Documentation

## Scientific knowledge base

- **External (read-only):** [`SnatchPhaseBench_Literature_Foundation.md`](../../SnatchPhaseBench_Literature_Foundation.md) — authoritative literature and reviewer strategy
- [`literature/README.md`](literature/README.md) — how knowledge is distributed in this repo
- [`literature/GAP_ANALYSIS.md`](literature/GAP_ANALYSIS.md) — literature vs repository gaps
- [`SCIENTIFIC_WORKFLOW.md`](SCIENTIFIC_WORKFLOW.md) — sync software, benchmark, docs, manuscript

## Research and benchmark

- [`research_design.md`](research_design.md) — scientific goals and contribution framing
- [`benchmark/BENCHMARK_PLAN.md`](benchmark/BENCHMARK_PLAN.md) — baseline tiers, metrics, milestones
- [`evaluation_metrics.md`](evaluation_metrics.md) — metric definitions
- [`release/PUBLICATION_STRATEGY.md`](release/PUBLICATION_STRATEGY.md) — venue fit and release plan

## Paper preparation

- [`paper/MANUSCRIPT_LOCATION.md`](paper/MANUSCRIPT_LOCATION.md) — LaTeX lives outside Git
- [`paper/PAPER_TODO.md`](paper/PAPER_TODO.md) — manuscript action tracker
- [`paper/REVIEWER_CHECKLIST.md`](paper/REVIEWER_CHECKLIST.md) — reviewer risks and mitigations
- [`figures_plan.md`](figures_plan.md) / [`tables_plan.md`](tables_plan.md) — artifact inventory
- Living manuscript (external): `~/papers/snatch-phase-bench/paper/WRITING_STATUS.md`

## Dataset and architecture

- [`dataset/dataset.md`](dataset/dataset.md) — dataset specification
- [`project_architecture.md`](project_architecture.md) — software layout and flows
- [`FROZEN_BASELINE.md`](FROZEN_BASELINE.md) — baseline freeze policy
- [`benchmark/BASELINE_SPECIFICATION.md`](benchmark/BASELINE_SPECIFICATION.md) — verified thesis LSTM baseline (B1-repro-v1)

## Policies and reproduction

- [`WORKSPACE_POLICY.md`](WORKSPACE_POLICY.md) — read-only `Paper_TFM-main`, canonical workspace rules
- [`REPRODUCTION_PLAN.md`](REPRODUCTION_PLAN.md) — reproduce baseline without touching the snapshot
- [`reproduction/REPRODUCTION_SUMMARY.md`](reproduction/REPRODUCTION_SUMMARY.md) — Phase 2 results (frozen)
- [`reproduction/CHECKPOINT_PROVENANCE.md`](reproduction/CHECKPOINT_PROVENANCE.md) — recovered `best_model.pt` provenance
- [`reproduction/CHECKPOINT_VALIDATION.md`](reproduction/CHECKPOINT_VALIDATION.md) — thesis metric reproduction (VERIFIED)
- [`reproduction/REMAINING_BLOCKERS.md`](reproduction/REMAINING_BLOCKERS.md) — post-validation blockers

## Phase 1 audit (historical)

- [`audit/PROJECT_AUDIT.md`](audit/PROJECT_AUDIT.md)
- [`audit/RESEARCH_ROADMAP.md`](audit/RESEARCH_ROADMAP.md) — **superseded** by [`benchmark/BENCHMARK_PLAN.md`](benchmark/BENCHMARK_PLAN.md) for benchmark planning
- [`audit/QUESTIONS_FOR_STUDENT.md`](audit/QUESTIONS_FOR_STUDENT.md)

## Status

Phase 2 reproduction is **complete**: dataset rebuild exact; thesis checkpoint **VERIFIED** (all metrics EXACT).
Phase 2.5 infrastructure and Phase 2.6 living manuscript are active.
Benchmark experiments (B0–B3) may proceed; see [`reproduction/REMAINING_BLOCKERS.md`](reproduction/REMAINING_BLOCKERS.md).
