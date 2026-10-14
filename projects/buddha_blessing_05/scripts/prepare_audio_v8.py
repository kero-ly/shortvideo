"""Prepare a cleaned, tightly spaced narration run from the approved v7 phrases."""
import argparse, json, shutil, subprocess, wave
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--job', type=Path, required=True)
args = parser.parse_args()
source = args.source.resolve(); job = args.job.resolve(); (job / 'audio').mkdir(parents=True, exist_ok=False)

manifest = json.loads((source / 'tts-manifest.json').read_text())
filters = 'highpass=f=70,lowpass=f=11000,afftdn=nr=10:nf=-42,silenceremove=start_periods=1:start_duration=0.08:start_threshold=-42dB:stop_periods=1:stop_duration=0.20:stop_threshold=-42dB'
segments = []
for segment in manifest['segments']:
    sid = segment['id']
    output = job / 'audio' / f'{sid}.wav'
    subprocess.run(['ffmpeg', '-y', '-v', 'warning', '-i', str(source / 'audio' / f'{sid}.wav'), '-af', filters, '-ar', '48000', '-ac', '1', str(output)], check=True)
    with wave.open(str(output), 'rb') as wav:
        duration = wav.getnframes() / wav.getframerate()
    segments.append({**segment, 'raw_duration_seconds': duration, 'source_sha256': __import__('hashlib').sha256((source / 'audio' / f'{sid}.wav').read_bytes()).hexdigest(), 'output': str(output)})
(job / 'tts-manifest.json').write_text(json.dumps({**manifest, 'revision': 'v8-cleaned', 'segments': segments, 'cleanup': filters, 'gap_target_seconds': 0.20}, ensure_ascii=False, indent=2))
shutil.copy2(source / 'voice-reference.json', job / 'voice-reference.json')
(job / 'revision.json').write_text(json.dumps({'revision': 8, 'source_run': str(source), 'audio': 'approved phrase WAVs, highpass/lowpass/afftdn, leading/trailing silence trimmed, 0.20s inter-phrase target gap', 'caption_color': 'third sentence pink #FF8FA3'}, ensure_ascii=False, indent=2))
print(json.dumps({'job': str(job), 'segments': [(s['id'], s['raw_duration_seconds']) for s in segments]}, ensure_ascii=False))
