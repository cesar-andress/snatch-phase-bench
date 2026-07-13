# B0 — Exploratory reference (frozen)

**Status:** **FROZEN — exploratory reference only**  
**Date frozen:** 2026-07-14  
**Supersedes for B0 scope:** competitive baseline claims in earlier benchmark drafts

---

## Scientific outcome

The biomechanical evidence audit ([`B0_EVIDENCE_MATRIX.md`](B0_EVIDENCE_MATRIX.md)) concluded that a **knee-angle-only rule-based segmenter cannot be implemented** without introducing unsupported operational decisions (joint definitions, smoothing, numeric onset rules, and late-phase boundaries that require bar position).

This is an **accepted scientific result**, not a deferred implementation task.

---

## What B0 is

| Aspect | Definition |
|--------|------------|
| Role | **Exploratory reference** documenting how biomechanics literature names pull-phase events (knee reversals and extrema) |
| Competitive status | **Not a primary benchmark comparator** until operational rules are evidence-backed |
| Code | **Not implemented** and **not planned** under current protocol |
| Ontology artifacts | Retained for documentation only (`five_phase_knee_angle_v1`, `seven_to_five_knee_angle_v1`) |

---

## What B0 is not

- A verified baseline tier (that role belongs to **B1**, the frozen thesis LSTM)
- A mandatory row in the primary benchmark comparison table
- A substitute for learned temporal segmenters (**B2**: MS-TCN family)

---

## Primary benchmark path

Learned **temporal action segmentation** models (MS-TCN, MS-TCN++, ASFormer) on fixed MediaPipe pose inputs are the **primary scientific comparators**, evaluated with canonical segment- and boundary-level metrics against seven-class expert labels.

B1 remains the frozen historical reproduction reference.

---

## Related documents

| Document | Purpose |
|----------|---------|
| [`B0_EVIDENCE_MATRIX.md`](B0_EVIDENCE_MATRIX.md) | Transition-level evidence audit |
| [`B0_IMPLEMENTATION_SPECIFICATION.md`](B0_IMPLEMENTATION_SPECIFICATION.md) | Blocked spec (archived) |
| [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md) §B0 | Protocol language (exploratory) |
| [`MS_TCN_INTEGRATION.md`](MS_TCN_INTEGRATION.md) | B2 infrastructure preparation |

---

## Re-opening B0 (future, optional)

B0 implementation may be reconsidered only if **new evidence** resolves open decisions in [`B0_IMPLEMENTATION_SPECIFICATION.md`](B0_IMPLEMENTATION_SPECIFICATION.md) §8 (OD-2, OD-B0-1/2/3) with documented provenance—not by inventing thresholds ad hoc.

Any future B0 run would receive a new version ID and would **not** retroactively change primary benchmark rankings.
