"""Per-video dense frame sequences for learned temporal segmenters (TAS)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Literal

import numpy as np
import pandas as pd

from snatch_phase_bench.data.dataset_builder import (
    get_athlete_from_relpath,
    get_feature_columns,
    get_keypoint_csv_path,
    load_and_prepare_pose_csv,
    normalize_relpath,
)
from snatch_phase_bench.data.labels import FrameLabelStore
from snatch_phase_bench.data.splits import AthleteSplit, SplitName

SplitFilter = Literal["train", "val", "test", "all"]


@dataclass(frozen=True)
class FrameSequenceRecord:
    """Aligned pose features and labels for one video."""

    video_relpath: str
    athlete_id: str
    frames: np.ndarray
    features: np.ndarray
    phase_ids: np.ndarray
    split: SplitName | None = None

    @property
    def num_frames(self) -> int:
        return int(len(self.frames))

    @property
    def feature_dim(self) -> int:
        return int(self.features.shape[1])


def _merge_pose_and_labels(
    video_relpath: str,
    pose_df: pd.DataFrame,
    feature_cols: list[str],
    label_store: FrameLabelStore,
) -> FrameSequenceRecord:
    labels = label_store.get(video_relpath)
    merged = pd.merge(
        pd.DataFrame(
            {
                "video_relpath": video_relpath,
                "frame": labels.frames,
                "phase_id": labels.phase_ids,
            }
        ),
        pose_df[["frame"] + feature_cols],
        on="frame",
        how="inner",
        validate="one_to_one",
    )
    if merged.empty:
        raise RuntimeError(f"No aligned labels/keypoints for {video_relpath}")

    merged = merged.sort_values("frame").reset_index(drop=True)
    athlete_id = get_athlete_from_relpath(video_relpath)
    return FrameSequenceRecord(
        video_relpath=video_relpath,
        athlete_id=athlete_id,
        frames=merged["frame"].to_numpy(dtype=np.int64),
        features=merged[feature_cols].to_numpy(dtype=np.float32),
        phase_ids=merged["phase_id"].to_numpy(dtype=np.int64),
    )


def build_frame_sequence(
    video_relpath: str,
    *,
    labels_csv: Path,
    keypoints_dir: Path,
    use_z: bool = True,
    use_visibility: bool = False,
    athlete_split: AthleteSplit | None = None,
) -> FrameSequenceRecord:
    """Build one dense frame sequence from keypoints and frame labels."""
    video_relpath = normalize_relpath(video_relpath)
    label_store = FrameLabelStore(labels_csv)
    pose_csv = get_keypoint_csv_path(keypoints_dir, video_relpath)
    if not pose_csv.exists():
        raise FileNotFoundError(f"Missing keypoints CSV: {pose_csv}")

    raw_pose = pd.read_csv(pose_csv, nrows=1)
    feature_cols = get_feature_columns(raw_pose, use_z=use_z, use_visibility=use_visibility)
    pose_df = load_and_prepare_pose_csv(pose_csv, feature_cols)
    record = _merge_pose_and_labels(video_relpath, pose_df, feature_cols, label_store)

    split: SplitName | None = None
    if athlete_split is not None:
        split = athlete_split.partition_for_athlete(record.athlete_id)
    return FrameSequenceRecord(
        video_relpath=record.video_relpath,
        athlete_id=record.athlete_id,
        frames=record.frames,
        features=record.features,
        phase_ids=record.phase_ids,
        split=split,
    )


def iter_frame_sequences(
    *,
    labels_csv: Path,
    keypoints_dir: Path,
    use_z: bool = True,
    use_visibility: bool = False,
    athlete_split: AthleteSplit | None = None,
    split_filter: SplitFilter = "all",
) -> Iterator[FrameSequenceRecord]:
    """Yield dense frame sequences for all labeled videos."""
    label_store = FrameLabelStore(labels_csv)
    for labels in label_store.iter_videos():
        video_relpath = labels.video_relpath
        if athlete_split is not None and split_filter != "all":
            athlete = get_athlete_from_relpath(video_relpath)
            if athlete_split.partition_for_athlete(athlete) != split_filter:
                continue
        yield build_frame_sequence(
            video_relpath,
            labels_csv=labels_csv,
            keypoints_dir=keypoints_dir,
            use_z=use_z,
            use_visibility=use_visibility,
            athlete_split=athlete_split,
        )


def load_frame_sequences(
    *,
    labels_csv: Path,
    keypoints_dir: Path,
    use_z: bool = True,
    use_visibility: bool = False,
    athlete_split: AthleteSplit | None = None,
    split_filter: SplitFilter = "all",
) -> list[FrameSequenceRecord]:
    """Materialize frame sequences into a list."""
    return list(
        iter_frame_sequences(
            labels_csv=labels_csv,
            keypoints_dir=keypoints_dir,
            use_z=use_z,
            use_visibility=use_visibility,
            athlete_split=athlete_split,
            split_filter=split_filter,
        )
    )


def summarize_frame_sequences(records: list[FrameSequenceRecord]) -> dict[str, Any]:
    """Return lightweight dataset statistics for logging."""
    if not records:
        return {"videos": 0, "frames": 0}
    return {
        "videos": len(records),
        "frames": int(sum(record.num_frames for record in records)),
        "feature_dim": records[0].feature_dim,
        "athletes": len({record.athlete_id for record in records}),
    }
