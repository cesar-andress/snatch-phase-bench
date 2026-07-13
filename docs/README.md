# Documentation

## Scientific knowledge base

- **External (read-only):** [`SnatchPhaseBench_Literature_Foundation.md`](../../SnatchPhaseBench_Literature_Foundation.md) — authoritative literature and reviewer strategy
- [`literature/README.md`](literature/README.md) — how knowledge is distributed in this repo
- [`literature/GAP_ANALYSIS.md`](literature/GAP_ANALYSIS.md) — literature vs repository gaps
- [`SCIENTIFIC_WORKFLOW.md`](SCIENTIFIC_WORKFLOW.md) — sync software, benchmark, docs, manuscript

## Research and benchmark

- [`research_design.md`](research_design.md) — scientific goals and contribution framing
- [`benchmark/B0_EXPLORATORY_REFERENCE.md`](benchmark/B0_EXPLORATORY_REFERENCE.md) — B0 frozen as exploratory reference
- [`benchmark/B0_EVIDENCE_MATRIX.md`](benchmark/B0_EVIDENCE_MATRIX.md) — B0 biomechanical evidence audit
- [`benchmark/B0_IMPLEMENTATION_SPECIFICATION.md`](benchmark/B0_IMPLEMENTATION_SPECIFICATION.md) — archived blocked spec
- [`benchmark/MS_TCN_DESIGN.md`](benchmark/MS_TCN_DESIGN.md) — MS-TCN paper audit and deviations
- [`benchmark/MS_TCN_USAGE.md`](benchmark/MS_TCN_USAGE.md) — training and evaluation guide
- [`benchmark/BENCHMARK_PROTOCOL.md`](benchmark/BENCHMARK_PROTOCOL.md) — **canonical** Phase 3 benchmark specification
- [`benchmark/EXPERIMENT_MATRIX.md`](benchmark/EXPERIMENT_MATRIX.md) — planned experiments
- [`benchmark/STATISTICAL_PROTOCOL.md`](benchmark/STATISTICAL_PROTOCOL.md) — inferential analysis rules
- [`benchmark/BENCHMARK_GOVERNANCE.md`](benchmark/BENCHMARK_GOVERNANCE.md) — versioning policy
- [`benchmark/BENCHMARK_PLAN.md`](benchmark/BENCHMARK_PLAN.md) — implementation checklist (legacy summary)
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
- [`reproduction/AUTHOR_CLARIFICATIONS.md`](reproduction/AUTHOR_CLARIFICATIONS.md) — phase taxonomy, annotation, provenance (author-confirmed)
- [`reproduction/REPRODUCTION_SUMMARY.md`](reproduction/REPRODUCTION_SUMMARY.md) — Phase 2 results (frozen)
- [`reproduction/CHECKPOINT_PROVENANCE.md`](reproduction/CHECKPOINT_PROVENANCE.md) — recovered `best_model.pt` provenance
- [`reproduction/CHECKPOINT_VALIDATION.md`](reproduction/CHECKPOINT_VALIDATION.md) — thesis metric reproduction (VERIFIED)
- [`reproduction/REMAINING_BLOCKERS.md`](reproduction/REMAINING_BLOCKERS.md) — post-validation blockers

## Phase 1 audit (historical)

- [`audit/PROJECT_AUDIT.md`](audit/PROJECT_AUDIT.md)
- [`audit/RESEARCH_ROADMAP.md`](audit/RESEARCH_ROADMAP.md) — **superseded** by [`benchmark/BENCHMARK_PLAN.md`](benchmark/BENCHMARK_PLAN.md) for benchmark planning
- [`audit/QUESTIONS_FOR_STUDENT.md`](audit/QUESTIONS_FOR_STUDENT.md)

## Status

Phase 2 reproduction is **complete** (checkpoint VERIFIED).
Phase 3 benchmark **design** is **complete**; implementation **not** started.
See [`benchmark/BENCHMARK_PROTOCOL.md`](benchmark/BENCHMARK_PROTOCOL.md).
