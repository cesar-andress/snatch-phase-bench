# MS-TCN design specification (SnatchPhaseBench)

**Paper:** Yazan Abu Farha and Jürgen Gall, *MS-TCN: Multi-Stage Temporal Convolutional Network for Action Segmentation*, CVPR 2019.  
**DOI:** [10.1109/CVPR.2019.00369](https://doi.org/10.1109/CVPR.2019.00369)  
**Status:** Canonical B2 implementation reference (M2)  
**Implementation:** `src/snatch_phase_bench/models/ms_tcn/`

This document summarizes the **original publication** and records **SnatchPhaseBench deviations**. It is the scientific basis for `configs/benchmark/ms_tcn.yaml`.

---

## 1. Task

Given frame-wise features \(\mathbf{x}_{1:T}\), predict a class label \(c_t\) for each frame (temporal action segmentation at full temporal resolution).

SnatchPhaseBench uses **MediaPipe 0.10.30 Full** pose vectors (\(D=99\)) instead of I3D features. The **architecture and loss** follow the paper; only the input feature extractor differs (documented deviation §8).

---

## 2. Architecture overview

MS-TCN stacks **\(S\) identical single-stage TCNs** (SS-TCN). Stage 1 maps input features to class logits; each later stage **refines** the softmax probabilities from the previous stage.

```text
x (features) ──► Stage 1 ──► logits ──► softmax ──► Stage 2 ──► … ──► Stage S
```

Each stage contains:

1. **1×1 convolution** — project input channels to \(D\) feature maps (`num_f_maps`).
2. **\(L\) dilated residual layers** — kernel size 3, dilation \(1, 2, 4, \ldots, 2^{L-1}\).
3. **1×1 convolution** — project to \(C\) class logits.

**Residual dilated layer** (paper Eq. 1–2):

\[
\hat{H}_l = \mathrm{ReLU}(W_1 * H_{l-1} + b_1), \quad
H_l = H_{l-1} + W_2 * \hat{H}_l + b_2
\]

where \(*\) is dilated 1D convolution (kernel size 3, **acausal** / symmetric padding in the paper).

**Receptive field** (kernel 3, doubling dilation): \(\mathrm{RF}(l) = 2^{l+1} - 1\) (paper Eq. 3).  
With \(L=10\) layers per stage: RF per stage \(\approx 2047\) frames.

---

## 3. Inputs and outputs

| Item | Paper | SnatchPhaseBench |
|------|-------|------------------|
| Input features | I3D (2048-d) at 15 fps | MediaPipe pose (99-d) at native video fps |
| Tensor layout | Conv1D: \((B, D_{in}, T)\) | Same internally; public API \((B, T, D)\) |
| Stage-1 input | \(\mathbf{x}_{1:T}\) | Standardized pose features |
| Stage-\(s>1\) input | Softmax probabilities only (no feature concat) | Same (paper §4.5, Table 5) |
| Output | Per-frame class probabilities / logits | Logits from **final stage** for inference; all stages for training loss |
| Masking | Not in paper | Padding mask for batched sequences (author release pattern) |

---

## 4. Loss function (mandatory)

Per stage \(s\), the paper minimizes (Eq. 12–13):

\[
\mathcal{L}_s = \mathcal{L}_{cls} + \lambda \mathcal{L}_{T-MSE}
\]

**Classification (Eq. 7):** cross-entropy over frames (implemented on **logits**, standard PyTorch `CrossEntropyLoss` — matches author release).

**Truncated smoothing loss (Eq. 8–10):** penalizes frame-to-frame changes in log-probabilities:

\[
\Delta_{t,c} = |\log y_{t,c} - \log y_{t-1,c}|, \quad
\tilde{\Delta}_{t,c} = \min(\Delta_{t,c}, \tau)
\]

\[
\mathcal{L}_{T-MSE} = \frac{1}{TC}\sum_{t,c} \tilde{\Delta}_{t,c}^2
\]

Gradients flow only through \(y_{t,c}\); \(y_{t-1,c}\) is detached (paper §3.3).

**Total loss:** \(\mathcal{L} = \sum_s \mathcal{L}_s\) (Eq. 13).

| Hyperparameter | Paper §3.4 / §4.4 | SnatchPhaseBench config |
|--------------|-------------------|-------------------------|
| \(\lambda\) | **0.15** | `loss.tmse_weight: 0.15` |
| \(\tau\) | **4** | `loss.tmse_truncate_tau: 4` |

**Implementation note:** the author release clamps squared log-softmax differences to \(\tau^2 = 16\), equivalent to truncating at \(\tau=4\). SnatchPhaseBench follows that release convention for the smoothing term.

---

## 5. Inference

- Run all \(S\) stages sequentially.
- Apply softmax to stage output before feeding the next stage.
- **Final prediction:** \(\arg\max_c\) over final-stage logits (per frame).
- Deterministic given fixed weights and input (no dropout at eval).

---

## 6. Hyperparameters

### 6.1 Reported in CVPR 2019 §3.4 (mandatory defaults)

| Parameter | Value | Config key |
|-----------|-------|------------|
| Stages \(S\) | **4** | `model.num_stages` |
| Layers per stage \(L\) | **10** | `model.num_layers` |
| Feature maps \(D\) | **64** | `model.num_f_maps` |
| Kernel size | **3** | `model.kernel_size` |
| Dilation schedule | \(1,2,4,\ldots,2^{L-1}\) | derived from `num_layers` |
| Optimizer | **Adam** | `optimizer.name: adam` |
| Learning rate | **0.0005** | `optimizer.learning_rate` |
| \(\lambda\) (smoothing) | **0.15** | `loss.tmse_weight` |
| \(\tau\) (truncation) | **4** | `loss.tmse_truncate_tau` |

### 6.2 Mentioned but underspecified in the paper

| Parameter | Paper status | SnatchPhaseBench decision |
|-----------|--------------|---------------------------|
| **Dropout rate** | “dropout is used after each layer” — **rate not stated** | `model.dropout: 0.5` — PyTorch `nn.Dropout()` default, used in [author release `model.py`](https://github.com/yabufarha/ms-tcn/blob/master/model.py) |
| **Batch size** | Not stated | `training.batch_size: 1` — variable-length videos; matches author release training loop |
| **Epochs** | §4.9 mentions **50 epochs** on 50Salads | `training.epochs: 50` |
| **Weight decay** | Not stated | `optimizer.weight_decay: 0.0` — Adam in author release has no weight decay |
| **LR scheduler** | Not stated | `scheduler.name: none` |
| **Class weighting** | Not in MS-TCN paper | `training.class_weighting: true` — **SnatchPhaseBench deviation** for imbalanced snatch phases (same policy as frozen LSTM protocol) |
| **Feature standardization** | Not in paper (I3D features used as-is) | `training.standardize: train_only` — **SnatchPhaseBench deviation** for pose coordinates |
| **Ignore unlabeled frames** | N/A (all frames labeled in TAS datasets) | `ontology.ignore_label_id: 0` — CE `ignore_index=0` |

### 6.3 Optional (SnatchPhaseBench)

| Parameter | Default | Notes |
|-----------|---------|-------|
| Mixed precision | `false` | Optional AMP on CUDA |
| Early stopping | val macro-F1, patience 15 | Benchmark protocol (not in original paper) |
| Seeds | `[42, 123, 456]` | `configs/benchmark.yaml` |

---

## 7. Mandatory vs optional components

| Component | Mandatory for SnatchPhaseBench | Notes |
|-----------|-------------------------------|-------|
| Multi-stage stack (\(S=4\)) | **Yes** | Core MS-TCN contribution |
| Dilated residual layers (\(L=10\)) | **Yes** | Defines receptive field |
| Softmax inter-stage input | **Yes** | Paper §3.2, Eq. 6 |
| Cross-entropy loss (all stages) | **Yes** | Eq. 7, 13 |
| Truncated smoothing loss | **Yes** | Eq. 8–10; \(\lambda=0.15, \tau=4\) |
| Feature concat to higher stages | **No** | Paper Table 5: hurts performance |
| KL smoothing loss | **No** | Paper Table 3: T-MSE preferred |
| I3D features | **No** | Replaced by MediaPipe pose |
| Single-stage TCN baseline | **No** | Ablations only |
| MS-TCN++ dual dilated layer | **No** | Separate future model (`ms_tcn_pp`) |

---

## 8. Documented deviations (SnatchPhaseBench)

| # | Deviation | Rationale |
|---|-----------|-----------|
| D1 | **Pose input (99-d)** instead of I3D (2048-d) | Benchmark v1 fixed extractor policy |
| D2 | **Train-only feature standardization** | Stabilize coordinate scales across athletes |
| D3 | **Class-weighted CE** | Mitigate phase imbalance (dataset §class distribution) |
| D4 | **`ignore_index=0`** for `unlabeled` frames | Seven-class ontology includes unsupervised frames |
| D5 | **Padding masks** in conv layers | Enable batched training (author release pattern) |
| D6 | **Conv1D padding = dilation** | Matches author release (equivalent length for kernel 3) |
| D7 | **Early stopping** on validation macro-F1 | Benchmark training budget control (not in paper) |
| D8 | **Dropout = 0.5** | Not in paper text; author release default (see §6.2) |

No deviation is introduced silently — all appear in this file and in `configs/benchmark/ms_tcn.yaml` comments.

---

## 9. Ambiguities (resolved or flagged)

| Topic | Resolution |
|-------|------------|
| Dropout rate | **Resolved:** 0.5 via author release default (§6.2) |
| Batch size | **Resolved:** 1 (author release) |
| Epoch count | **Resolved:** 50 (paper §4.9 training reference) |
| Weight decay | **Resolved:** 0.0 (author release Adam) |
| Smoothing on logits vs probabilities | **Resolved:** author release applies T-MSE on log-softmax of **logits**; SnatchPhaseBench matches release |

---

## 10. References in repository

- Config: `configs/benchmark/ms_tcn.yaml`
- Model code: `src/snatch_phase_bench/models/ms_tcn/`
- Trainer: `src/snatch_phase_bench/training/ms_tcn_trainer.py`
- Usage: `docs/benchmark/MS_TCN_USAGE.md`
- Integration: `docs/benchmark/MS_TCN_INTEGRATION.md`
