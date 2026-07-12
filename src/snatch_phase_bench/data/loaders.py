"""Load processed datasets without modifying preprocessing logic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from snatch_phase_bench.evaluation.checkpoint_eval import is_lfs_pointer


@dataclass(frozen=True)
class ProcessedDataset:
    """Window-level processed tensors and metadata."""

    X: np.ndarray
    y: np.ndarray
    meta: pd.DataFrame
    label_map: pd.DataFrame
    data_dir: Path

    @property
    def num_samples(self) -> int:
        return int(len(self.X))

    @property
    def shape(self) -> tuple[int, ...]:
        return tuple(self.X.shape)


def load_processed_dataset(data_dir: Path) -> ProcessedDataset:
    """
    Load ``X.npy``, ``y.npy``, ``meta.csv``, ``label_map.csv`` from ``data_dir``.

    Raises ``FileNotFoundError`` if tensors are Git LFS pointer stubs.
    """
    data_dir = data_dir.resolve()
    X_path = data_dir / "X.npy"
    y_path = data_dir / "y.npy"
    meta_path = data_dir / "meta.csv"
    label_map_path = data_dir / "label_map.csv"

    for path in (X_path, y_path, meta_path, label_map_path):
        if not path.exists():
            raise FileNotFoundError(f"Missing processed artifact: {path}")
    if is_lfs_pointer(X_path):
        raise FileNotFoundError(f"X.npy is a Git LFS pointer, not a real tensor: {X_path}")
    if is_lfs_pointer(y_path):
        raise FileNotFoundError(f"y.npy is a Git LFS pointer, not a real tensor: {y_path}")

    X = np.load(X_path)
    y = np.load(y_path)
    meta = pd.read_csv(meta_path)
    label_map = pd.read_csv(label_map_path)

    if not (len(X) == len(y) == len(meta)):
        raise ValueError(
            f"Sample count mismatch: X={len(X)}, y={len(y)}, meta={len(meta)} in {data_dir}"
        )
    if not np.array_equal(y, meta["phase_id"].to_numpy(dtype=np.int64)):
        raise ValueError(f"y.npy phase_id values do not match meta.csv in {data_dir}")

    return ProcessedDataset(X=X, y=y, meta=meta, label_map=label_map, data_dir=data_dir)
