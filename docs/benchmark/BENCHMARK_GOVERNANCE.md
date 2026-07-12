# SnatchPhaseBench — Benchmark Governance

**Parent document:** [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md)  
**Status:** Active policy (Phase 3+)  
**Version:** governance-v1.0

---

## 1. Purpose

Define **versioning, compatibility, and deprecation rules** so benchmark results remain comparable over time and reproducible claims stay auditable.

---

## 2. Versioned artifacts

| Artifact | Version ID format | Current | Authority doc |
|----------|-------------------|---------|---------------|
| **Dataset** | `ds-YYYY-MM-DD` or `ds-vMAJOR.MINOR` | `ds-v1.0` (rebuilt tensors) | [`BASELINE_SPECIFICATION.md`](BASELINE_SPECIFICATION.md) §2 |
| **B1 checkpoint** | `B1-repro-vMAJOR` | `B1-repro-v1` | [`BASELINE_SPECIFICATION.md`](BASELINE_SPECIFICATION.md) |
| **Benchmark protocol** | `protocol-vMAJOR.MINOR` | `protocol-v1.0-draft` | This tree |
| **Evaluation code** | `eval-vMAJOR.MINOR` (git tag) | tracks `main` | `pyproject.toml` / git |
| **Split file** | SHA-256 of `athlete_split.json` | fixed snapshot hash | [`../reproduction/reports/split_validation.md`](../reproduction/reports/split_validation.md) |
| **Statistical protocol** | `stats-vMAJOR.MINOR` | `stats-v1.0-draft` | [`STATISTICAL_PROTOCOL.md`](STATISTICAL_PROTOCOL.md) |
| **Model runs** | `<registry>-<config-hash>-<seed>` | — | `outputs/benchmark/` |

Every published result row must cite: `{dataset version, split hash, eval version, protocol version}`.

---

## 3. Dataset version policy

### 3.1 Current dataset (`ds-v1.0`)

| Field | Value |
|-------|-------|
| Tensors | `data/processed/rebuilt/` |
| X SHA-256 | `8497a69a2c6d80f24c0fc6242500aa931ab2c00e8172b534a98f86d92ed698b4` |
| y SHA-256 | `0175c1c314fd22fef37d4b16a96b038d4643765c323c8b13599ff9a9b17c3546` |
| Windows | 21,249 |
| Labels | Seven-phase thesis ontology |

### 3.2 Minor bump (`ds-v1.x`)

Permitted without resetting benchmark leaderboard:

- Documentation fixes
- `meta.csv` column additions (non-label)
- Bug fixes in builder that **preserve tensor checksums**

### 3.3 Major bump (`ds-v2.0`)

**Required when:**

- Label ontology changes (5-phase merge, relabeling)
- Preprocessing formula changes (normalization, window size, stride)
- Keypoint source changes for benchmark v1 table
- Split file changes

**Actions on major bump:**

1. Increment dataset version
2. Re-validate B1 checkpoint or mark B1 as legacy-only
3. Re-run all benchmark models
4. Publish migration note

---

## 4. Baseline version policy

### 4.1 B1 (thesis LSTM) — frozen

| Rule | Detail |
|------|--------|
| Immutability | `outputs/baseline/best_model.pt` checksum must match `ea5ff9ca…b7fb` |
| Code freeze | Modules listed in [`../FROZEN_BASELINE.md`](../FROZEN_BASELINE.md) |
| New checkpoint | New version ID (`B1-repro-v2`); never overwrite v1 |
| Evaluation | Window-level metrics only; deterministic on CPU |

### 4.2 B0 (rule-based) — versioned config

| Field | Tracked |
|-------|---------|
| Thresholds | YAML `configs/benchmark/rule_knee_angle.yaml` |
| Joint definitions | Version with ontology (EXP-ONT) |
| Code hash | Git commit |

Any threshold change → increment `B0-vMAJOR`.

### 4.3 B2/B3 models — versioned by config hash

Each run logs:

```yaml
model_registry: ms_tcn
config_path: configs/benchmark/ms_tcn.yaml
config_sha256: <hash>
seeds: [42, 123, 456]
dataset_version: ds-v1.0
split_sha256: <hash>
eval_version: <git tag or commit>
```

