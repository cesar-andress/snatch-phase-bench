#!/usr/bin/env python3
"""Evaluate an MS-TCN checkpoint with canonical benchmark metrics."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from snatch_phase_bench.benchmark.gpu_runtime import (
    GpuMemoryTracker,
    collect_cuda_warnings,
    resolve_cuda_device_index,
)
from snatch_phase_bench.benchmark.results_export import enrich_eval_result_with_frame_metrics, export_predictions_json
from snatch_phase_bench.benchmark.registry import load_model_experiment_config
from snatch_phase_bench.config import load_config, resolve_path
from snatch_phase_bench.data.frame_sequence import iter_frame_sequences
from snatch_phase_bench.data.splits import load_athlete_split
from snatch_phase_bench.evaluation.results import write_evaluation_result
from snatch_phase_bench.evaluation.tas_hooks import evaluate_frame_predictions
from snatch_phase_bench.experiments.config_loader import get_section
from snatch_phase_bench.models.ms_tcn.inference import load_ms_tcn_from_checkpoint, predict_videos
from snatch_phase_bench.training.lstm_trainer import resolve_device, resolve_num_classes
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer
from snatch_phase_bench.utils.logging import setup_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate MS-TCN checkpoint.")
    parser.add_argument("--config", type=Path, default=Path("configs/benchmark/ms_tcn.yaml"))
    parser.add_argument("--checkpoint", type=Path, required=True, help="Path to best_model.pt")
    parser.add_argument("--split", choices=["train", "val", "test"], default="test")
    parser.add_argument("--output", type=Path, default=None, help="Evaluation JSON output path.")
    args = parser.parse_args()

    setup_logging()
    config = load_model_experiment_config(args.config)
    reproduction = load_config()
    labels_csv = resolve_path(reproduction, "labels_csv")
    keypoints_dir = resolve_path(reproduction, "keypoints_dir")
    split_json = resolve_path(reproduction, "athlete_split_json")
    split = load_athlete_split(split_json)

    dataset_cfg = get_section(config, "dataset")
    model_cfg = get_section(config, "model")
    ontology_cfg = get_section(config, "ontology")
    train_cfg = get_section(config, "training")

    records = list(
        iter_frame_sequences(
            labels_csv=labels_csv,
            keypoints_dir=keypoints_dir,
            use_z=bool(dataset_cfg.get("use_z", True)),
            athlete_split=split,
            split_filter=args.split,
        )
    )

    num_classes = resolve_num_classes(ontology_cfg)
    device = resolve_device(str(train_cfg.get("device", "cuda")))
    model, _payload = load_ms_tcn_from_checkpoint(
        args.checkpoint,
        input_size=int(dataset_cfg.get("features_per_frame", 99)),
        num_classes=num_classes,
        num_stages=int(model_cfg["num_stages"]),
        num_layers=int(model_cfg["num_layers"]),
        num_f_maps=int(model_cfg["num_f_maps"]),
        kernel_size=int(model_cfg.get("kernel_size", 3)),
        dropout=float(model_cfg.get("dropout", 0.5)),
    )
    checkpoint_dir = args.checkpoint.parent
    mean, std = MSTCNTrainer.load_standardization(checkpoint_dir)

    gpu_tracker = GpuMemoryTracker(device_index=resolve_cuda_device_index(device))
    if device.type == "cuda":
        gpu_tracker.reset_peak()

    infer_start = time.perf_counter()
    try:
        predictions = predict_videos(records, model=model, mean=mean, std=std, device=str(device))
    except RuntimeError as exc:
        if device.type == "cuda" and "out of memory" in str(exc).lower():
            raise RuntimeError(
                "CUDA out-of-memory during MS-TCN inference. "
                "Report failure; do not silently change batch size or device mid-protocol."
            ) from exc
        raise
    inference_seconds = time.perf_counter() - infer_start
    total_frames = sum(record.num_frames for record in records)
    if device.type == "cuda":
        gpu_tracker.update_peak()
        gpu_tracker.cuda_warnings.extend(collect_cuda_warnings())

    output_dir = args.checkpoint.parent
    predictions_path = output_dir / f"predictions_{args.split}.json"
    export_predictions_json(records, predictions, predictions_path)

    output_path = args.output or output_dir / f"eval_{args.split}.json"
    result = evaluate_frame_predictions(
        records,
        predictions,
        model_identifier=f"ms_tcn_{checkpoint_dir.name}",
    )
    enriched = enrich_eval_result_with_frame_metrics(
        result,
        predictions_path,
        ignore_label_id=int(ontology_cfg.get("ignore_label_id", 0)),
    )
    enriched["inference_runtime"] = {
        "seconds": inference_seconds,
        "frames": total_frames,
        "seconds_per_frame": inference_seconds / total_frames if total_frames else None,
        "device": str(device),
    }
    enriched["gpu_runtime"] = gpu_tracker.snapshot()
    write_evaluation_result(output_path, result)
    output_path.write_text(json.dumps(enriched, indent=2, sort_keys=True), encoding="utf-8")

    eval_runtime_path = output_dir / f"inference_{args.split}.json"
    eval_runtime_path.write_text(
        json.dumps(
            {
                "split": args.split,
                "inference_seconds": inference_seconds,
                "frames": total_frames,
                "device": str(device),
                "gpu_runtime": gpu_tracker.snapshot(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output": str(output_path),
                "predictions": str(predictions_path),
                "videos": len(records),
                "aggregate": result.aggregate,
                "frame_macro_f1": enriched.get("frame_macro_f1"),
                "inference_seconds": inference_seconds,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
