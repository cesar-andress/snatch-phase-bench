# Reviewer checklist

**Source:** Reviewer red-team analysis in [`SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md) Part 10.

Each item lists why reviewers may raise the criticism, current repository status, remaining work, and mitigation strategy.

---

## 1. “Why not a rule-based knee-angle threshold?”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Weightlifting biomechanics defines snatch phases via knee-extension-angle changes; markerless validity literature shows knee angles recoverable to ~few degrees RMSD. A learned model must justify its complexity. |
| **Current status** | **Mitigated** for checkpoint; **Not mitigated** for B0 rule baseline. Literature foundation ranks B0 as the single most dangerous reviewer question. |
| **Remaining work** | Implement `rule_knee_angle` segmenter per [`../benchmark/BENCHMARK_PROTOCOL.md`](../benchmark/BENCHMARK_PROTOCOL.md); compute boundary-ms metrics. |
| **Mitigation** | Include B0 as **first-class baseline** (tier B0) in all comparison tables. See [`../benchmark/BENCHMARK_PROTOCOL.md`](../benchmark/BENCHMARK_PROTOCOL.md) §7. |

---

## 2. “No methodological novelty — applied TAS.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | MS-TCN, ASFormer, etc. are published; applying them to a new dataset is incremental at methods venues (e.g. Pattern Recognition). |
| **Current status** | **Partially mitigated.** Paper abstract and `research_design.md` shift toward benchmark framing; no method novelty claims in manuscript results. |
| **Remaining work** | Ensure abstract/intro never claim new architecture; target benchmark-friendly venues. |
| **Mitigation** | Claim dataset + benchmark + boundary-timing formalization. Foreground boundary-ms evaluation as conceptual increment. Avoid Pattern Recognition as primary target. |

---

## 3. “Dataset too small / not diverse.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | 208 videos / 70 athletes may be modest vs Breakfast or FineGYM; generalization unclear. |
| **Current status** | **Partially mitigated.** Counts verified and documented in `docs/dataset/dataset.md`. Demographics, camera diversity, weight classes **unknown**. |
| **Remaining work** | Collect and publish metadata table; scope claims as “first benchmark” not “definitive”; power analysis if comparing many models. |
| **Mitigation** | Transparent dataset statistics table; athlete-disjoint evaluation; honest limitation subsection. |

---

## 4. “Pose signal unreliable for overhead catch.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Theia3D validation shows upper-limb and hip rotation weaknesses; snatch catch involves occlusion by plates and extreme arm positions. |
| **Current status** | **Acknowledged** in paper limitations and `dataset.md`; **not quantified** on this dataset. |
| **Remaining work** | Pose-error subset vs reference (if available); occlusion/motion-blur ablation; per-transition error breakdown. |
| **Mitigation** | Measure impact on boundary MAE at catch/turnover transitions; cite Theia3D limitations honestly. |

---

## 5. “Data leakage / clip-level splits.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Random clip splits leak athlete style across train/test; stride-1 windows amplify dependence. |
| **Current status** | **Mitigated.** Athlete-level split validated (no athlete/video overlap); documented in reproduction reports and tests. |
| **Remaining work** | Prominently state in paper abstract; ship split JSON with release; add LOAO/k-fold for uncertainty. |
| **Mitigation** | Never use clip-random splits; automated test `test_split_validation.py` in CI. |

---

## 6. “Results depend on the pose extractor you picked.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Different extractors (OpenPose, HRNet, MediaPipe) yield different keypoints; benchmark may not transfer. |
| **Current status** | **Not mitigated.** MediaPipe fixed in thesis pipeline; no extractor ablation. |
| **Remaining work** | Pose-extractor swap experiment (HRNet, RTMPose); report metric variance. |
| **Mitigation** | Fix extractor for benchmark v1 but document sensitivity; plan v2 with alternate extractor. |

---

## 7. “Metrics saturate — easy 5-class problem.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Long phases (setup, recovery) dominate frame accuracy; high window accuracy may hide poor boundaries. |
| **Current status** | **Partially mitigated.** Class imbalance documented; overlap/autocorrelation analyzed; segment metrics implemented but not reported. |
| **Remaining work** | Lead with boundary-ms and F1@50; per-transition table; show Second Pull→Turnover is not saturated. |
| **Mitigation** | De-emphasize window accuracy in abstract; use segment-level primary endpoints. |

---

## 8. “Not reproducible.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Sports-CV papers often lack code, splits, and checkpoints. |
| **Current status** | **Strong infrastructure** — config-driven rebuild, manifest hashes, tests, frozen baseline policy. **B1 checkpoint validated** (2026-07-13). |
| **Remaining work** | Zenodo release; CI badge; B0/B2 benchmark runs. |
| **Mitigation** | Reproduction summary + [`../benchmark/BENCHMARK_GOVERNANCE.md`](../benchmark/BENCHMARK_GOVERNANCE.md); public repo. |

---

## 9. “Annotation subjectivity in phase boundaries.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Phase transitions are judgment calls; single annotator undermines ground truth. |
| **Current status** | **Acknowledged** — no inter-annotator agreement (IAA) study in repository. |
| **Remaining work** | Second annotator on subset; report boundary MAE between annotators or κ with frame tolerance; tie definitions to kinematic events where possible. |
| **Mitigation** | Operational definitions from biomechanics literature (Theia3D IJES 2025); document annotation protocol. |

---

## 10. “Overclaimed novelty / gap.”

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Prior work exists on barbell tracking, Theia3D snatch kinematics, deadlift classification, wearable phase segmentation. |
| **Current status** | **Partially mitigated.** Paper Related Work outlines gap; precise gap statement in literature foundation not yet in manuscript prose. |
| **Remaining work** | Add prior-art comparison table (input, method, output, gap); state seam between three communities explicitly. |
| **Mitigation** | Cite barbell-trajectory papers, Theia3D validation, deadlift CV; claim only “reproducible per-frame phase segmentation benchmark from markerless pose.” |

---

## 11. Phase ontology mismatch (internal risk)

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Biomechanics uses five-phase knee-angle ontology; thesis uses seven labels including separate catch/turnover/setup. |
| **Current status** | **Unresolved.** Documented in [`../literature/GAP_ANALYSIS.md`](../literature/GAP_ANALYSIS.md). |
| **Remaining work** | Expert review; mapping table or relabeling; update manuscript taxonomy. |
| **Mitigation** | Do not claim “standard five-phase ontology” until reconciled. |

---

## 12. Window overlap inflates significance

| Field | Detail |
|-------|--------|
| **Why reviewers raise it** | Stride-1 windows share 30/31 frames; test samples are not independent. |
| **Current status** | **Documented** — `temporal_autocorrelation.md`, paper limitations, evaluation framework for frame/segment levels. |
| **Remaining work** | Report frame- and segment-level metrics; discuss effective sample size. |
| **Mitigation** | Statistical testing must account for overlap or use segment-level unit of analysis. |

---

## Summary matrix

| # | Risk | Status | Priority |
|---|------|--------|----------|
| 1 | Rule-based baseline | ❌ Open | **P0** |
| 2 | No method novelty | ⚠️ Partial | P0 (framing) |
| 3 | Small dataset | ⚠️ Partial | P1 |
| 4 | Pose at catch | ⚠️ Acknowledged | P1 |
| 5 | Data leakage | ✅ Mitigated | Maintain |
| 6 | Extractor dependence | ❌ Open | P1 |
| 7 | Metric saturation | ⚠️ Partial | P0 |
| 8 | Reproducibility | ⚠️ B1 verified; release pending | P0 |
| 9 | Annotation subjectivity | ❌ Open | P1 |
| 10 | Overclaimed gap | ⚠️ Partial | P1 |
| 11 | Phase ontology | ❌ Open | **P0** |
| 12 | Window overlap | ⚠️ Documented | P1 |

**Legend:** ✅ Mitigated · ⚠️ Partial · ❌ Open

Update this checklist when benchmark milestones complete (`../benchmark/BENCHMARK_PLAN.md` §9).
