"""Restore phrase-02 onset from pre-trim source; leave accepted phrases untouched."""
import argparse, hashlib, json, shutil, subprocess, wave
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--job',type=Path,required=True); a=p.parse_args()
E=Path(__file__).resolve().parents[1]; old=E/'runs/revision-v8-20261014-audio'; original=E/'runs/revision-v7-20261014'
job=a.job.resolve(); (job/'audio').mkdir(parents=True,exist_ok=False)
manifest=json.loads((old/'tts-manifest.json').read_text())
for s in manifest['segments']:
    sid=s['id']; src=(original if sid=='phrase-02' else old)/'audio'/f'{sid}.wav'; dst=job/'audio'/f'{sid}.wav'
    if sid=='phrase-02':
        # No silence-removal or leading fade: preserve the low-energy initial consonant.
        subprocess.run(['ffmpeg','-y','-v','warning','-i',str(src),'-af','highpass=f=60,afftdn=nr=5:nf=-45','-ar','48000','-ac','1',str(dst)],check=True)
    else: shutil.copy2(src,dst)
    with wave.open(str(dst),'rb') as w: s['raw_duration_seconds']=w.getnframes()/w.getframerate()
    s.update(output=str(dst),source_path=str(src),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),processing='mild noise reduction without onset trim' if sid=='phrase-02' else 'unchanged v8 accepted phrase')
manifest.update(revision='v10-onset-repair',inter_phrase_gaps_seconds=[.35,.55],cleanup='phrase-02 restored from v7 with mild noise reduction, no silenceremove; phrase-01/04 unchanged v8')
(job/'tts-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
shutil.copy2(old/'voice-reference.json',job/'voice-reference.json')
(job/'revision.json').write_text(json.dumps(dict(revision=10,reason='user reports unnatural 家 onset and rushed second transition',preserve='v9 visual clip, 192px captions, pink final sentence, gold title',onset_repair='restore full phrase-02 pre-trim WAV; no onset trim',phrase_gaps_seconds=[.35,.55],listening='pending'),ensure_ascii=False,indent=2))
print('AUDIO_SOURCE_READY',job,flush=True)
