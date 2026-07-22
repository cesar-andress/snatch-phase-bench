# MS-TCN M3 aggregate test metrics

Seeds: 42, 123, 456
Early-stopping monitor: `val_segmental_f1_at_50`

| Metric | Mean | Std | Median | Min | Max |
|--------|------|-----|--------|-----|-----|
| frame_macro_f1 | 0.9048 | 0.0092 | 0.9093 | 0.8921 | 0.9131 |
| segmental_f1_at_50 | 0.7747 | 0.0177 | 0.7763 | 0.7523 | 0.7955 |
| edit_score | 0.8505 | 0.0644 | 0.8781 | 0.7615 | 0.9118 |
| boundary_mae_frames | 1.3221 | 0.3006 | 1.1303 | 1.0894 | 1.7465 |
| boundary_f1 | 0.9474 | 0.0086 | 0.9483 | 0.9364 | 0.9574 |
