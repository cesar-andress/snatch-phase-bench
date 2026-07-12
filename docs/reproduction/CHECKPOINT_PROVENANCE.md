# Checkpoint provenance — `best_model.pt`

**Status:** Verified reproduction artifact (2026-07-13)  
**Canonical copy:** `outputs/baseline/best_model.pt` (this repository)

---

## Identity

| Field | Value |
|-------|-------|
| **File name** | `best_model.pt` |
| **Expected size** | 478,137 bytes |
| **SHA-256** | `ea5ff9ca8a6dd163ad88efe06e1e221ae1b06393538c365b6c185faa7ef6b7fb` |
| **Format** | PyTorch checkpoint (ZIP archive; contains `model_state_dict`, `mean`, `std`, `class_ids`, hyperparameters) |
| **LFS OID (manifest)** | `sha256:ea5ff9ca8a6dd163ad88efe06e1e221ae1b06393538c365b6c185faa7ef6b7fb` |

---

## Original location (read-only student snapshot)

| Path | Status at recovery |
|------|-------------------|
| `~/papers/Paper_TFM-main/best_model.pt` | **Real binary** (478,137 B) — recovered artifact used for validation |
| `~/papers/Paper_TFM-main/outputs/lstm_phases/best_model.pt` | Git LFS pointer stub (131 B) — **not** the weights file |

The student export listed the checkpoint under `outputs/lstm_phases/` in documentation and `baseline_tfm/manifest.json`, but the **recovered weights file** was provided at the snapshot root (`Paper_TFM-main/best_model.pt`). Checksum matches the manifest entry for `outputs/lstm_phases/best_model.pt`.

---

## Recovery record

| Item | Detail |
|------|--------|
| **Date received** | 2026-07-13 (file mtime on recovered binary: 2026-07-13 00:29 UTC+2) |
| **Provided by** | Project team / student (via restored binary in read-only snapshot; no modification to snapshot) |
| **How obtained** | Binary placed in `~/papers/Paper_TFM-main/best_model.pt`; verified by size and SHA-256 against `Paper_TFM-main/baseline_tfm/manifest.json` |
| **Immutability policy** | Original snapshot paths are **read-only**; canonical repo uses a **copy** only |

---

## Canonical repository copy

```text
snatch-phase-bench/outputs/baseline/best_model.pt
```

| Field | Value |
|-------|-------|
| Copy date | 2026-07-13 |
| Copy method | `cp -p` (preserve timestamp) from read-only snapshot root |
| Post-copy SHA-256 | `ea5ff9ca8a6dd163ad88efe06e1e221ae1b06393538c365b6c185faa7ef6b7fb` |
| Git tracking | **Not committed** (see `.gitignore`; binary stays local / Zenodo release) |

Sidecar metadata: `outputs/baseline/best_model.pt.sha256`

---

## Related thesis artifacts (read-only snapshot)

| Artifact | Path (snapshot) | Role |
|----------|-----------------|------|
| Saved metrics | `outputs/lstm_phases/classification_report.json` | Thesis reference report |
| Split | `outputs/lstm_phases/athlete_split.json` | Test athletes (11) |
| Processed tensors (reference) | `data/processed/X.npy`, `y.npy` | Original training/eval tensors (LFS in export) |
| Manifest | `baseline_tfm/manifest.json` | Expected checksums |

---

## Verification cross-links

- Evaluation report: [`CHECKPOINT_VALIDATION.md`](CHECKPOINT_VALIDATION.md)
- Frozen baseline spec: [`../benchmark/BASELINE_SPECIFICATION.md`](../benchmark/BASELINE_SPECIFICATION.md)
- Evaluation JSON: [`reports/checkpoint_validation.json`](reports/checkpoint_validation.json)
