"""ASFormer unit and smoke tests."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

from snatch_phase_bench.benchmark.registry import load_benchmark_registry, load_model_experiment_config
from snatch_phase_bench.data.frame_sequence import iter_frame_sequences
from snatch_phase_bench.models.asformer.core import ASFormerCore, AttLayer, exponential_decrease
from snatch_phase_bench.models.asformer.model import ASFormerModel
from snatch_phase_bench.models.ms_tcn.loss import compute_mstcn_loss
from snatch_phase_bench.models.registry import build_model, list_models
from snatch_phase_bench.ontology.loader import PROJECT_ROOT
from snatch_phase_bench.training.asformer_trainer import ASFormerTrainer
from snatch_phase_bench.training.interfaces import TrainerConfig, TrainingRunContext


def test_asformer_in_registry() -> None:
    assert "asformer" in list_models()
    model = build_model(
        "asformer",
        input_size=99,
        num_classes=8,
        num_decoders=2,
        num_layers=3,
        num_f_maps=16,
        channel_masking_rate=0.0,
    )
    assert isinstance(model, ASFormerModel)
    assert model.name == "asformer"


def test_exponential_decrease() -> None:
    assert exponential_decrease(0) == 1.0
    assert exponential_decrease(1) < 1.0


def test_window_mask_fix_indexing() -> None:
    layer = AttLayer(8, 8, 8, 2, 2, 2, bl=4, stage="encoder", att_type="sliding_att")
    mask = layer._construct_window_mask(torch.device("cpu"), torch.float32)
    assert mask.shape == (1, 4, 8)
    # Fixed indexing: row i has ones starting at column i.
    assert float(mask[0, 0, 0]) == 1.0
    assert float(mask[0, 0, 3]) == 1.0
    assert float(mask[0, 0, 4]) == 0.0
    assert float(mask[0, 1, 1]) == 1.0


def test_asformer_forward_shapes() -> None:
    model = ASFormerModel(
        input_size=99,
        num_classes=8,
        num_decoders=2,
        num_layers=3,
        num_f_maps=16,
        channel_masking_rate=0.0,
    )
    model.eval()
    x = torch.randn(1, 40, 99)
    out = model(x)
    assert out.logits.shape == (1, 40, 8)
    stages = model.forward_stages(x)
    assert stages.shape == (3, 1, 8, 40)  # encoder + 2 decoders


def test_asformer_batch_size_must_be_one_for_sliding() -> None:
    model = ASFormerModel(
        input_size=8,
        num_classes=4,
        num_decoders=1,
        num_layers=2,
        num_f_maps=8,
        channel_masking_rate=0.0,
    )
    x = torch.randn(2, 16, 8)
    try:
        model(x)
        raised = False
    except ValueError as exc:
        raised = True
        assert "batch_size=1" in str(exc)
    assert raised


def test_asformer_loss_backward() -> None:
    model = ASFormerModel(
        input_size=16,
        num_classes=5,
        num_decoders=1,
        num_layers=2,
        num_f_maps=8,
        channel_masking_rate=0.0,
    )
    x = torch.randn(1, 20, 16)
    y = torch.randint(1, 5, (1, 20))
    stages = model.forward_stages(x)
    ce = nn.CrossEntropyLoss(ignore_index=0)
    mask = torch.ones(1, 1, 20)
    loss, metrics = compute_mstcn_loss(
        stages,
        y,
        mask=mask,
        ce_loss=ce,
        tmse_weight=0.15,
        tmse_truncate_tau=4.0,
    )
    loss.backward()
    assert metrics["loss_total"] > 0


def test_asformer_config_defaults() -> None:
    config = load_model_experiment_config(PROJECT_ROOT / "configs/benchmark/asformer.yaml")
    assert config["experiment"]["tier"] == "B3"
    assert config["model"]["num_decoders"] == 3
    assert config["model"]["num_layers"] == 10
    assert config["loss"]["tmse_weight"] == 0.15
    assert config["optimizer"]["weight_decay"] == 0.00001
    assert config["training"]["early_stopping"]["monitor"] == "val_segmental_f1_at_50"


def test_asformer_manifest_tier() -> None:
    registry = load_benchmark_registry()
    spec = registry.get("asformer")
    assert spec.tier_id == "B3"
    assert spec.status == "verified"
    ms = registry.get("ms_tcn")
    assert ms.tier_id == "B2"
    assert ms.status == "verified"


def test_asformer_training_smoke(synthetic_ms_tcn_dataset, tmp_path: Path) -> None:
    labels_csv, keypoints_dir, split = synthetic_ms_tcn_dataset
    train = list(
        iter_frame_sequences(
            labels_csv=labels_csv,
            keypoints_dir=keypoints_dir,
            athlete_split=split,
            split_filter="train",
        )
    )
    val = list(
        iter_frame_sequences(
            labels_csv=labels_csv,
            keypoints_dir=keypoints_dir,
            athlete_split=split,
            split_filter="val",
        )
    )
    model = ASFormerModel(
        input_size=99,
        num_classes=8,
        num_decoders=1,
        num_layers=2,
        num_f_maps=16,
        channel_masking_rate=0.0,
    )
    trainer = ASFormerTrainer(num_classes=8, tmse_weight=0.15, tmse_truncate_tau=4.0)
    output_dir = tmp_path / "asformer_smoke"
    context = TrainingRunContext(
        model_id="asformer",
        registry_name="asformer",
        config_path=PROJECT_ROOT / "configs/benchmark/asformer.yaml",
        seed=42,
        split_version="test",
        dataset_version="test",
        output_dir=output_dir,
    )
    config = TrainerConfig(
        batch_size=1,
        epochs=2,
        learning_rate=5e-4,
        weight_decay=1e-5,
        device="cpu",
        early_stopping_monitor="val_segmental_f1_at_50",
        early_stopping_patience=5,
        class_weighting=True,
        ignore_label_id=0,
    )
    trained = trainer.fit(train, val, model=model, config=config, context=context)
    assert (output_dir / "best_model.pt").exists()
    assert (output_dir / "history.json").exists()
    mean, std = ASFormerTrainer.load_standardization(output_dir)
    preds = trainer.predict_records(val, model=trained, device=torch.device("cpu"), mean=mean, std=std)
    assert len(preds) == len(val)
    for video_id, pred in preds.items():
        assert pred.ndim == 1
        assert pred.dtype == np.int64


def test_asformer_core_stage_count() -> None:
    core = ASFormerCore(
        num_decoders=3,
        num_layers=2,
        r1=2,
        r2=2,
        num_f_maps=8,
        input_dim=16,
        num_classes=5,
        channel_masking_rate=0.0,
    )
    x = torch.randn(1, 16, 25)
    mask = torch.ones(1, 1, 25)
    out = core(x, mask)
    assert out.shape[0] == 4
