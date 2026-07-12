# Temporal Autocorrelation Analysis

## Window overlap
- Window size: 31
- Stride: 1
- Shared frames between consecutive windows: 30
- Overlap fraction: 0.9677 (96.77%)

## Dataset coverage
- Total windows: 21249
- Total videos: 208
- Windows per video (mean): 102.16
- Windows per video (median): 106.0

## Approximate independent temporal samples
- Non-overlapping window stride used: 31
- Approximate independent samples: 581
- Ratio reported windows / approximate independent: 36.57

## Notes
- Adjacent windows share shared_frames_per_adjacent_window of window_size frames.
- Approximate independent samples uses non-overlapping windows of size window_size per video.
- This quantifies temporal autocorrelation; it is not equivalent to cross-split leakage.
