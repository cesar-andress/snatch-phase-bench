# Related Work 2026 audit — SnatchPhaseBench

**Date:** 2026-07-22  
**Manuscript updated:** `~/papers/snatch-phase-bench/paper/sections/02_related_work.tex`  
**Bibliography updated:** `~/papers/snatch-phase-bench/paper/bibliography.bib`  
**Primary source:** OpenAlex API (`OPEN_ALEX_KEY` from `~/.bashrc`)  
**Auxiliary:** DOI resolution via OpenAlex only (no fabricated metadata)  
**Policy:** No citation padding; omit if uncertain.

---

## 1. Keywords searched

Temporal action segmentation; video temporal segmentation; temporal action localization (screened, mostly out of scope for frame-wise TAS); human action segmentation; fine-grained action recognition; skeleton-based temporal action analysis; sports video understanding; Olympic weightlifting / snatch analysis; weightlifting biomechanics; markerless motion capture; MediaPipe Pose; pose estimation in sports; TAS benchmarks; sports CV benchmarks; boundary detection in TAS; MS-TCN; ASFormer; transformer architectures for temporal segmentation.

---

## 2. OpenAlex queries (representative)

| Query theme | Filter / search |
|-------------|-----------------|
| TAS title corpus 2022–2026 | `filter=title.search:temporal action segmentation,publication_year:2022-2026` |
| Boundary TAS | `filter=title.search:boundary action segmentation,publication_year:2020-2026` |
| Transformer TAS | `filter=title.search:transformer action segmentation,publication_year:2022-2026` |
| ASFormer | `search=ASFormer action segmentation` |
| DiffAct | `search=DiffAct action segmentation` |
| Markerless | `filter=title.search:markerless,publication_year:2021-2026` |
| MediaPipe | `search=MediaPipe Pose sports` |
| Snatch (title) | `filter=title.search:snatch,publication_year:2018-2026` |
| FineGym / MultiSports / FineDiving | targeted search + DOI resolve |
| Sports AR surveys | search + DOI `10.1109/TMM.2022.3232034` |
| Skeleton action segmentation | DOI `10.1109/tetc.2022.3230912` |
| Multimodal HAR review | DOI `10.1109/TPAMI.2022.3183112` |

Authenticated OpenAlex requests succeeded with `OPEN_ALEX_KEY`. Broad free-text surveys (e.g. “sports video survey”) were noisy; title/DOI filters were preferred.

---

## 3. Papers evaluated (high-signal subset)

| Paper | Year | Venue (OpenAlex) | Cites* | Decision |
|-------|------|------------------|-------:|----------|
| Ding et al., TAS survey | 2023 | TPAMI | 94 | KEEP (anchor survey) |
| Farha & Gall, MS-TCN | 2019 | CVPR | — | KEEP (B2 baseline) |
| Yi et al., ASFormer | 2021 | BMVC | 75 | KEEP (B3 baseline) |
| Li et al., MS-TCN++ | 2020 | TPAMI | — | KEEP |
| Liu et al., DiffAct | 2023 | ICCV | 82 | KEEP (registered future tier) |
| Lu & Elhamifar, FACT | 2024 | CVPR | 39 | **ADD** (recent transformer TAS) |
| Wang et al., BACS | 2020 | ECCV | 139 | KEEP |
| Ishikawa et al. | 2021 | WACV | 157 | KEEP |
| Du et al., unsupervised boundaries | 2022 | CVPR | 43 | **ADD** |
| Filtjens et al., skeleton TAS | 2022 | IEEE TETC | 70 | **ADD** |
| Sun et al., multimodal HAR review | 2022 | TPAMI | 566 | **ADD** |
| Wu et al., sports AR survey | 2022 | IEEE TMM | 129 | KEEP (DOI verified) |
| Shao et al., FineGym | 2020 | CVPR | — | KEEP |
| Li et al., MultiSports | 2021 | ICCV | — | KEEP |
| Xu et al., FineDiving | 2022 | CVPR | 129 | **ADD** (competing fine-grained sports resource) |
| Wade et al., markerless review | 2022 | PeerJ | 346 | **ADD** |
| Zheng et al., pose survey | 2023 | ACM CSUR | — | KEEP |
| Lugaresi et al., MediaPipe | 2019 | arXiv | — | KEEP |
| Bazarevsky et al., BlazePose | 2020 | arXiv | — | KEEP |
| Cao / Chen / Baumann / Harbili / Thiele / Shah | — | — | — | KEEP (weightlifting line) |
| C2F-TCN (TPAMI 2023) | 2023 | TPAMI | 51 | REJECT (semi-sup focus; not used as baseline) |
| Team-sports AR survey (AIR 2024) | 2024 | AIR | 31 | REJECT (team sports; weak snatch fit) |
| Scataglini et al. markerless meta-analysis | 2024 | Sensors | 123 | REJECT (overlaps Wade; avoid padding) |
| Video Mamba Suite / VideoLLM | 2023–24 | arXiv | — | REJECT (not TAS positioning) |
| Metaverse / XAI hits from noisy survey search | 2022–23 | various | high | REJECT (irrelevant) |

