# Video metadata audit — SnatchPhaseBench raw videos

**Date:** 2026-07-22
**Source directory:** `/home/cesar/papers/snatch-phase-bench/raw_videos`
**Method:** `ffprobe` stream/format metadata for every file; CFR/VFR classified from **decoded frame** `best_effort_timestamp_time` deltas (not packet PTS, which are misleading under H.264 B-frames).
**Policy:** Read-only audit. Dataset files were not modified.

---

## 1. Summary statistics

| Quantity | Value |
|----------|-------|
| Number of videos | **208** |
| Athlete directories | 70 |
| Unique FPS (avg / r) | **[25.0]** (all `25/1`) |
| Unique resolutions | {(1280, 720): 18, (1920, 1080): 190} |
| Codec distribution | {'h264': 208} |
| Container (extension) | mp4 × 208 |
| ffprobe `format_name` family | `mov,mp4,...` (ISO BMFF) for all |
| Frame-timing class | {'CFR': 208} |
| Duration (s) min / median / mean / max | 3.000 / 7.000 / 6.889 / 17.000 |
| Frame count min / median / max | 75 / 175 / 425 |
| Bitrate min / median / max | 0.969 Mbps / 3.004 Mbps / 6.465 Mbps |
| Corrupted / unreadable | **0** |
| Duplicate basenames | **0** |
| Duplicate content hashes (head+tail SHA-256) | **0** |

### Duration distribution (integer seconds)

| Duration (s) | Count |
|-------------:|------:|
| 3 | 1 |
| 4 | 21 |
| 5 | 38 |
| 6 | 35 |
| 7 | 37 |
| 8 | 37 |
| 9 | 21 |
| 10 | 6 |
| 11 | 9 |
| 12 | 1 |
| 14 | 1 |
| 17 | 1 |

### Resolution distribution

| Resolution | Count | Share |
|------------|------:|------:|
| 1920×1080 | 190 | 91.3% |
| 1280×720 | 18 | 8.7% |

---

## 2. Per-video table

FPS columns are exact rational rates from the container (`r_frame_rate` / `avg_frame_rate`).
CFR/VFR is from frame presentation timestamps.

