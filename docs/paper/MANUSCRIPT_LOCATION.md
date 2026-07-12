# Manuscript location

The **living LaTeX manuscript is not tracked in this Git repository.**

| Item | Path |
|------|------|
| Manuscript root | `~/papers/snatch-phase-bench/paper/` |
| Main file | `~/papers/snatch-phase-bench/paper/main.tex` |
| Writing roadmap | `~/papers/snatch-phase-bench/paper/WRITING_ROADMAP.md` |
| Review prep | `~/papers/snatch-phase-bench/paper/REVIEW_RESPONSE_NOTES.md` |

Relative path from this repository root:

```text
../paper/
```

## LaTeX structure (maturation phase)

```text
../paper/
  main.tex, preamble.tex, macros/
  sections/     Scientific prose
  figures/      One float per file (caption + label + TODO)
  tables/       One float per file (\pending cells)
  appendices/   Notation, dataset, reproducibility, hyperparams, extras
  formatting/   Journal switch (Elsevier / Springer / IEEE)
  generated/    Exported PDF figures
```

## In-repo paper documentation

These files **stay in Git** (process trackers, not LaTeX):

- [`PAPER_TODO.md`](PAPER_TODO.md)
- [`REVIEWER_CHECKLIST.md`](REVIEWER_CHECKLIST.md)

See [`../SCIENTIFIC_WORKFLOW.md`](../SCIENTIFIC_WORKFLOW.md) for synchronization rules.