\*Citation counts from OpenAlex at query time (2026-07-22); approximate.

---

## 4. New papers added (6)

| Bib key | Why |
|---------|-----|
| `lu2024fact` | Recent efficient transformer TAS (CVPR 2024); shows ASFormer is not the only modern option while retaining ASFormer as locked B3 |
| `du2022boundary` | CVPR 2022 boundary detection for TAS; strengthens boundary-endpoint motivation |
| `filtjens2022skeleton` | Skeleton-stream action segmentation; bridges ST-GCN literature and TAS |
| `sun2022har` | Broad multimodal HAR review; situates skeleton vs RGB sports pipelines |
| `wade2022markerless` | High-cite markerless MMC limitations review |
| `xu2022finediving` | Fine-grained sports procedure dataset; prevents overclaiming “no sports benchmarks” |

---

## 5. Old papers removed

**None removed from the bibliography.**  
Prose was reorganized; unused risk for `shahroudy2016ntu` was fixed by restoring a one-line NTU mention.

**Prose removals / compressions (not bib deletions):**
- Standalone “Primary sources for the phase taxonomy” section merged into Weightlifting Analysis.
- Separate long “Skeleton-based action recognition” section folded under TAS (skeleton-oriented paragraph).
- Duplicate positioning paragraphs collapsed into **Research Gap**.

---

## 6. Citation audit of previously present keys

| Key | Verdict | Note |
|-----|---------|------|
| `cao2022snatch` | KEEP | Ontology M1–M6 |
| `chen2022snatch` | KEEP | Phase names / barbell CV |
| `baumann1988snatch` | KEEP | Landmark biomechanics |
| `cao2017openpose` | KEEP | Landmark HPE |
| `sun2019hrnet` | KEEP | Landmark HPE |
| `lugaresi2019mediapipe` | KEEP | MediaPipe framework (still appropriate) |
| `bazarevsky2020blazepose` | KEEP | On-device pose companion |
| `chen2020monocular_pose` | KEEP | Older HPE survey |
| `zheng2023pose_survey` | KEEP / UPDATE | Recent HPE survey |
| `kanko2021concurrent` | KEEP | Markerless vs marker gait |
| `uhlrich2023opencap` | KEEP | Smartphone markerless dynamics |
| `harbili2014comparative` | KEEP | Snatch kinematics |
| `thiele2024snatch` | KEEP | Markerless snatch validation |
| `yan2018stgcn` | KEEP | Skeleton GCN landmark |
| `chen2021ctrgcn` | KEEP | Modern skeleton GCN |
| `shahroudy2016ntu` | KEEP | Pose corpus |
| `duan2022posec3d` | KEEP | Skeleton representation |
| `lea2017temporal` | KEEP | ED-TCN |
| `farha2019ms` | KEEP | MS-TCN still appropriate B2 ref |
| `li2020mspp` | KEEP | MS-TCN++ |
| `yi2021asformer` | KEEP | ASFormer still appropriate B3 ref |
| `ding2023temporal` | KEEP | Essential TAS survey |
| `wang2020bacs` | KEEP | Boundary-aware TAS |
| `ishikawa2021boundary` | KEEP | Boundary detection |
| `liu2023diffact` | KEEP | Future-tier method |
| `kuehne2014breakfast` | KEEP | TAS corpus |
| `stein2013salads` | KEEP | TAS corpus |
| `fathi2012gtea` | KEEP | TAS corpus |
| `kim2018wearable` | KEEP | Closest wearable phase segmentation |
| `shao2020finegym` | KEEP | Fine-grained sports |
| `li2021multisports` | KEEP | Sports ST localization |
| `wu2022sportsvideo` | KEEP | Sports AR survey (DOI verified) |
| `pineau2021reproducibility` | KEEP | Reproducibility framing |
| `kapoor2023leakage` | KEEP | Split leakage |
| `shah2026barbell` | KEEP | Barbell CV (metadata note retained) |
| `snatchphasebench_repo` | KEEP | Artifact pointer |

