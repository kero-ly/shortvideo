#!/usr/bin/env python3
"""Generate timed-plan narration segments with an existing IndexTTS2 checkout."""

import argparse
import json
import sys
import time
import wave
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-dir", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--reference-audio", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--w2v-bert-dir", type=Path, required=True)
    parser.add_argument("--maskgct-codec", type=Path, required=True)
    parser.add_argument("--campplus-checkpoint", type=Path, required=True)
    parser.add_argument("--bigvgan-dir", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--emotion-alpha", type=float, default=0.65)
    return parser.parse_args()


def install_local_asset_routes(args: argparse.Namespace):
    sys.path.insert(0, str(args.runtime_dir))
    import indextts.infer_v2 as infer_v2
    import indextts.utils.maskgct_utils as maskgct_utils

    original_feature_loader = infer_v2.SeamlessM4TFeatureExtractor.from_pretrained
    original_semantic_loader = maskgct_utils.Wav2Vec2BertModel.from_pretrained
    original_bigvgan_loader = infer_v2.bigvgan.BigVGAN.from_pretrained

    def load_features(*_unused, **kwargs):
        kwargs["local_files_only"] = True
        return original_feature_loader(str(args.w2v_bert_dir), **kwargs)

    def load_semantic(*_unused, **kwargs):
        kwargs["local_files_only"] = True
        return original_semantic_loader(str(args.w2v_bert_dir), **kwargs)

    def local_hub_download(repo_id: str, filename: str, **_kwargs):
        if repo_id == "amphion/MaskGCT" and filename == "semantic_codec/model.safetensors":
            return str(args.maskgct_codec)
        if repo_id == "funasr/campplus" and filename == "campplus_cn_common.bin":
            return str(args.campplus_checkpoint)
        raise RuntimeError(f"No local route for {repo_id}/{filename}")

    def load_bigvgan(*_unused, **kwargs):
        return original_bigvgan_loader(str(args.bigvgan_dir), **kwargs)

    def save_wav(path: str, audio, sample_rate: int, **_kwargs) -> None:
        samples = audio.detach().cpu().numpy()
        if samples.ndim == 1:
            samples = samples[np.newaxis, :]
        samples = samples.astype("<i2", copy=False)
        with wave.open(str(path), "wb") as output:
            output.setnchannels(samples.shape[0])
            output.setsampwidth(2)
            output.setframerate(sample_rate)
            output.writeframes(samples.T.reshape(-1).tobytes())

    infer_v2.SeamlessM4TFeatureExtractor.from_pretrained = load_features
    maskgct_utils.Wav2Vec2BertModel.from_pretrained = load_semantic
    infer_v2.hf_hub_download = local_hub_download
    infer_v2.bigvgan.BigVGAN.from_pretrained = load_bigvgan
    infer_v2.torchaudio.save = save_wav
    return infer_v2


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / audio.getframerate()


def main() -> None:
    args = parse_args()
    plan = json.loads(args.plan.read_text())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    infer_v2 = install_local_asset_routes(args)

    load_started = time.perf_counter()
    engine = infer_v2.IndexTTS2(
        cfg_path=str(args.model_dir / "config.yaml"),
        model_dir=str(args.model_dir),
        use_fp16=True,
        device=args.device,
        use_cuda_kernel=False,
        use_deepspeed=False,
    )
    load_seconds = time.perf_counter() - load_started

    segments = []
    for segment in plan:
        output = args.output_dir / f"{segment['id']}.wav"
        started = time.perf_counter()
        engine.infer(
            str(args.reference_audio),
            str(segment["text"]),
            str(output),
            emo_vector=segment["emotion_vector"],
            emo_alpha=args.emotion_alpha,
            use_random=False,
            interval_silence=140,
            verbose=False,
        )
        result = {
            "id": segment["id"],
            "text": segment["text"],
            "emotion_vector": segment["emotion_vector"],
            "slot_duration_seconds": int(segment["duration_ms"]) / 1000,
            "raw_duration_seconds": round(wav_duration(output), 3),
            "tempo": 1.0,
            "inference_seconds": round(time.perf_counter() - started, 3),
            "output": str(output),
        }
        segments.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)

    manifest = {
        "engine": "IndexTTS2",
        "reference_audio": str(args.reference_audio),
        "emotion_alpha": args.emotion_alpha,
        "device": args.device,
        "load_seconds": round(load_seconds, 3),
        "segments": segments,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
