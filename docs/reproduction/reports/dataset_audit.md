# Dataset Audit Report

## File counts
- Keypoint CSV files: 208
- Frame annotation rows: 35825
- Annotated videos: 208
- Segment label files: 208

## Processed dataset
- Meta rows: 21249
- Meta videos: 208
- Meta athletes: 70
- Window size: 31
- Stride: 1
- Rebuilt samples: None
- Rebuilt X shape: None

## meta.csv vs manifest
- Baseline meta bytes: 1756579
- Manifest expected bytes: 1777829
- Discrepancy: 21250
- Baseline SHA-256: 6b1fc02b4062be11781f675bf1c79cc5272198882cfe48b6784b35dbe1089278
- Manifest SHA-256: 4a3b566f47c8a19a64f5848b9a4190d91e1cf3ea850b72dabdb3712dcb351226

## Class distribution (processed meta)
- catch: 1912
- first_pull: 2434
- recovery: 7065
- second_pull: 1245
- setup: 6017
- transition: 673
- turnover: 1903

## Filenames with space before .csv
- `nagashima/snatch_-86kg_nagashima_wakana_i1_ok_000182 .csv`
- `nakajima/snatch_-86kg_nakajima_motoka_i1_fail_000183 .csv`
- `nakajima/snatch_-86kg_nakajima_motoka_i2_fail_000184 .csv`

## Warnings
- baseline meta.csv size differs from manifest by 21250 bytes
- baseline meta.csv SHA-256 differs from manifest entry
- 3 keypoint files contain a space before .csv; labels use matching spaced .mp4 paths — rebuild should still resolve them.