| # | Relpath | Container | Codec | FPS | Mode | W | H | Duration (s) | Frames | Bitrate |
|--:|---------|-----------|-------|-----|------|--:|--:|-------------:|-------:|---------|
| 1 | `abokhala/snatch_-94kg_abokhala_karim_i1_ok_000002.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 5.000 | 125 | 0.969 Mbps |
| 2 | `abokhala/snatch_-94kg_abokhala_karim_i2_fail_000004.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 5.000 | 125 | 1.193 Mbps |
| 3 | `abokhala/snatch_-94kg_abokhala_karim_i3_fail_000005.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 4.000 | 100 | 1.124 Mbps |
| 4 | `adventino/snatch_-65kg_adventino_geovani_leonardo_i1_ok_000085.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.479 Mbps |
| 5 | `adventino/snatch_-65kg_adventino_geovani_leonardo_i2_fail_000097.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.725 Mbps |
| 6 | `adventino/snatch_-65kg_adventino_geovani_leonardo_i3_fail_000099.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.322 Mbps |
| 7 | `alipour/snatch_-94kg_alipour_ali_i1_fail_000006.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 5.000 | 125 | 0.975 Mbps |
| 8 | `alipour/snatch_-94kg_alipour_ali_i2_ok_000009.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 7.000 | 175 | 1.359 Mbps |
| 9 | `alipour/snatch_-94kg_alipour_ali_i3_ok_000013.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 8.000 | 200 | 1.337 Mbps |
| 10 | `bardalez/snatch_-65kg_bardalez_tuisima_luis_david_i1_ok_000078.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.100 Mbps |
| 11 | `bardalez/snatch_-65kg_bardalez_tuisima_luis_david_i2_ok_000084.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.300 Mbps |
| 12 | `bardalez/snatch_-65kg_bardalez_tuisima_luis_david_i3_ok_000089.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 10.000 | 250 | 2.444 Mbps |
| 13 | `cambei/snatch_-53kg_cambei_mihaela_valentina_i1_ok_000118.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.725 Mbps |
| 14 | `cambei/snatch_-53kg_cambei_mihaela_valentina_i2_fail_000125.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 2.749 Mbps |
| 15 | `cambei/snatch_-53kg_cambei_mihaela_valentina_i3_ok_000129.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 4.659 Mbps |
| 16 | `campbell/snatch_-+86kg_campbell_emily_jade_i1_ok_000168.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 3.312 Mbps |
| 17 | `campbell/snatch_-+86kg_campbell_emily_jade_i2_fail_000173.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.367 Mbps |
| 18 | `campbell/snatch_-+86kg_campbell_emily_jade_i3_fail_000176.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.068 Mbps |
| 19 | `chen/snatch_-53kg_chen_guan_ling_i1_fail_000115.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.872 Mbps |
| 20 | `chen/snatch_-53kg_chen_guan_ling_i2_fail_000119.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 3.000 | 75 | 2.605 Mbps |
| 21 | `chen/snatch_-53kg_chen_guan_ling_i3_ok_000121.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.821 Mbps |
| 22 | `cheng/snatch_-48kg_lin_cheng_jing_i1_fail_000132.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 4.385 Mbps |
| 23 | `cheng/snatch_-48kg_lin_cheng_jing_i2_fail_000134.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 4.657 Mbps |
| 24 | `cheng/snatch_-48kg_lin_cheng_jing_i3_ok_000135.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 5.176 Mbps |
| 25 | `cikamatana/snatch_-86kg_cikamatana_eileen_f_i1_fail_000193.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.216 Mbps |
| 26 | `cikamatana/snatch_-86kg_cikamatana_eileen_f_i2_ok_000194.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.463 Mbps |
| 27 | `cikamatana/snatch_-86kg_cikamatana_eileen_f_i3_fail_000199.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.942 Mbps |
| 28 | `daehee/snatch_-88kg_jo_daehee_i1_ok_000030.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.278 Mbps |
| 29 | `daehee/snatch_-88kg_jo_daehee_i2_fail_000041.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.322 Mbps |
| 30 | `daehee/snatch_-88kg_jo_daehee_i3_fail_000045.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.201 Mbps |
| 31 | `du/snatch_-53kg_du_meiyuan_i1_ok_000117.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.266 Mbps |
| 32 | `du/snatch_-53kg_du_meiyuan_i2_fail_000123.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.609 Mbps |
| 33 | `du/snatch_-53kg_du_meiyuan_i3_fail_000128.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 2.575 Mbps |
| 34 | `fang/snatch_-48kg_fang_wan_ling_i1_ok_000131.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 6.465 Mbps |
| 35 | `fang/snatch_-48kg_fang_wan_ling_i2_ok_000133.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 5.687 Mbps |
| 36 | `fang/snatch_-48kg_fang_wan_ling_i3_ok_000144.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.968 Mbps |
| 37 | `ficco/snatch_-88k_ficco_cristiano_giuseppe_i3_fail_000040.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.796 Mbps |
| 38 | `ficco/snatch_-88kg_ficco_cristiano_giuseppe_i1_ok_000021.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 2.426 Mbps |
| 39 | `ficco/snatch_-88kg_ficco_cristiano_giuseppe_i2_ok_000029.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 2.200 Mbps |
| 40 | `friedrich/snatch_-94kg_friedich_raphael_i1_ok_000001.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 6.000 | 150 | 2.024 Mbps |
| 41 | `friedrich/snatch_-94kg_friedich_raphael_i2_ok_000003.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 6.000 | 150 | 1.097 Mbps |
| 42 | `friedrich/snatch_-94kg_friedich_raphael_i3_ok_000007.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 8.000 | 200 | 1.089 Mbps |
| 43 | `genc/snatch_-71kg_genc_ysuf_fehmi_i3_ok_000069.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.019 Mbps |
| 44 | `genc/snatch_-71kg_genc_yusuf_fehmi_i1_fail_000065.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.844 Mbps |
| 45 | `genc/snatch_-71kg_genc_yusuf_fehmi_i2_fail_000067.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 2.963 Mbps |
| 46 | `grigoryan/snatch_-88kg_grigoryan_suren_i1_fail_000031.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.723 Mbps |
| 47 | `grigoryan/snatch_-88kg_grigoryan_suren_i2_fail_000033.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.835 Mbps |
| 48 | `grigoryan/snatch_-88kg_grigoryan_suren_i3_ok_000034.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.967 Mbps |
| 49 | `hardal/snatch_-65kg_hardal_ferdi_i1_ok_000090.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.118 Mbps |
| 50 | `hardal/snatch_-65kg_hardal_ferdi_i2_fail_000098.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.584 Mbps |
| 51 | `hardal/snatch_-65kg_hardal_ferdi_i3_fail_000100.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 10.000 | 250 | 2.158 Mbps |
| 52 | `he/snatch_-71kg_he_yueji_i1_ok_000073.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 12.000 | 300 | 3.045 Mbps |
| 53 | `he/snatch_-71kg_he_yueji_i2_ok_000077.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.102 Mbps |
| 54 | `he/snatch_-71kg_he_yueji_i3_ok_000078.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.480 Mbps |
| 55 | `higa/snatch_-53kg_higa_sei_i1_fail_000112.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 5.159 Mbps |
| 56 | `higa/snatch_-53kg_higa_sei_i2_fail_000113.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.529 Mbps |
| 57 | `higa/snatch_-53kg_higa_sei_i3_fail_000114.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.222 Mbps |
| 58 | `hyeongo/snatch_-88kg_park_hyeongo_i1_fail_000022.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.050 Mbps |
| 59 | `hyeongo/snatch_-88kg_park_hyeongo_i2_fail_000024.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.288 Mbps |
| 60 | `hyeongo/snatch_-88kg_park_hyeongo_i3_fail_000025.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.173 Mbps |
| 61 | `irawan/snatch_-65kg_irawan_eko_yuli_i1_fail_000091.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.946 Mbps |
| 62 | `irawan/snatch_-65kg_irawan_eko_yuli_i2_fail_000095.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.104 Mbps |
| 63 | `irawan/snatch_-65kg_irawan_eko_yuli_i3_ok_000096.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.982 Mbps |
| 64 | `kahriman/snatch_-71k_kahriman_kaan_i1_ok_000059.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.823 Mbps |
| 65 | `kahriman/snatch_-71kg_kahriman_kaan_i2_fail_000066.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.432 Mbps |
| 66 | `kahriman/snatch_-71kg_kahriman_kaan_i3_fail_000068.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.004 Mbps |
| 67 | `kang/snatch_-53kg_kang_hyon_gyong_i1_fail_000124.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.091 Mbps |
| 68 | `kang/snatch_-53kg_kang_hyon_gyong_i2_ok_000126.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 3.064 Mbps |
| 69 | `kang/snatch_-53kg_kang_hyon_gyong_i3_fail_000130.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.248 Mbps |
| 70 | `karapetyan/snatch_-88k_karapetyan_andranik_i1_fail_000042.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.620 Mbps |
| 71 | `karapetyan/snatch_-88k_karapetyan_andranik_i2_fail_000044.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.990 Mbps |
| 72 | `karapetyan/snatch_-88k_karapetyan_andranik_i3_fail_000049.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.159 Mbps |
| 73 | `khambao/snatch_-53kg_khambao_surodchana_i1_ok_000111.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 3.654 Mbps |
| 74 | `khambao/snatch_-53kg_khambao_surodchana_i2_fail_000119.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 2.254 Mbps |
| 75 | `khambao/snatch_-53kg_khambao_surodchana_i3_ok_000120.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 10.000 | 250 | 2.469 Mbps |
| 76 | `koanda/snatch_-86kg_koanda_solfrid_eila_amena_i1_ok_000200.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.339 Mbps |
| 77 | `koanda/snatch_-86kg_koanda_solfrid_eila_amena_i2_ok_000203.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 10.000 | 250 | 2.672 Mbps |
| 78 | `koanda/snatch_-86kg_koanda_solfrid_eila_amena_i3_fail_000205.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.566 Mbps |
| 79 | `kwang/snatch_-88k_ro_kwang_ryol_i1_ok_000036.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.856 Mbps |
| 80 | `kwang/snatch_-88k_ro_kwang_ryol_i2_fail_000043.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.957 Mbps |
| 81 | `kwang/snatch_-88k_ro_kwang_ryol_i3_fail_000046.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.600 Mbps |
| 82 | `li/snatch_-48kg_li_shumiao_i1_fail_000142.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 4.499 Mbps |
| 83 | `li/snatch_-48kg_li_shumiao_i2_ok_000143.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 4.862 Mbps |
| 84 | `li/snatch_-48kg_li_shumiao_i3_fail_000151.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 4.636 Mbps |
| 85 | `lo/snatch_-86kg_lo_ying_yuan_i1_ok_000189.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.019 Mbps |
| 86 | `lo/snatch_-86kg_lo_ying_yuan_i2_fail_000195.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.108 Mbps |
| 87 | `lo/snatch_-86kg_lo_ying_yuan_i3_fail_000197.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.100 Mbps |
| 88 | `lopez/snatch_-88k_lopez_lopez_yeison_i1_ok_000048.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.901 Mbps |
| 89 | `lopez/snatch_-88k_lopez_lopez_yeison_i2_ok_000052.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.862 Mbps |
| 90 | `lopez/snatch_-88k_lopez_lopez_yeison_i3_fail_000053.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.612 Mbps |
| 91 | `marin/snatch_-88k_robu_marin_i1_ok_000047.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.180 Mbps |
| 92 | `marin/snatch_-88k_robu_marin_i2_fail_000050.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.282 Mbps |
| 93 | `marin/snatch_-88k_robu_marin_i3_fail_000051.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.457 Mbps |
| 94 | `mego/snatch_-53kg_mego_contreras_shoely_mabel_i1_ok_000108.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 5.133 Mbps |
| 95 | `mego/snatch_-53kg_mego_contreras_shoely_mabel_i2_fail_000109.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 5.031 Mbps |
| 96 | `mego/snatch_-53kg_mego_contreras_shoely_mabel_i3_ok_000110.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 4.864 Mbps |
| 97 | `mirabai/snatch_-48kg_mirabai_chanu_saikhom_i1_ok_000153.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 4.751 Mbps |
| 98 | `mirabai/snatch_-48kg_mirabai_chanu_saikhom_i2_fail_000156.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 4.096 Mbps |
| 99 | `mirabai/snatch_-48kg_mirabai_chanu_saikhom_i3_fail_000157.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.919 Mbps |
| 100 | `miyamoto/snatch_-71k_miyamoto_masanori_i1_ok_000058.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.544 Mbps |
| 101 | `miyamoto/snatch_-71kg_miyamoto_masanori_i2_ok_000070.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 2.898 Mbps |
| 102 | `miyamoto/snatch_-71kg_miyamoto_masanori_i3_fail_000075.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.385 Mbps |
| 103 | `moeini/snatch_-94kg_moeini_sedeh_alireza_i1_ok_000012.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 8.000 | 200 | 1.184 Mbps |
| 104 | `moeini/snatch_-94kg_moeini_sedeh_alireza_i2_ok_000016.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 8.000 | 200 | 1.277 Mbps |
| 105 | `moeini/snatch_-94kg_moeini_sedeh_alireza_i3_ok_000018.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 9.000 | 225 | 1.356 Mbps |
| 106 | `montero/snatch_-48kg_montero_ramos_ludia_m_i1_ok_000140.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 4.111 Mbps |
| 107 | `montero/snatch_-48kg_montero_ramos_ludia_m_i2_ok_000149.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 4.519 Mbps |
| 108 | `montero/snatch_-48kg_montero_ramos_ludia_m_i3_fail_000154.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 4.409 Mbps |
| 109 | `morris/snatch_-65kg_morris_hampton_miller_i1_fail_000083.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.448 Mbps |
| 110 | `morris/snatch_-65kg_morris_hampton_miller_i2_ok_000086.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.430 Mbps |
| 111 | `morris/snatch_-65kg_morris_hampton_miller_i3_fail_000102.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.719 Mbps |
| 112 | `mosquera/snatch_-65kg_mosquera_valencia_f_i1_ok_000079.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.561 Mbps |
| 113 | `mosquera/snatch_-65kg_mosquera_valencia_f_i2_fail_000087.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.252 Mbps |
| 114 | `mosquera/snatch_-65kg_mosquera_valencia_f_i3_fail_000094.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.295 Mbps |
| 115 | `mueller/snatch_-88kg_mueller_lucas_i1_ok_000019.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 17.000 | 425 | 3.612 Mbps |
| 116 | `mueller/snatch_-88kg_mueller_lucas_i2_ok_000026.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.095 Mbps |
| 117 | `mueller/snatch_-88kg_mueller_lucas_i3_fail_000027.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.712 Mbps |
| 118 | `muhamad/snatch_-65kg_muhamad_aznil_bin_bidin_i1_ok_000080.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.923 Mbps |
| 119 | `muhamad/snatch_-65kg_muhamad_aznil_bin_bidin_i2_ok_000093.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.758 Mbps |
| 120 | `muhamad/snatch_-65kg_muhamad_aznil_bin_bidin_i3_fail_000103.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 2.747 Mbps |
| 121 | `muthupandi/snatch_-65kg_muthupandi_raja_i1_fail_000081.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.224 Mbps |
| 122 | `muthupandi/snatch_-65kg_muthupandi_raja_i2_ok_000082.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.859 Mbps |
| 123 | `muthupandi/snatch_-65kg_muthupandi_raja_i3_fail_000088.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.342 Mbps |
| 124 | `nagashima/snatch_-86kg_nagashima_wakana_i1_ok_000182 .mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.160 Mbps |
| 125 | `nagashima/snatch_-86kg_nagashima_wakana_i2_ok_000186.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 3.429 Mbps |
| 126 | `nagashima/snatch_-86kg_nagashima_wakana_i3_ok_000187.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.250 Mbps |
| 127 | `nakajima/snatch_-86kg_nakajima_motoka_i1_fail_000183 .mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.460 Mbps |
| 128 | `nakajima/snatch_-86kg_nakajima_motoka_i2_fail_000184 .mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.891 Mbps |
| 129 | `nakajima/snatch_-86kg_nakajima_motoka_i3_ok_000185.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.090 Mbps |
| 130 | `nasar/snatch_-94kg_nasar_karlos_i1_ok_000011.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 7.000 | 175 | 1.473 Mbps |
| 131 | `nasar/snatch_-94kg_nasar_karlos_i2_fail_000015.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 6.000 | 150 | 0.978 Mbps |
| 132 | `nasar/snatch_-94kg_nasar_karlos_i3_fail_000017.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 4.000 | 100 | 1.149 Mbps |
| 133 | `ngake/snatch_-86kg_ngake_madias_dodo_nzesso_i1_fail_000191.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.432 Mbps |
| 134 | `ngake/snatch_-86kg_ngake_madias_dodo_nzesso_i2_ok_000192.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.131 Mbps |
| 135 | `ngake/snatch_-86kg_ngake_madias_dodo_nzesso_i3_fail_000201.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 2.423 Mbps |
| 136 | `olivares/snatch_-71kg_olivares_paez_sebastian_a_i1_fail_000063.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.893 Mbps |
| 137 | `ortiz/snatch_-48kg_ortiz_dahiana_i1_fail_000136.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.939 Mbps |
| 138 | `ortiz/snatch_-48kg_ortiz_dahiana_i2_fail_000137.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.338 Mbps |
| 139 | `ortiz/snatch_-48kg_ortiz_dahiana_i3_fail_000138.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.515 Mbps |
| 140 | `ozbek/snatch_-65kg_ozbek_muhammed_furkan_i1_ok_000105.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 10.000 | 250 | 3.156 Mbps |
| 141 | `ozbek/snatch_-65kg_ozbek_muhammed_furkan_i2_ok_000106.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.074 Mbps |
| 142 | `ozbek/snatch_-65kg_ozbek_muhammed_furkan_i3_ok_000107.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.078 Mbps |
| 143 | `ozkan/snatch_-53kg_ozkan_cansel_i1_ok_000116.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.411 Mbps |
| 144 | `ozkan/snatch_-53kg_ozkan_cansel_i2_fail_000122.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.719 Mbps |
| 145 | `ozkan/snatch_-53kg_ozkan_cansel_i3_ok_000127.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.527 Mbps |
| 146 | `pak/snatch_-65kg_pak_myong_jin_i1_ok_000092.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 2.643 Mbps |
| 147 | `pak/snatch_-65kg_pak_myong_jin_i2_fail_000101.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.472 Mbps |
| 148 | `pak/snatch_-65kg_pak_myong_jin_i3_fail_000104.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.562 Mbps |
| 149 | `park/snatch_-+86kg_park_hyejeong_i1_ok_000178.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.524 Mbps |
| 150 | `park/snatch_-+86kg_park_hyejeong_i2_ok_000180.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.005 Mbps |
| 151 | `park/snatch_-+86kg_park_hyejeong_i3_fail_000181.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.642 Mbps |
| 152 | `peguero/snatch_-86kg_mejia_peguero_yudelina_i1_ok_000198.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 4.098 Mbps |
| 153 | `peguero/snatch_-86kg_mejia_peguero_yudelina_i2_ok_000202.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 3.197 Mbps |
| 154 | `peguero/snatch_-86kg_mejia_peguero_yudelina_i3_ok_000204.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 3.317 Mbps |
| 155 | `ramos/snatch_-48kg_ramos_rosegie_i1_ok_000139.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 4.468 Mbps |
| 156 | `ramos/snatch_-48kg_ramos_rosegie_i2_fail_000148.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 4.869 Mbps |
| 157 | `ramos/snatch_-48kg_ramos_rosegie_i3_fail_000152.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 4.667 Mbps |
| 158 | `ri/snatch_-71k_ri_won_ju_i1_ok_000056.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.035 Mbps |
| 159 | `ri/snatch_-71kg_ri_won_ju_i2_ok_000061.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.432 Mbps |
| 160 | `ri/snatch_-71kg_ri_won_ju_i3_ok_000072.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.631 Mbps |
| 161 | `ri_song/snatch_-48kg_ri_song_gum_i1_ok_000159.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 3.157 Mbps |
| 162 | `ri_song/snatch_-48kg_ri_song_gum_i2_fail_000162.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 4.958 Mbps |
| 163 | `ri_song/snatch_-48kg_ri_song_gum_i3_ok_000163.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 5.155 Mbps |
| 164 | `rivas/snatch_-86kg_rivas_mosquera_valeria_i1_fail_000188.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 4.166 Mbps |
| 165 | `rivas/snatch_-86kg_rivas_mosquera_valeria_i2_ok_000190.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.957 Mbps |
| 166 | `rivas/snatch_-86kg_rivas_mosquera_valeria_i3_fail_000196.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.301 Mbps |
| 167 | `rostami/snatch_-94kg_rostami_kianoush_i1_fail_000008.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 6.000 | 150 | 1.097 Mbps |
| 168 | `rostami/snatch_-94kg_rostami_kianoush_i2_ok_000010.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 7.000 | 175 | 1.243 Mbps |
| 169 | `rostami/snatch_-94kg_rostami_kianoush_i3_fail_000014.mp4` | mp4 | h264 | 25/1 | CFR | 1280 | 720 | 6.000 | 150 | 1.309 Mbps |
| 170 | `rustamov/snatch_-71k_rustamov_isa_i1_ok_000055.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.005 Mbps |
| 171 | `rustamov/snatch_-71k_rustamov_isa_i2_fail_000057.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 2.689 Mbps |
| 172 | `rustamov/snatch_-71kg_rustamov_isa_i3_ok_000062.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 3.509 Mbps |
| 173 | `sahakyan/snatch_-71kg_sahakyan_gor_i1_ok_000064.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.619 Mbps |
| 174 | `sahakyan/snatch_-71kg_sahakyan_gor_i2_fail_000074.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.248 Mbps |
| 175 | `sahakyan/snatch_-71kg_sahakyan_gor_i3_ok_000077.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 3.424 Mbps |
| 176 | `salehi/snatch_-88kg_salehi_pour_iliya_i1_fail_000023.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 2.194 Mbps |
| 177 | `salehi/snatch_-88kg_salehi_pour_iliya_i2_ok_000054.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.947 Mbps |
| 178 | `salehi/snatch_-88kg_salehi_pour_iliya_i3_ok_000038.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.188 Mbps |
| 179 | `sarria/snatch_-+86kg_sarria_ruiz_marifelix_i1_ok_000167.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.447 Mbps |
| 180 | `sarria/snatch_-+86kg_sarria_ruiz_marifelix_i2_fail_000172.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.363 Mbps |
| 181 | `sarria/snatch_-+86kg_sarria_ruiz_marifelix_i3_ok_000175.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.748 Mbps |
| 182 | `sukcharoen/snatch_-48kg_sukcharoen_thanyathon_i1_ok_000158.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.445 Mbps |
| 183 | `sukcharoen/snatch_-48kg_sukcharoen_thanyathon_i2_fail_000160.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 4.946 Mbps |
| 184 | `sukcharoen/snatch_-48kg_sukcharoen_thanyathon_i3_fail_000161.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 4.595 Mbps |
| 185 | `suzuki/snatch_-48kg_suzuki_rira_i1_fail_000145.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 4.565 Mbps |
| 186 | `suzuki/snatch_-48kg_suzuki_rira_i2_fail_000146.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 4.754 Mbps |
| 187 | `suzuki/snatch_-48kg_suzuki_rira_i3_fail_000147.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 4.521 Mbps |
| 188 | `tarquini/snatch_-88k_tarquini_lorenzo_i3_fail_000039.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.799 Mbps |
| 189 | `tarquini/snatch_-88kg_tarquini_lorenzo_i1_ok_000020.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 14.000 | 350 | 2.967 Mbps |
| 190 | `tarquini/snatch_-88kg_tarquini_lorenzo_i2_ok_000028.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 3.297 Mbps |
| 191 | `theisen/snatch_-+86kg_theisen_lappen_mary_anne_i1_ok_000169.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 3.594 Mbps |
| 192 | `theisen/snatch_-+86kg_theisen_lappen_mary_anne_i2_fail_000174.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.662 Mbps |
| 193 | `theisen/snatch_-+86kg_theisen_lappen_mary_anne_i3_fail_000177.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 3.023 Mbps |
| 194 | `wang/snatch_-+86kg_wang_ling_chen_i1_ok_000164.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 3.846 Mbps |
| 195 | `wang/snatch_-+86kg_wang_ling_chen_i2_ok_000166.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 11.000 | 275 | 2.634 Mbps |
| 196 | `wang/snatch_-+86kg_wang_ling_chen_i3_fail_000170.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 2.100 Mbps |
| 197 | `wichuma/snatch_-71k_wichuma_weeraphon_i1_ok_000060.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 8.000 | 200 | 2.321 Mbps |
| 198 | `wichuma/snatch_-71kg_wichuma_weeraphon_i2_ok_000071.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 10.000 | 250 | 2.549 Mbps |
| 199 | `wichuma/snatch_-71kg_wichuma_weeraphon_i3_fail_000076.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.395 Mbps |
| 200 | `yunhua/snatch_-88k_pan_yunhua_i2_fail_000035.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 2.904 Mbps |
| 201 | `yunhua/snatch_-88k_pan_yunhua_i3_fail_000037.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 4.000 | 100 | 3.086 Mbps |
| 202 | `yunhua/snatch_-88kg_pan_yunhua_i1_fail_000032.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 2.687 Mbps |
| 203 | `zhu/snatch_-48kg_zhu_qiulian_i1_ok_000141.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 4.214 Mbps |
| 204 | `zhu/snatch_-48kg_zhu_qiulian_i2_ok_000150.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 4.558 Mbps |
| 205 | `zhu/snatch_-48kg_zhu_qiulian_i3_fail_000155.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 5.000 | 125 | 4.138 Mbps |
| 206 | `zhu_linhan/snatch_-+86kg_zhu_linhan_i1_ok_000165.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 9.000 | 225 | 3.392 Mbps |
| 207 | `zhu_linhan/snatch_-+86kg_zhu_linhan_i2_ok_000171.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 7.000 | 175 | 3.065 Mbps |
| 208 | `zhu_linhan/snatch_-+86kg_zhu_linhan_i3_fail_000179.mp4` | mp4 | h264 | 25/1 | CFR | 1920 | 1080 | 6.000 | 150 | 2.881 Mbps |