---

## 5. Evaluation version policy

### 5.1 Metric modules

| Change type | Version bump |
|-------------|--------------|
| Bug fix (numeric change) | **eval MAJOR** + re-run all models |
| New optional metric | eval MINOR |
| Performance only | PATCH |

### 5.2 Regression tests

Mandatory before merging eval changes:

- B1 checkpoint eval → EXACT legacy metrics
- Golden segment/boundary files on synthetic sequences

---

## 6. Benchmark protocol version policy

| Change | Action |
|--------|--------|
| Inclusion criteria change | protocol MAJOR |
| New mandatory model in B2-core | protocol MAJOR + re-run |
| Statistical requirement change | stats MAJOR |
| Clarification only | protocol MINOR |

---

## 7. Compatibility matrix

|  | Same ds | New ds major | New eval major |
|--|---------|--------------|----------------|
| **B1 checkpoint** | ✅ Valid | ⚠ Re-validate | ⚠ Re-validate |
| **B0 results** | ✅ Comparable | ❌ Re-run | ⚠ Re-run if metrics changed |
| **B2 results** | ✅ Comparable | ❌ Re-run | ⚠ Re-run if metrics changed |
| **Manuscript tables** | ✅ | ❌ Regenerate | ⚠ Regenerate affected columns |

---

## 8. Deprecation policy

| Item | Deprecation rule |
|------|------------------|
| Old split files | Deprecated immediately if athlete assignments change; keep archived with SHA |
| Retrain LSTM proxy | Never official; deprecated for claims (use B1 checkpoint) |
| Window-only comparisons | Deprecated for B2; allowed for B1 row only |
| Legacy tier naming (B1=MS-TCN) | Deprecated in docs; use [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md) hierarchy |
| Clip-random splits | **Forbidden** — not deprecated, rejected |

Deprecation notice minimum: **one protocol MINOR version** documented in CHANGELOG before removal.

---

## 9. Release and publication governance

### 9.1 Pre-submission gate

All must pass:

- [ ] G0: B1 checkpoint validated — **DONE**
- [ ] G1: Phase ontology reconciled (EXP-ONT)
- [ ] G2: B0 + boundary metrics on ds-v1.0
- [ ] G3: B2-core complete with statistical protocol
- [ ] G4: Manuscript numbers trace to versioned artifacts

### 9.2 Zenodo bundle contents

| Artifact | Include |
|----------|---------|
| Split JSON | Yes |
| Config YAMLs | Yes |
| Eval scripts | Yes |
| B1 checkpoint | Yes (when legal) |
| Processed tensors or rebuild script | Yes |
| Raw videos | Only if licensed |

---

## 10. Roles and change control

| Change | Approver |
|--------|----------|
| ds MAJOR / label change | PI + domain expert |
| B1 code/threshold change | PI + re-validation |
| B0 threshold / ontology | Domain expert |
| Eval metric definition change | PI + regression tests |
| New B2-core mandatory model | PI + protocol MAJOR bump |

All changes recorded in git with reference to experiment ID from [`EXPERIMENT_MATRIX.md`](EXPERIMENT_MATRIX.md).

---

## 11. Audit trail

Each benchmark run must produce `manifest.json`:

```json
{
  "dataset_version": "ds-v1.0",
  "split_sha256": "...",
  "protocol_version": "protocol-v1.0",
  "stats_version": "stats-v1.0",
  "eval_git_commit": "...",
  "model": "ms_tcn",
  "config_sha256": "...",
  "seeds": [42, 123, 456],
  "outputs": {"predictions": "...", "metrics": "..."}
}
```

---

## 12. Related documents

- [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md)
- [`BASELINE_SPECIFICATION.md`](BASELINE_SPECIFICATION.md)
- [`../FROZEN_BASELINE.md`](../FROZEN_BASELINE.md)
- [`../SCIENTIFIC_WORKFLOW.md`](../SCIENTIFIC_WORKFLOW.md)
- [`../release/PUBLICATION_STRATEGY.md`](../release/PUBLICATION_STRATEGY.md)
