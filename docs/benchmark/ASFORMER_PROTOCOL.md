# ASFormer B3 experiment protocol (frozen)

**Milestone:** B3 — first transformer baseline under the same protocol as MS-TCN (B2)  
**Frozen:** 2026-07-22  
**Status:** Pre-declared protocol; do not change seeds or hyperparameters after viewing results.  
**Design:** `docs/benchmark/ASFORMER_DESIGN.md`

---

## Objective

Train and evaluate canonical ASFormer (B3) on all 208 frame-sequence videos with three fixed seeds, using validation **segment F1@IoU=0.50** for checkpoint selection — identical selection rule to frozen MS-TCN (B2).

---

## Comparability lock (vs B2)

| Item | Frozen value |
|------|----------------|
| Dataset / split / ontology / evaluator | Same as B2 |
| Seeds | 42, 123, 456 |
| Hardware | NVIDIA GeForce RTX 4090, CUDA, FP32 |
| Batch size | 1 |
| Max epochs / patience | 50 / 15 |
| Monitor | `val_segmental_f1_at_50` |
| Standardization / class weights | train-only / true |

Only the **model architecture** differs (ASFormer vs MS-TCN).

---

## ASFormer hyperparameters (author release + documented deviations)

See `ASFORMER_DESIGN.md`. Summary: 1 encoder + 3 decoders, 10 layers, 64 maps, channel mask 0.3, λ=0.15, Adam lr=5e-4, weight_decay=1e-5, sliding-window attention with author L72 mask fix.

---

## Runner

```bash
python scripts/run_asformer_benchmark.py --config configs/benchmark/asformer.yaml
```

Outputs under `outputs/benchmark/asformer/` (gitignored); summaries tracked in `docs/benchmark/results/asformer_b3/` after the campaign.
