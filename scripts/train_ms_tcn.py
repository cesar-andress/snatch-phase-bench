#!/usr/bin/env python3
"""Train MS-TCN on the SnatchPhaseBench frame-sequence dataset."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import yaml

from snatch_phase_bench.benchmark.experiment_metadata import build_protocol_freeze, capture_environment, write_json
from snatch_phase_bench.benchmark.registry import load_model_experiment_config
from snatch_phase_bench.config import load_config, resolve_path
from snatch_phase_bench.data.frame_sequence import iter_frame_sequences, summarize_frame_sequences
from snatch_phase_bench.data.splits import load_athlete_split
from snatch_phase_bench.experiments.config_loader import get_section
from snatch_phase_bench.models.registry import build_model, count_parameters
from snatch_phase_bench.ontology.loader import load_benchmark_manifest
from snatch_phase_bench.training.interfaces import TrainerConfig, TrainingRunContext
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer
from snatch_phase_bench.utils.logging import setup_logging


def _resolve_dataset_paths(config: dict) -> tuple[Path, Path, Path]:
    if config.get("paths", {}).get("use_reproduction_paths", False):
        reproduction = load_config()
        labels_csv = resolve_path(reproduction, "labels_csv")
        keypoints_dir = resolve_path(reproduction, "keypoints_dir")
        split_json = resolve_path(reproduction, "athlete_split_json")
        return labels_csv, keypoints_dir, split_json
    raise ValueError("Only use_reproduction_paths=true is supported.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train MS-TCN benchmark model.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/benchmark/ms_tcn.yaml"),
        help="Experiment YAML path.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint_last.pt.")
    args = parser.parse_args()

    setup_logging()
    config = load_model_experiment_config(args.config)
    labels_csv, keypoints_dir, split_json = _resolve_dataset_paths(config)
    split = load_athlete_split(split_json)
    manifest = load_benchmark_manifest()

    dataset_cfg = get_section(config, "dataset")
    model_cfg = get_section(config, "model")
    train_cfg = get_section(config, "training")
    loss_cfg = get_section(config, "loss")
    optimizer_cfg = get_section(config, "optimizer")
    ontology_cfg = get_section(config, "ontology")
    output_cfg = get_section(config, "output")

    train_records = list(
        iter_frame_sequences(
            labels_csv=labels_csv,
            keypoints_dir=keypoints_dir,
            use_z=bool(dataset_cfg.get("use_z", True)),
            athlete_split=split,
            split_filter="train",
        )
    )
    val_records = list(
        iter_frame_sequences(
            labels_csv=labels_csv,
            keypoints_dir=keypoints_dir,
            use_z=bool(dataset_cfg.get("use_z", True)),
            athlete_split=split,
            split_filter="val",
        )
    )

    num_classes = int(ontology_cfg.get("ignore_label_id", 0)) + int(
        ontology_cfg.get("num_supervised_classes", 7)
    )
    model = build_model(
        str(model_cfg["name"]),
        input_size=int(dataset_cfg.get("features_per_frame", 99)),
        num_classes=num_classes,
        num_stages=int(model_cfg["num_stages"]),
        num_layers=int(model_cfg["num_layers"]),
        num_f_maps=int(model_cfg["num_f_maps"]),
        kernel_size=int(model_cfg.get("kernel_size", 3)),
        dropout=float(model_cfg.get("dropout", 0.5)),
    )

    output_dir = Path(str(output_cfg["checkpoint_dir"])) / f"seed{args.seed}"
    output_dir.mkdir(parents=True, exist_ok=True)
    context = TrainingRunContext(
        model_id="ms_tcn",
        registry_name=str(config["experiment"]["registry_name"]),
        config_path=Path(str(config["config_path"])),
        seed=args.seed,
        split_version=str(manifest["split"]["version"]),
        dataset_version=str(manifest["dataset"]["version"]),
        output_dir=output_dir,
        extra={"resume": args.resume},
    )

    early_stopping_cfg = train_cfg.get("early_stopping", {})
    trainer = MSTCNTrainer(
        num_classes=num_classes,
        tmse_weight=float(loss_cfg.get("tmse_weight", 0.15)),
        tmse_truncate_tau=float(loss_cfg.get("tmse_truncate_tau", 4.0)),
        use_amp=bool(train_cfg.get("use_amp", False)),
        log_dir=Path(str(output_cfg.get("tensorboard_dir", output_dir / "tensorboard"))) / f"seed{args.seed}",
    )
    trainer_config = TrainerConfig(
        batch_size=int(train_cfg.get("batch_size", 1)),
        epochs=int(train_cfg.get("epochs", 50)),
        learning_rate=float(optimizer_cfg.get("learning_rate", 5e-4)),
        weight_decay=float(optimizer_cfg.get("weight_decay", 0.0)),
        device=str(train_cfg.get("device", "auto")),
        early_stopping_monitor=str(early_stopping_cfg.get("monitor", "val_segmental_f1_at_50")),
        early_stopping_patience=int(early_stopping_cfg.get("patience", 15)),
        class_weighting=bool(train_cfg.get("class_weighting", True)),
        ignore_label_id=int(ontology_cfg.get("ignore_label_id", 0)),
    )

    (output_dir / "config_snapshot.yaml").write_text(
        yaml.safe_dump(config, sort_keys=False),
        encoding="utf-8",
    )
    write_json(output_dir / "environment.json", capture_environment())

    start = time.perf_counter()
    model = trainer.fit(train_records, val_records, model=model, config=trainer_config, context=context)
    runtime_seconds = time.perf_counter() - start

    early_stop = {}
    early_stop_path = output_dir / "early_stopping.json"
    if early_stop_path.exists():
        early_stop = json.loads(early_stop_path.read_text(encoding="utf-8"))

    summary = {
        "model": model.name,
        "seed": args.seed,
        "train_videos": len(train_records),
        "val_videos": len(val_records),
        "train_stats": summarize_frame_sequences(train_records),
        "val_stats": summarize_frame_sequences(val_records),
        "parameter_count": count_parameters(model),
        "runtime_seconds": runtime_seconds,
        "early_stopping": early_stop,
        "output_dir": str(output_dir),
        "evaluator_version": manifest["evaluation"]["version"],
        "ontology_version": manifest["ontology"]["canonical"],
    }
    (output_dir / "train_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
