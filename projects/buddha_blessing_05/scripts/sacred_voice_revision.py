"""220-only voice revision: preserve authorized speech, lower pitch without retiming."""
import argparse, hashlib, json, shutil, subprocess, time, wave
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--finish', type=Path)
a = p.parse_args()
E = Path(__file__).resolve().parents[1]
pitch = 2 ** (-3 / 12)
voice_filter = f'rubberband=tempo=1:pitch={pitch:.9f},highpass=f=65,equalizer=f=150:t=q:w=0.8:g=3,equalizer=f=3200:t=q:w=1:g=-1'
space_filter = 'aecho=0.9:0.95:110|230|390:0.13|0.08|0.04'
def digest(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def ff(args): subprocess.run(['ffmpeg', '-y', '-v', 'warning', *map(str,args)], check=True)

if not a.finish:
    job = E/'runs'/('voice-sacred-v2-'+time.strftime('%Y%m%d-%H%M%S'))
    (job/'audio').mkdir(parents=True, exist_ok=False)
    manifest = json.loads((a.source/'tts-manifest.json').read_text())
    sources = []
    for s in manifest['segments']:
        old = a.source/'audio'/f"{s['id']}.wav"
        new = job/'audio'/old.name
        ff(['-i',old,'-af',voice_filter,'-ar','24000','-ac','1',new])
        with wave.open(str(new)) as w: duration = w.getnframes()/w.getframerate()
        sources.append({'id':s['id'],'source':str(old),'source_sha256':digest(old),'processed_sha256':digest(new)})
        s.update(output=str(new),raw_duration_seconds=round(duration,3),tempo=1.0)
    manifest['voice_revision']={'source_job':str(a.source),'method':'pitch-shift and EQ of authorized existing IndexTTS2 speech; no new TTS/model invocation','semitones':-3,'voice_filter':voice_filter,'authorization':'user: 我有授权，你需要换成佛祖那样的神圣配音','sources':sources}
    (job/'tts-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print('VOICE_JOB '+str(job),flush=True)
else:
    job = a.finish
    # Reuse the actual original music; only voice and its ducking response change.
    shutil.copy2(a.source/'music-original.wav',job/'music-original.wav')
    filters=f'[0:a]{space_filter},atrim=duration=15,asplit=2[v][side];[1:a]volume=0.75[m];[m][side]sidechaincompress=threshold=0.02:ratio=4:attack=12:release=220[duck];[v][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=8,aresample=48000[mix]'
    ff(['-i',job/'narration.wav','-i',job/'music-original.wav','-filter_complex',filters,'-map','[mix]','-ac','2','-t','15',job/'mix.wav'])
    music = json.loads((a.source/'music-source.json').read_text())
    music.update(source_job=str(a.source),music_sha256=digest(job/'music-original.wav'),mix_filter=filters)
    (job/'music-source.json').write_text(json.dumps(music,ensure_ascii=False,indent=2))
    effect={'direction':'低沉庄严，轻微殿堂空间感，非原视频原声','pitch_semitones':-3,'tempo':1,'reverb_delays_ms':[110,230,390],'reverb_gains':[.13,.08,.04],'reverb_tail_max_seconds':.39,'narration_sha256':digest(job/'narration.wav'),'mix_sha256':digest(job/'mix.wav'),'actual_listening':'pending'}
    (job/'voice-effects.json').write_text(json.dumps(effect,ensure_ascii=False,indent=2))
    print('SACRED_MIX_READY '+str(job),flush=True)
