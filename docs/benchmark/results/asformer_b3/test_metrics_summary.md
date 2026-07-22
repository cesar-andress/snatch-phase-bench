# ASFormer B3 aggregate test metrics

Seeds: 42, 123, 456
Early-stopping monitor: `val_segmental_f1_at_50`

| Metric | Mean | Std | Median | Min | Max |
|--------|------|-----|--------|-----|-----|
| frame_macro_f1 | 0.9019 | 0.0171 | 0.9016 | 0.8812 | 0.9230 |
| segmental_f1_at_50 | 0.7897 | 0.0011 | 0.7898 | 0.7882 | 0.7910 |
| edit_score | 0.8545 | 0.0475 | 0.8441 | 0.8022 | 0.9173 |
| boundary_mae_frames | 0.9773 | 0.0576 | 0.9611 | 0.9162 | 1.0545 |
| boundary_f1 | 0.9529 | 0.0073 | 0.9568 | 0.9427 | 0.9592 |
