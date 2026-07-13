"""Extended MS-TCN trainer tests."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.models.ms_tcn.model import MSTCNModel
from snatch_phase_bench.training.interfaces import TrainerConfig, TrainingRunContext
from snatch_phase_bench.training.lstm_trainer import set_seed
from snatch_phase_bench.training.ms_tcn_trainer import (
    CHECKPOINT_VERSION,
    FrameSequenceDataset,
    MSTCNTrainer,
    _collate_single,
    _compute_standardization,
    _macro_f1_supervised,
)


def test_collate_single_rejects_multi_item_batch() -> None:
    item = (torch.randn(5, 8), torch.randint(0, 4, (5,)), "video.mp4")
    with pytest.raises(ValueError, match="batch_size=1"):
        _collate_single([item, item])


def test_collate_single_shapes() -> None:
    features = torch.randn(12, 99)
    labels = torch.randint(1, 5, (12,))
    batch_features, batch_labels, mask, video_ids = _collate_single([(features, labels, "a/b.mp4")])
    assert batch_features.shape == (1, 12, 99)
    assert batch_labels.shape == (1, 12)
    assert mask.shape == (1, 12)
    assert video_ids == ["a/b.mp4"]


def test_compute_standardization_train_only_stats(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
) -> None:
    train, _ = synthetic_train_val_records
    mean, std = _compute_standardization(train)
    assert mean.shape == (99,)
    assert std.shape == (99,)
    assert np.all(std > 0)


def test_compute_standardization_empty_raises() -> None:
    with pytest.raises(ValueError, match="without training records"):
        _compute_standardization([])


def test_macro_f1_ignores_unlabeled() -> None:
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([0, 3, 1, 1, 2, 3])
    score = _macro_f1_supervised(y_true, y_pred, ignore_label_id=0)
    assert 0.0 <= score <= 1.0


def test_frame_sequence_dataset_applies_standardization(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
) -> None:
    train, _ = synthetic_train_val_records
    mean, std = _compute_standardization(train)
    dataset = FrameSequenceDataset(train[:1], mean, std)
    features, labels, video_id = dataset[0]
    assert features.shape[1] == 99
    assert labels.shape[0] == train[0].num_frames
    assert video_id == train[0].video_relpath


def test_trainer_fit_creates_all_artifacts(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
    tiny_ms_tcn_model: MSTCNModel,
    ms_tcn_trainer: MSTCNTrainer,
    tmp_path: Path,
) -> None:
    train, val = synthetic_train_val_records
    output_dir = tmp_path / "fit_artifacts"
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name="ms_tcn",
        config_path=tmp_path / "cfg.yaml",
        seed=1,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=output_dir,
    )
    config = TrainerConfig(epochs=2, early_stopping_patience=10)
    ms_tcn_trainer.fit(train, val, model=tiny_ms_tcn_model, config=config, context=context)
    for name in ("best_model.pt", "checkpoint_last.pt", "history.json", "feature_mean.npy", "feature_std.npy"):
        assert (output_dir / name).exists()


def test_trainer_resume_continues_from_checkpoint(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
    tiny_ms_tcn_model: MSTCNModel,
    ms_tcn_trainer: MSTCNTrainer,
    tmp_path: Path,
) -> None:
    train, val = synthetic_train_val_records
    output_dir = tmp_path / "resume"
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name="ms_tcn",
        config_path=tmp_path / "cfg.yaml",
        seed=2,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=output_dir,
    )
    config_first = TrainerConfig(epochs=2, early_stopping_patience=10)
    ms_tcn_trainer.fit(train, val, model=tiny_ms_tcn_model, config=config_first, context=context)

    model2 = MSTCNModel(
        input_size=99, num_classes=8, num_stages=2, num_layers=4, num_f_maps=32, dropout=0.0
    )
    config_resume = TrainerConfig(epochs=4, early_stopping_patience=10)
    ms_tcn_trainer.fit(train, val, model=model2, config=config_resume, context=context)
    payload = torch.load(output_dir / "checkpoint_last.pt", map_location="cpu", weights_only=False)
    assert payload["checkpoint_version"] == CHECKPOINT_VERSION
    assert payload["epoch"] == 4


def test_trainer_early_stopping(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
    tmp_path: Path,
) -> None:
    train, val = synthetic_train_val_records
    model = MSTCNModel(input_size=99, num_classes=8, num_stages=1, num_layers=2, num_f_maps=8, dropout=0.0)
    trainer = MSTCNTrainer(num_classes=8)
    output_dir = tmp_path / "early_stop"
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name="ms_tcn",
        config_path=tmp_path / "cfg.yaml",
        seed=3,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=output_dir,
    )
    config = TrainerConfig(epochs=50, early_stopping_patience=1, learning_rate=1e-4)
    trainer.fit(train, val, model=model, config=config, context=context)
    history = json.loads((output_dir / "history.json").read_text(encoding="utf-8"))
    assert len(history) < 50


def test_trainer_predict_video_single(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
    trained_ms_tcn_checkpoint: Path,
    ms_tcn_trainer: MSTCNTrainer,
) -> None:
    train, _ = synthetic_train_val_records
    mean, std = MSTCNTrainer.load_standardization(trained_ms_tcn_checkpoint)
    model = MSTCNModel(input_size=99, num_classes=8, num_stages=2, num_layers=4, num_f_maps=32, dropout=0.0)
    ms_tcn_trainer.load_checkpoint(trained_ms_tcn_checkpoint / "best_model.pt", model=model)
    pred = ms_tcn_trainer.predict_video(
        train[0].features,
        model=model,
        device=torch.device("cpu"),
        mean=mean,
        std=std,
    )
    assert pred.shape == (train[0].num_frames,)
    assert pred.dtype == np.int64


def test_trainer_save_load_roundtrip(
    tiny_ms_tcn_model: MSTCNModel,
    ms_tcn_trainer: MSTCNTrainer,
    tmp_path: Path,
) -> None:
    path = tmp_path / "roundtrip.pt"
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name="ms_tcn",
        config_path=tmp_path / "cfg.yaml",
        seed=4,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=tmp_path,
    )
    ms_tcn_trainer.save_checkpoint(tiny_ms_tcn_model, path, context=context, metrics={"epoch": 1})
    model2 = MSTCNModel(input_size=99, num_classes=8, num_stages=2, num_layers=4, num_f_maps=32, dropout=0.0)
    ms_tcn_trainer.load_checkpoint(path, model=model2)
    x = torch.randn(1, 8, 99)
    tiny_ms_tcn_model.eval()
    model2.eval()
    with torch.no_grad():
        assert torch.equal(tiny_ms_tcn_model.predict_classes(x), model2.predict_classes(x))


def test_trainer_requires_mstcn_model(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
    ms_tcn_trainer: MSTCNTrainer,
    tmp_path: Path,
) -> None:
    from snatch_phase_bench.models.lstm_baseline import LSTMBaselineModel

    train, val = synthetic_train_val_records
    lstm = LSTMBaselineModel(input_size=99, num_classes=7)
    context = TrainingRunContext(
        model_id="lstm",
        registry_name="lstm_baseline",
        config_path=tmp_path / "cfg.yaml",
        seed=5,
        split_version="synthetic",
        dataset_version="synthetic",
        output_dir=tmp_path,
    )
    with pytest.raises(TypeError, match="MSTCNModel"):
        ms_tcn_trainer.fit(train, val, model=lstm, config=TrainerConfig(epochs=1), context=context)


def test_training_is_deterministic_with_seed(
    synthetic_train_val_records: tuple[list[FrameSequenceRecord], list[FrameSequenceRecord]],
    tmp_path: Path,
) -> None:
    train, val = synthetic_train_val_records

    def _run(seed: int) -> np.ndarray:
        set_seed(seed)
        model = MSTCNModel(input_size=99, num_classes=8, num_stages=1, num_layers=2, num_f_maps=8, dropout=0.0)
        trainer = MSTCNTrainer(num_classes=8)
        out = tmp_path / f"seed_{seed}"
        context = TrainingRunContext(
            model_id="ms_tcn",
            registry_name="ms_tcn",
            config_path=tmp_path / "cfg.yaml",
            seed=seed,
            split_version="synthetic",
            dataset_version="synthetic",
            output_dir=out,
        )
        trainer.fit(train, val, model=model, config=TrainerConfig(epochs=1), context=context)
        mean, std = MSTCNTrainer.load_standardization(out)
        return trainer.predict_video(train[0].features, model=model, device=torch.device("cpu"), mean=mean, std=std)

    pred_a = _run(123)
    pred_b = _run(123)
    assert np.array_equal(pred_a, pred_b)
