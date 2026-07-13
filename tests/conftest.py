"""Shared pytest fixtures for SnatchPhaseBench tests."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import torch

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord, load_frame_sequences
from snatch_phase_bench.data.splits import AthleteSplit
from snatch_phase_bench.models.ms_tcn.model import MSTCNModel
from snatch_phase_bench.training.interfaces import TrainerConfig, TrainingRunContext
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer


def _write_synthetic_video(
    keypoints_root: Path,
    athlete: str,
    clip_name: str,
    phase_pattern: list[int],
    phase_names: list[str],
    athlete_idx: int,
) -> str:
    video = f"{athlete}/{clip_name}.mp4"
    csv_dir = keypoints_root / athlete
    csv_dir.mkdir(parents=True, exist_ok=True)
    rows: dict[str, list[float] | list[int]] = {"frame": list(range(len(phase_pattern)))}
    for landmark in range(33):
        base = 0.1 * (athlete_idx + 1) + 0.01 * landmark
        rows[f"x{landmark}"] = [base + 0.01 * frame for frame in range(len(phase_pattern))]
        rows[f"y{landmark}"] = [base + 0.02 * frame for frame in range(len(phase_pattern))]
        rows[f"z{landmark}"] = [base + 0.03 * frame for frame in range(len(phase_pattern))]
    pd.DataFrame(rows).to_csv(csv_dir / f"{clip_name}.csv", index=False)
    return video


@pytest.fixture
def synthetic_ms_tcn_dataset(tmp_path: Path) -> tuple[Path, Path, AthleteSplit]:
    """Minimal two-athlete dataset for MS-TCN CI tests."""
    labels_rows: list[dict[str, object]] = []
    keypoints_root = tmp_path / "keypoints"
    phase_pattern = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    phase_names = [
        "setup",
        "setup",
        "first_pull",
        "first_pull",
        "transition",
        "transition",
        "second_pull",
        "second_pull",
        "turnover",
        "turnover",
    ]

    for athlete_idx, athlete in enumerate(["athlete_a", "athlete_b"]):
        for clip_idx in range(2):
            video = _write_synthetic_video(
                keypoints_root,
                athlete,
                f"clip{clip_idx}",
                phase_pattern,
                phase_names,
                athlete_idx,
            )
            for frame, (phase_id, phase_name) in enumerate(zip(phase_pattern, phase_names, strict=True)):
                labels_rows.append(
                    {
                        "video_relpath": video,
                        "frame": frame,
                        "phase_id": phase_id,
                        "phase_name": phase_name,
                    }
                )

    labels_csv = tmp_path / "labels.csv"
    pd.DataFrame(labels_rows).to_csv(labels_csv, index=False)
    split = AthleteSplit(
        train_athletes=frozenset(["athlete_a"]),
        val_athletes=frozenset(["athlete_b"]),
        test_athletes=frozenset(),
    )
    return labels_csv, keypoints_root, split


@pytest.fixture
def synthetic_train_val_records(
    synthetic_ms_tcn_dataset: tuple[Path, Path, AthleteSplit],
) -> tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]]:
    labels_csv, keypoints_dir, split = synthetic_ms_tcn_dataset
    train = load_frame_sequences(
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
        athlete_split=split,
        split_filter="train",
    )
    val = load_frame_sequences(
        labels_csv=labels_csv,
        keypoints_dir=keypoints_dir,
        athlete_split=split,
        split_filter="val",
    )
    return train, val


@pytest.fixture
def tiny_ms_tcn_model() -> MSTCNModel:
    return MSTCNModel(
        input_size=99,
        num_classes=8,
        num_stages=2,
        num_layers=4,
        num_f_maps=32,
        kernel_size=3,
        dropout=0.0,
    )


@pytest.fixture
def ms_tcn_trainer() -> MSTCNTrainer:
    return MSTCNTrainer(num_classes=8, tmse_weight=0.15, tmse_truncate_tau=4.0)


@pytest.fixture
def trained_ms_tcn_checkpoint(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
    tiny_ms_tcn_model: MSTCNModel,
    ms_tcn_trainer: MSTCNTrainer,
    tmp_path: Path,
) -> Path:
    """Train a tiny MS-TCN for one epoch and return checkpoint directory."""
    train, val = synthetic_train_val_records
    output_dir = tmp_path / "ms_tcn_checkpoint"
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name="ms_tcn",
        config_path=tmp_path / "config.yaml",
        seed=42,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=output_dir,
    )
    config = TrainerConfig(batch_size=1, epochs=1, early_stopping_patience=5, learning_rate=1e-3)
    ms_tcn_trainer.fit(train, val, model=tiny_ms_tcn_model, config=config, context=context)
    return output_dir


def make_frame_record(
    *,
    video: str = "athlete_x/clip0.mp4",
    num_frames: int = 12,
    feature_dim: int = 99,
    label_cycle: list[int] | None = None,
) -> FrameSequenceRecord:
    label_cycle = label_cycle or [1, 2, 3, 4]
    frames = np.arange(num_frames, dtype=np.int64)
    features = np.random.RandomState(0).randn(num_frames, feature_dim).astype(np.float32)
    phase_ids = np.array([label_cycle[i % len(label_cycle)] for i in range(num_frames)], dtype=np.int64)
    return FrameSequenceRecord(
        video_relpath=video,
        athlete_id=video.split("/", 1)[0],
        frames=frames,
        features=features,
        phase_ids=phase_ids,
        split="train",
    )
