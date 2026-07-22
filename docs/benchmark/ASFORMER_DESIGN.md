# ASFormer design specification (SnatchPhaseBench)

**Paper:** Fangqiu Yi, Hongyu Wen, Tingting Jiang, *ASFormer: Transformer for Action Segmentation*, BMVC 2021.  
**arXiv:** [2110.08568](https://arxiv.org/abs/2110.08568)  
**Official code:** [ChinaYi/ASFormer](https://github.com/ChinaYi/ASFormer) (commit audited 2026-07-22)  
**Status:** Canonical B3 implementation reference  
**Implementation:** `src/snatch_phase_bench/models/asformer/`

This document summarizes the **publication**, the **official release**, and **SnatchPhaseBench deviations**. It is the scientific basis for `configs/benchmark/asformer.yaml`.

---

## 1. Task

Frame-wise temporal action segmentation: given \(\mathbf{x}_{1:T}\), predict class \(c_t\) per frame.

SnatchPhaseBench uses **MediaPipe 0.10.30 Full** pose vectors (\(D=99\)) instead of I3D features (\(D=2048\)). **Architecture and loss follow the official ASFormer release**; only the input feature extractor differs (deviation D1).

---

## 2. Architecture overview

ASFormer is an **encoder + iterative decoder** Transformer specialized for action segmentation:

```text
x (features)
  → Encoder (J blocks, sliding-window self-attention)
  → initial logits
  → Decoder #1 (cross-attention refinement)
  → Decoder #2
  → Decoder #3
  → final logits
```

Each **encoder/decoder block** (paper Fig. 1):

1. **Feed-forward:** dilated temporal convolution (kernel 3), ReLU.  
2. **Attention:** single-head self-attention (encoder) or cross-attention (decoder), residual with weight \(\alpha\).  
3. **1×1 conv + dropout**, residual around the block, masked.

**Hierarchical local windows:** attention window size and dilation grow as \(2^i\) with block index \(i\) (local → global).

**No positional encoding** in the final model (paper §5.1: PE hurts when temporal conv is used).  
**Single-head attention** by default (paper §5.1).

---

## 3. Paper vs official code (mandatory audit)

| Item | Paper (BMVC 2021) | Official `model.py` / `main.py` | SnatchPhaseBench choice |
|------|-------------------|----------------------------------|-------------------------|
| Blocks \(J\) per stage | **9** (§3.3) | **`num_layers=10`** | **10** (author release; documented D2) |
| Decoders | **3** | **3** | **3** |
| Feature dim | **64** | **64** | **64** |
| Channel drop | **0.3** | **0.3** (0.5 GTEA) | **0.3** |
| Smooth loss \(\lambda\) | **0.25** (§3.3) | **0.15** in `Trainer.train` | **0.15** (author release; D3) |
| TMSE clamp | MSE on probs (Eq.) | clamp squared log-softmax Δ to **16** (`τ²`) | Same as release / MS-TCN |
| Epochs | **120** | **120** | **50 + early stop** (B2 protocol; D4) |
| LR | **0.0005** | **0.0005** (Breakfast 1e-4) | **0.0005** |
| Weight decay | not stated | **1e-5** | **1e-5** (author release; D5) |
| LR scheduler | not stated | `ReduceLROnPlateau` on train loss | **none** (B2 protocol; D6) |
| Cross-attn Q/K/V | Paper: Q,K from concat(encoder, prev); V from prev | Code: Q,K from decoder path; V from `f` (encoder/prev feature) | **Follow code** (D7) |
| Window mask L72 | — | Known bug ([issue #2](https://github.com/ChinaYi/ASFormer/issues/2)) | **Apply author-suggested fix** (D8) |
| Positional encoding | Ablated; omitted | `PositionalEncoding` present but unused | Unused |
| Batch size | implied 1 for sliding att | `assert batch==1` for sliding | **1** |

### D8 — window mask fix (author-recommended)

Official `construct_window_mask` (approx. L70–73):

```python
for i in range(self.bl):
    window_mask[:, :, i:i+self.bl] = 1  # buggy indexing
```

Suggested correction (authors recommend applying after download):

```python
for i in range(self.bl):
    window_mask[:, i, i:i+self.bl] = 1
```

SnatchPhaseBench **applies this fix**. Pretrained ASFormer Zoo weights are not used; all models are trained from scratch on SnatchPhaseBench.

---

## 4. Inputs and outputs

| Item | Paper / release | SnatchPhaseBench |
|------|-----------------|------------------|
| Input | I3D 2048-d | MediaPipe pose **99-d** (D1) |
| Layout | Conv1d `(B, C, T)` | Same internally; public API `(B, T, D)` |
| Labels | Dataset action classes | Canonical **8** ids (0=ignore + 7 phases) |
| Output | Per-stage logits; final stage for inference | Same |
| Masking | Padding mask `(B, 1, T)` | Same |

---

## 5. Loss

Sum over encoder + all decoder stages (same structure as MS-TCN multi-stage loss):

\[
\mathcal{L} = \sum_s \big(\mathcal{L}_{\mathrm{CE}}^{(s)} + \lambda \mathcal{L}_{\mathrm{T\text{-}MSE}}^{(s)}\big)
\]

Author release: \(\lambda=0.15\), clamp of squared log-softmax differences to \(16\).  
Ignore index: release uses `-100`; SnatchPhaseBench uses **0** (unlabeled), consistent with B2.

---

## 6. Inference

1. Forward encoder → decoder stack.  
2. Softmax between stages (masked).  
3. \(\arg\max\) on **final decoder** logits.  
4. Eval mode: no channel dropout / block dropout stochasticity.

---

## 7. Training protocol (aligned with frozen B2)

To keep comparisons fair with MS-TCN (B2), the **benchmark protocol** (not the architecture) matches M3:

| Item | Value |
|------|-------|
| Seeds | 42, 123, 456 |
| Hardware | NVIDIA RTX 4090, FP32, CUDA |
| Split / ontology / evaluator | Identical to B2 |
| Batch size | 1 |
| Max epochs | 50 |
| Early stopping | `val_segmental_f1_at_50`, patience 15 |
| Standardization | train-only (SPB D_std) |
| Class weighting | true (SPB D_cw) |
| Optimizer | Adam, lr 0.0005, weight_decay **1e-5** |

ASFormer-specific: `channel_masking_rate=0.3`, `num_decoders=3`, `num_layers=10`, `r1=r2=2`, `att_type=sliding_att`.

---

## 8. SnatchPhaseBench deviation register

| ID | Deviation | Justification |
|----|-----------|---------------|
| D1 | Input 99-d pose vs 2048-d I3D | Benchmark principle: adapt input only |
| D2 | \(J=10\) (code) not 9 (paper) | Match author training release |
| D3 | \(\lambda=0.15\) (code) not 0.25 (paper) | Match author release; comparable to B2 loss scale |
| D4 | 50 epochs + segment-F1 early stop vs 120 | Fair protocol with frozen B2 |
| D5 | weight_decay=1e-5 | Author release trainer |
| D6 | No ReduceLROnPlateau | Avoid confounding early-stop protocol vs B2 |
| D7 | Cross-attn as in code | Published numbers come from release |
| D8 | Window-mask indexing fix | Authors recommend fix for new training |
| D_std | Train-only standardization | Shared SPB preprocessing with B2 |
| D_cw | Class-weighted CE | Shared SPB imbalance handling with B2 |
| D_dev | Device-agnostic tensors (no global `device`) | Reproducible multi-process CUDA |

---

## 9. Implementation map

| Component | Path |
|-----------|------|
| Core (attention, encoder, decoder) | `models/asformer/core.py` |
| Adapter | `models/asformer/model.py` |
| Loss | reuse `models/ms_tcn/loss.py` |
| Trainer | `training/asformer_trainer.py` |
| Config | `configs/benchmark/asformer.yaml` |
| Scripts | `scripts/train_asformer.py`, `eval_asformer.py`, `run_asformer_benchmark.py` |

---

## 10. References

1. Yi, Wen, Jiang. ASFormer: Transformer for Action Segmentation. BMVC 2021.  
2. Official repository: https://github.com/ChinaYi/ASFormer  
3. Farha & Gall. MS-TCN. CVPR 2019 (loss form shared with author ASFormer release).
