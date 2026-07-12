# Checkpoint validation report

**Date:** 2026-07-13  
**Status:** **VERIFIED** — all metrics **EXACT** vs thesis artifact  
**Evaluator:** `snatch_phase_bench.evaluation.checkpoint_eval.evaluate_checkpoint`  
**Machine-readable output:** [`reports/checkpoint_validation.json`](reports/checkpoint_validation.json)

---

## 1. Evaluation setup

| Item | Value |
|------|-------|
| Checkpoint (canonical) | `outputs/baseline/best_model.pt` |
| Checkpoint SHA-256 | `ea5ff9ca8a6dd163ad88efe06e1e221ae1b06393538c365b6c185faa7ef6b7fb` |
| Processed data | `data/processed/rebuilt/` (`X.npy`, `y.npy`, `meta.csv`) |
| Split | `Paper_TFM-main/outputs/lstm_phases/athlete_split.json` (read-only) |
| Thesis reference | `Paper_TFM-main/outputs/lstm_phases/classification_report.json` |
| Mode | **Evaluate only** (no retrain, no fine-tune) |
| PyTorch | 2.10.0 (CPU) |
| `matches_saved_report` | **`true`** |

---

## 2. Global metrics

| Metric | Thesis | Evaluated | \|Δ\| | Status |
|--------|--------|-----------|------|--------|
| Accuracy | 0.9517668300232138 | 0.9517668300232138 | 0.0 | **EXACT** |
| Macro precision | 0.9132237952982087 | 0.9132237952982087 | 0.0 | **EXACT** |
| Macro recall | 0.9250259239618474 | 0.9250259239618474 | 0.0 | **EXACT** |
| Macro F1 | 0.9186193964811207 | 0.9186193964811207 | 0.0 | **EXACT** |
| Weighted precision | 0.9537798429829668 | 0.9537798429829668 | 0.0 | **EXACT** |
| Weighted recall | 0.9517668300232138 | 0.9517668300232138 | 0.0 | **EXACT** |
| Weighted F1 | 0.9523614152610658 | 0.9523614152610658 | 0.0 | **EXACT** |
| Test windows (predictions) | 3877 | 3877 | 0 | **EXACT** |

---

## 3. Per-class metrics

| Phase | Metric | Thesis | Evaluated | \|Δ\| | Status |
|-------|--------|--------|-----------|------|--------|
| setup | Precision | 0.9746070133010882 | 0.9746070133010882 | 0.0 | EXACT |
| setup | Recall | 0.9829268292682927 | 0.9829268292682927 | 0.0 | EXACT |
| setup | F1 | 0.978749241044323 | 0.978749241044323 | 0.0 | EXACT |
| setup | Support | 820 | 820 | 0 | EXACT |
| first_pull | Precision | 0.9282051282051282 | 0.9282051282051282 | 0.0 | EXACT |
| first_pull | Recall | 0.9118387909319899 | 0.9118387909319899 | 0.0 | EXACT |
| first_pull | F1 | 0.9199491740787802 | 0.9199491740787802 | 0.0 | EXACT |
| first_pull | Support | 397 | 397 | 0 | EXACT |
| transition | Precision | 0.8151260504201681 | 0.8151260504201681 | 0.0 | EXACT |
| transition | Recall | 0.8290598290598291 | 0.8290598290598291 | 0.0 | EXACT |
| transition | F1 | 0.8220338983050848 | 0.8220338983050848 | 0.0 | EXACT |
| transition | Support | 117 | 117 | 0 | EXACT |
| second_pull | Precision | 0.9346733668341709 | 0.9346733668341709 | 0.0 | EXACT |
| second_pull | Recall | 0.9117647058823529 | 0.9117647058823529 | 0.0 | EXACT |
| second_pull | F1 | 0.9230769230769231 | 0.9230769230769231 | 0.0 | EXACT |
| second_pull | Support | 204 | 204 | 0 | EXACT |
| turnover | Precision | 0.9073482428115016 | 0.9073482428115016 | 0.0 | EXACT |
| turnover | Recall | 0.9403973509933775 | 0.9403973509933775 | 0.0 | EXACT |
| turnover | F1 | 0.9235772357723577 | 0.9235772357723577 | 0.0 | EXACT |
| turnover | Support | 302 | 302 | 0 | EXACT |
| catch | Precision | 0.8357142857142857 | 0.8357142857142857 | 0.0 | EXACT |
| catch | Recall | 0.9335106382978723 | 0.9335106382978723 | 0.0 | EXACT |
| catch | F1 | 0.8819095477386935 | 0.8819095477386935 | 0.0 | EXACT |
| catch | Support | 376 | 376 | 0 | EXACT |
| recovery | Precision | 0.9968924798011187 | 0.9968924798011187 | 0.0 | EXACT |
| recovery | Recall | 0.9656833232992174 | 0.9656833232992174 | 0.0 | EXACT |
| recovery | F1 | 0.981039755351682 | 0.981039755351682 | 0.0 | EXACT |
| recovery | Support | 1661 | 1661 | 0 | EXACT |

---

## 4. Confusion matrix

| Item | Value |
|------|-------|
| Shape | 7 × 7 (seven phase classes) |
| Element-wise match vs thesis | **Not independently stored in thesis JSON**; implied by identical sklearn classification report and `matches_saved_report: true` |

The thesis artifact stores aggregate precision/recall/F1/support only. Confusion-matrix cells were not exported separately; exact reproduction of the classification report confirms identical predictions under the frozen evaluator.

---

## 5. Discrepancy investigation

**Result:** No metric discrepancies. Investigation not required for numerical mismatch.

Supporting evidence:

1. Rebuilt `X.npy` / `y.npy` SHA-256 match `baseline_tfm/manifest.json`.
2. Test partition: 3,877 windows, 11 athletes — matches thesis split JSON.
3. Evaluator loads checkpoint `mean`/`std` and `model_state_dict` from the recovered binary; bitwise-identical metrics to `classification_report.json`.

Known **non-metric** gaps (unchanged by this validation):

| Issue | Evidence | Affects checkpoint eval? |
|-------|----------|--------------------------|
| Snapshot `outputs/lstm_phases/best_model.pt` is LFS pointer | 131-byte stub | **No** — canonical copy used |
| CPU retrain ≠ checkpoint | `phase2_results.json` retraining block | **No** — separate approximate path |
| Frame count thesis vs audit (37,125 vs 35,825) | Phase 1 audit | **No** — window tensors match manifest |

---

## 6. Conclusion

The recovered `best_model.pt` **exactly reproduces** all thesis metrics on the rebuilt dataset in the canonical environment.

**Baseline reproduction phase: CLOSED (success).**

Proceed to benchmark tier development (B0 rule-based, B1–B3 TAS per [`BENCHMARK_PLAN.md`](../benchmark/BENCHMARK_PLAN.md)) without re-validating this checkpoint unless the artifact or data pipeline changes.