**MS-TCN / ASFormer:** Still the most appropriate locked baselines for a 2026 submission that already reports B2/B3. FACT is cited as a *recent direction*, not a replacement baseline. DiffAct++ (TPAMI 2024) exists but was not added to avoid padding; ICCV DiffAct remains sufficient for the registered future tier.

**MediaPipe:** Lugaresi et al. (framework) + BlazePose remain the correct citations; no newer MediaPipe *Pose* landmark paper displaced them in OpenAlex screening.

---

## 7. Citation graph summary (narrative)

```text
Biomechanics (Baumann → Harbili → Cao/Thiele)
        \
         → Weightlifting CV (Chen, Shah) ──┐
Sports surveys (Wu, Sun) / FineGym / MultiSports / FineDiving ──┤
TAS core (Lea → MS-TCN → ASFormer → Ding; boundary: Wang/Ishikawa/Du) ─┤
Pose (OpenPose/HRNet/MediaPipe; Zheng/Wade validity) ──────────────────┴→ SnatchPhaseBench gap
```

SnatchPhaseBench sits at the intersection of short-horizon TAS metrics, markerless pose inputs, and snatch phase semantics—not as a claim that no sports datasets exist.

---

## 8. Competing / neighbouring benchmarks discovered

| Resource | Modality | Sport | Annotations | Temporal grain | Public | Protocol vs SnatchPhaseBench |
|----------|----------|-------|-------------|----------------|--------|------------------------------|
| 50Salads / Breakfast / GTEA | RGB (+sensors) | Cooking / ADL | Frame actions | Long procedural | Yes | Different domain/duration |
| FineGym | RGB | Gymnastics | Hierarchical actions | Fine-grained events | Yes | Not snatch; not pose-phase TAS |
| MultiSports | RGB | Multi-person sports | Spatio-temporal tubes | Localized actions | Yes | Multi-person localization |
| FineDiving | RGB | Diving | Procedure / AQA | Procedure-aware | Yes | Quality assessment, not snatch pose phases |
| Kim & Kim IMU | Wearable | Sports motions | Boundary states | Online segments | Paper | Modality differs |
| Thiele snatch | Marker / markerless | Snatch | Kinematic phases | Event-based | No public TAS | Validation, not learned benchmark |

**Contribution beyond them:** athlete-disjoint **snatch phase** labels on **fixed MediaPipe pose**, locked MS-TCN/ASFormer baselines, and **boundary MAE** co-reported with segment F1—not a claim of being the only sports video dataset.

---

## 9. Remaining literature gaps

- Few peer-reviewed **snatch phase TAS** papers with public pose labels and shared splits.
- Limited **pose-stream TAS** benchmarks relative to RGB TAS.
- No LOAO multi-split literature baseline for this exact task (future work).
- IAA literature for snatch phase boundaries still absent (labels pending).
- Optional: DiffAct++ / more 2025 skeleton TAS transformers if future model tiers are activated.

---

## 10. Final assessment

**Is the Related Work ready for submission?**  
**Yes, with the usual caveats:** it is comprehensive for the paper’s claim, cites verified 2022–2024 updates, avoids “no benchmark exists,” and motivates SnatchPhaseBench precisely. Re-check `shah2026barbell` publisher metadata at camera-ready if the journal requires it.

---

*End of RELATED_WORK_2026_AUDIT.md*
