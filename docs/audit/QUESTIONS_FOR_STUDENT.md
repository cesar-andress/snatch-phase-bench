# Questions for the Student (Adrián Cardona Ruiz)

These questions **cannot be answered from the current repository or thesis PDF alone**.  
Do **not** treat any answer as verified until confirmed in writing and, where applicable, backed by artifacts.

---

## 1. Data provenance and licensing

1. **What is the exact source of the 208 competition videos** (e.g., official IWF feed, broadcaster, YouTube channel, event year/location)? Please provide URLs or catalog identifiers where possible.

2. **Do you hold redistribution rights** for the raw videos, extracted keypoints, and annotations for academic publication and Zenodo release?

3. **If public release of videos is not permitted**, are you authorized to publish:
   - pose keypoint CSVs,
   - phase annotations,
   - athlete pseudonymized IDs,
   - trained model weights?

4. **Were all athletes/minors depicted in a context that allows research redistribution**, or are there clips that must remain private?

5. **Is there an institutional or third-party agreement** (university, federation, broadcaster) governing this dataset?

---

## 2. Git LFS and missing binaries

6. **What is the canonical git remote** for the reproducibility package, and was `git lfs pull` required during packaging?

7. On our audit machine, `data/processed/X.npy`, `data/processed/y.npy`, `outputs/lstm_phases/best_model.pt`, and `models/pose_landmarker_full.task` are **Git LFS pointer stubs** (~130 bytes each). Can you provide:
   - a full LFS-enabled clone URL, **or**
   - a direct archive of these four files matching `baseline_tfm/manifest.json`?

8. **`data/processed/meta.csv` is 1,756,579 bytes** in our copy but the manifest expects 1,777,829 bytes, despite 21,249 rows. Was `meta.csv` regenerated after the manifest was frozen?

---

## 3. Annotation protocol

9. **Were all phase annotations performed by a single annotator**, or was there a second reviewer?

10. **What operational criteria** were used to mark boundaries for short phases (especially `transition` and `turnover`)? Is there a written annotation guide beyond the thesis text?

11. **Which annotation script version is canonical** — `annotate_phases.py`, a missing `annotate_phases_final2.py`, or one of the `scripts/legacy/` tools?

12. **Were segment labels (`master_segment_labels.csv`) derived automatically from frame labels**, or annotated independently?

13. **How were `unlabeled` frames defined** (pre-lift, post-lift, ambiguous, between phases)?

---

## 4. Video and capture metadata

14. **Native frame rate and resolution** of the source videos — uniform or mixed?

15. **Camera viewpoints** — mostly side view, front view, or mixed? Is this metadata recorded anywhere?

16. **How were lift attempts selected and trimmed** (`cutting_clips.py`)? Were start/end frames standardized across clips?

17. **Three keypoint files have trailing spaces in filenames** (nagashima i1, nakajima i1/i2). Are these intentional and reflected in `video_relpath` columns?

---

## 5. Training and evaluation details

18. **Exact hardware and OS** used for the final reported run (CPU/GPU model, CUDA version, training time)?

19. **Was the reported checkpoint trained on `data/processed/` tensors exactly as committed**, or on an earlier local build?

20. **Why does training stop after 13 epochs** in `history.csv` when `patience=8` and best val macro-F1 appears at epoch 5? Was training restarted or truncated manually?

21. **Was any post-processing applied to predictions** before generating figures (smoothing, majority vote), or are reported metrics purely per-window argmax?

22. **Were all figures in the thesis generated from the current repository state**, including paths under `outputs/tfm_figures/`?

---

## 6. Environment and dependencies

23. **`openai==2.32.0` appears in `requirements-original.txt` but is unused in code.** Was this dependency accidental?

24. **Are there any manual steps not committed** (spreadsheet edits, filename fixes, external pose re-export) required before reproduction?

25. **Was Python 3.12.3 (or another exact patch version) used exclusively**, or were multiple versions tested?

---

## 7. Scientific scope for follow-up paper

26. **Are you and your supervisor agreeable to reframing the contribution as a public benchmark** (SnatchPhaseBench) rather than an LSTM application paper?

27. **Would you support a second-annotator study** on a subset to estimate inter-rater agreement?

28. **Are there additional clips or athletes** not included in the 208-video release?

---

## Questions intentionally excluded (already answered in repo/thesis)

The following are documented and should **not** be re-asked unless contradictions appear:

- Number of videos (208), athletes (70), classes (7 useful + unlabeled)
- Window size (31), stride (1), features (99)
- Athlete split sizes (49/10/11)
- LSTM hyperparameters (hidden 128, layers 1, dropout 0.2, etc.)
- Reported test accuracy (0.9518) and macro F1 (0.9186) in saved JSON
- MediaPipe Pose Landmarker as pose backend