---

## 3. Anomaly detection

| Check | Result |
|-------|--------|
| Corrupted / ffprobe failures | **None** (208/208 readable) |
| Duplicated filenames | **None** |
| Duplicated content (quick hash) | **None** |
| Inconsistent FPS | **None** — all `25/1` avg and r |
| Inconsistent resolutions | **Two classes** — 190× 1920×1080 and 18× 1280×720 (not an error; document for pose pipelines) |
| VFR videos | **None** at frame level (all CFR @ 40 ms) |
| Missing bitrate | **None** |
| Missing frame counts | **None** (container `nb_frames` present; matches `round(duration×25)`) |
| Packet-PTS “VFR-looking” deltas | Present under H.264 B-frames; **not** true VFR (frame PTS are uniform) |

### Notes

- **Resolution mix:** 18 clips are 720p; the rest are 1080p. MediaPipe was run per-video; downstream tensors use normalized landmark coordinates, but any pixel-space analysis must account for the mix.
- **Duration:** short attempt clips (3–17 s); median 7 s.
- **Container label:** files are `.mp4`; ffprobe reports the MOV/MP4 brand family as `mov` first in `format_name`.

---

## 4. Common FPS conclusion

**Yes — all 208 videos share a common constant frame rate of exactly 25 fps (`25/1`), CFR.**

Conversion:

```
1 frame = 1000 / 25 = 40 ms
```

| Quantity | Value |
|----------|-------|
| Frame period | **40 ms** |
| Frames per second | **25** |
| Boundary MAE of 1 frame | **40 ms** |
| Boundary MAE of 2.49 frames (ASFormer catch→recovery mean) | **99.6 ms** |
| Boundary MAE of 4.52 frames (MS-TCN catch→recovery mean) | **180.8 ms** |

Millisecond boundary reporting in the manuscript can use this conversion **for this raw corpus**, provided analyses cite the audited 25 fps CFR assumption.

---

## Machine-readable extract

Full per-file JSON (including timing diagnostics): `docs/dataset/_video_metadata_raw.json`.

*End of video metadata audit.*
