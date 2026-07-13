# Missing content from thesis → journal paper

**Thesis PDF (read-only):** `~/Descargas/BMEM_49028285-54566-260531200716 - TFM_-_IA_para_la_deteccion_del_gesto_tecnico_de_la_arrancada_en_halterofilia (1).pdf`

Each row is an important idea **not yet fully present** in the manuscript or canonical docs. Page numbers refer to the thesis PDF body (approximate from text extraction).

| ID | Thesis chapter | Page (approx.) | Description | Paper destination | Rewrite? |
|----|----------------|----------------|-------------|-------------------|----------|
| M01 | Cap. 3 | 8 | Olympic HD video search, download, clip delimitation workflow | §3 Dataset (`sec:dataset:videos`) | Yes — legal tone |
| M02 | Cap. 5 | 14–15 | Filename encodes modality, weight class, athlete, attempt, ok/fail, global id | §3 Dataset + App. A | Yes — table |
| M03 | Cap. 5 | 14–15 | Four-level data layout: raw / annotations / keypoints / processed | §3 + `fig:pipeline` | Yes — remove wl_clips paths |
| M04 | Cap. 5 | 15 | Segment labels: 1,766 segments in master (verify vs repo) | §3 Annotations + segment eval | Yes |
| M05 | Cap. 5 | 15 | Frame labels: thesis claims 37,125 rows (**resolved:** 35,825 canonical) | §3 + App. A | Done — see `AUTHOR_CLARIFICATIONS.md` |
| M06 | Cap. 6.2 | 17 | Interactive OpenCV annotation: frame navigation, dual export | §3 Annotations + future `ANNOTATION_PROTOCOL.md` | Yes |
| M07 | Cap. 6.2 | 17 | Canonical script name drift (`annotate_phases_final2.py`) | App. B reproducibility note | Yes — factual |
| M08 | Cap. 6.3 | 18 | Pose extraction: skip existing, restrict to master CSV list | §4 Methods preprocessing / App. B | Yes |
| M09 | Cap. 6.6 | 19 | **Per-split phase counts** (setup 4006/1191/820, etc.) | App. A or new `tab:split_phase_distribution` | Minimal — table |
| M10 | Cap. 6.6 | 19 | Split percentages 70/14/16 by athlete count | §3 splits (optional) | Minimal |
| M11 | Cap. 6.10 | 21 | Limitation: no formal automated tests in original repo | §8 Limitations | Minimal |
| M12 | Cap. 7.2 | 22–23 | Best val epoch **5**, val macro-F1 **0.8991**, train macro-F1 0.9154 | `fig:training_curves` caption; App. C | Yes — gate metrics |
| M13 | Cap. 7.3 | 24 | Per-phase test F1: transition **0.822**, catch **0.882** | `tab:baseline_perclass` | No — populate after gate |
| M14 | Cap. 7.3 | 24 | Interpretation: setup/recovery stable; transition/catch hard | §7 Discussion (`sec:discussion:interpretation`) | Yes — evidence-linked |
| M15 | Cap. 7.4 | 25–26 | Confusion pairs: first_pull↔transition, transition↔second_pull, turnover↔catch, catch↔recovery | §7 + `fig:confusion_matrix` | Yes — after CM |
| M16 | Cap. 4.3 | 11 | Barbell trajectory CV (Balsalobre smartphone; Nagao auto-tracking) as related work | §2 Related Work (`sec:related:wl`) | Yes — verify cites |
| M17 | Cap. 4.4 | 12 | Windowing rationale + subject-level evaluation (Aleksic vertical jump) | §5 Protocol overlap | Yes |
| M18 | Cap. 4.5 | 13 | Explicit gap statement: no full pipeline for snatch phase segmentation | §2 gap paragraph | Yes — benchmark framing |
| M19 | Cap. 9 | 32 | Multi-annotator agreement recommendation | §8 Limitations + future work | Yes |
| M20 | Cap. 9 | 32 | Derived biomechanical features (angles, velocities, bar path) | Benchmark ablation plan; §7 future | Yes |
| M21 | Cap. 9 | 32–33 | Architecture comparison GRU/TCN/Transformer | §4 benchmark placeholders (done) | No — already structured |
| M22 | Cap. 9 | 33 | Real-time / clean & jerk extension | §7 Future work | Minimal |
| M23 | Cap. 1 | 5 | Snatch described as 3 biomechanical pulls vs 7 annotated phases | §3 taxonomy note | Yes — reconcile ontology |
| M24 | Cap. 2 | 6 | Bar speed up to **1.90 m/s** (Cao et al.) | §1 motivation (optional) | Yes — if cite verified |
| M25 | — | — | **Stride-1 overlap** not in thesis | §5 `sec:protocol:overlap`, §8 | N/A — repo adds this |

---

## Already incorporated (do not re-copy verbatim)

- Dataset counts 208/70/21249/31/99/7 (Cap. 5–6) → `tab:dataset_stats`, `tab:split_stats`, `tab:class_distribution`
- Athlete-level split rationale (Cap. 6.6) → §3, §5
- LSTM hyperparameters (Table 6.7.1) → `tab:lstm_hyperparams`
- Preprocessing chain (Cap. 6.4–6.5) → §4 Methods
- High-level limitations (Cap. 6.10, 8) → §8 Limitations
- Future architectures & dataset expansion (Cap. 9) → benchmark plan, §7 outline

---

## Do not transfer

| Thesis content | Reason |
|----------------|--------|
| Placeholder Resumen/Abstract | Incomplete |
| MSc “objetivos cumplidos” tables (7.6.1, 8) | TFM administrative |
| “Sistema funcional capaz de…” as journal conclusion | Overclaims vs benchmark scope |
| Long tutorial subsections in Cap. 4.1–4.2 | Replace with verified related work |
| `wl_clips/` directory paths | Obsolete vs canonical repo |
| Window accuracy as segmentation success | Methodological mismatch |

---

## Suggested transfer order

1. M05 — resolve frame count  
2. M01, M02, M03 — provenance and schema  
3. M09 — split-phase table  
4. M12–M15 — results/discussion (post checkpoint)  
5. M16, M18 — related work gap  
6. M19–M22 — future work alignment  

Track progress in [`WRITING_ROADMAP.md`](WRITING_ROADMAP.md) and [`../snatch-phase-bench/docs/paper/PAPER_TODO.md`](../snatch-phase-bench/docs/paper/PAPER_TODO.md).
