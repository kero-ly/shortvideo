"""CPU word alignment and original peaceful music, using real phrase audio."""
import argparse, difflib, hashlib, json, re, subprocess, wave
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
p=argparse.ArgumentParser();p.add_argument('--job',type=Path,required=True);p.add_argument('--dynamic-timing',action='store_true');p.add_argument('--font-size',type=int,default=68);a=p.parse_args();R=a.job.resolve();ROOT=Path(__file__).resolve().parents[3]
manifest=json.loads((R/'tts-manifest.json').read_text());duration=14.375;sr=48000
positions=[.4,2.65,4.85,7.10,10.40,12.65]
lengths=[]
for segment in manifest['segments']:
 with wave.open(str(R/'audio'/f"{segment['id']}.wav"),'rb') as wav: lengths.append(wav.getnframes()/wav.getframerate())
gaps=[.35,.55]
positions=[.15]
for length,gap in zip(lengths[:-1],gaps): positions.append(positions[-1]+length+gap)
assert positions[-1]+lengths[-1] <= duration-.6, ('cleaned narration exceeds duration', lengths)
texts=['见佛送花福到你家','家旺财旺子孙旺','一顺百顺阖家幸福平安顺遂']
cache=ROOT/'.cache/asr-model-cache/models--Systran--faster-whisper-small/snapshots'
model=WhisperModel(str(next(cache.iterdir())),device='cpu',compute_type='int8',cpu_threads=4)
voice=np.zeros(round(duration*sr));rows=[];clean=lambda t:re.sub(r'[^\u4e00-\u9fff0-9]','',t)
for i,s in enumerate(manifest['segments']):
 path=R/'audio'/f"{s['id']}.wav"
 pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar',str(sr),'-ac','1','-f','f32le','-']),dtype='<f4')
 offset=positions[i];stop=offset+len(pcm)/sr
 assert stop<=(positions[i+1]-.08 if i<len(manifest['segments'])-1 else duration-.6),('audio exceeds slot',s['id'],stop)
 start=round(offset*sr);voice[start:start+len(pcm)]+=pcm
 samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar','16000','-ac','1','-f','f32le','-']),dtype='<f4')
 segs,_=model.transcribe(samples,language='zh',word_timestamps=True,beam_size=5,vad_filter=False,initial_prompt=s['text'])
 words=[dict(text=w.word,start=w.start,end=w.end) for seg in segs for w in (seg.words or [])];assert words
 recognized=''.join(w['text'] for w in words);ratio=difflib.SequenceMatcher(None,clean(s['text']),clean(recognized)).ratio()
 assert words[-1]['end']<=s['raw_duration_seconds']+.15
 rows.append(dict(id=s['id'],shot_id='01',source_indices=[i],text=texts[i],locked_narration=s['text'],recognized=recognized,similarity=ratio,words=words,audio_start=offset,audio_end=stop,start=offset+words[0]['start'],end=offset+words[-1]['end'],sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 print(s['id'],recognized,ratio,flush=True)
def save(path,data):
 with wave.open(str(path),'wb') as w:w.setnchannels(1 if data.ndim==1 else 2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
save(R/'narration.wav',voice)
# Original warm drone and sparse bell partials; no external recordings.
n=len(voice);t=np.arange(n)/sr;music=np.zeros((n,2))
for freq,amp in [(130.8128,.025),(195.9977,.013),(261.6256,.008)]:
 pad=amp*np.sin(2*np.pi*freq*t)*(1+.12*np.sin(2*np.pi*.12*t));music[:,0]+=pad;music[:,1]+=pad
for start,note in [(0.05,76),(4.5,79),(9.3,81),(13.2,76)]:
 at=round(start*sr);x=np.arange(n-at)/sr;f=440*2**((note-69)/12)
 bell=sum(amp*np.sin(2*np.pi*f*partial*x)*np.exp(-x/decay) for partial,amp,decay in [(1,.045,1.5),(2.01,.016,.85),(2.76,.006,.55)])
 bell*=np.minimum(x/.012,1);music[at:,0]+=bell;music[at:,1]+=bell*.88
fade=np.minimum(t/.8,1)*np.minimum((duration-t)/1.2,1);music*=fade[:,None];save(R/'music-original.wav',music)
# Continuous diffuse stereo reverberation from the complete narration bus.
# Deterministic filtered-noise impulse, no synthetic noise floor on the voice.
rng=np.random.default_rng(1105); irlen=round(1.1*sr); u=np.arange(irlen)/sr
wet=np.zeros((n,2)); fftn=1 << (n+irlen-2).bit_length()
for ch in range(2):
 ir=rng.normal(size=irlen)*np.exp(-u/0.19)
 ir=np.convolve(ir,np.ones(9)/9,mode='same'); ir[:round(.025*sr)]=0
 ir/=np.sqrt(np.sum(ir**2))
 wet[:,ch]=np.fft.irfft(np.fft.rfft(voice,fftn)*np.fft.rfft(ir,fftn),fftn)[:n]
wet*=.14; wet*=np.minimum((duration-t)/.35,1)[:,None]
save(R/'voice-reverb.wav',wet)
filters='[0:a]volume=1.15,asplit=2[v][side];[1:a]volume=0.95[m];[m][side]sidechaincompress=threshold=0.035:ratio=2:attack=25:release=600[duck];[2:a]volume=1.15[r];[v][duck][r]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=8,aresample=48000[mix]'
subprocess.run(['ffmpeg','-y','-v','warning','-i',str(R/'narration.wav'),'-i',str(R/'music-original.wav'),'-i',str(R/'voice-reverb.wav'),'-filter_complex',filters,'-map','[mix]','-ac','2',str(R/'mix.wav')],check=True)
source_rows=rows.copy()
# Split at actual recognized word boundaries, retaining source phrase hashes.
chunks=[['见佛送花','福到你家'],['家旺财旺','子孙旺'],['一顺百顺','阖家幸福','平安顺遂']]
rows=[]
for source,parts in zip(source_rows,chunks):
 cursor=0;word_ranges=[]
 for w in source['words']:
  nchar=len(clean(w['text']));word_ranges.append((cursor,cursor+nchar,w));cursor+=nchar
 assert clean(source['recognized'])==clean(source['locked_narration']),source
 cursor=0
 for part in parts:
  end=cursor+len(part);matched=[w for lo,hi,w in word_ranges if hi>cursor and lo<end];assert matched
  rows.append(dict(source,text=part,start=source['audio_start']+matched[0]['start'],end=source['audio_start']+matched[-1]['end']))
  cursor=end
for i,r in enumerate(rows):r['end']=rows[i+1]['start']-.05 if i<len(rows)-1 else duration-.3
narration_hash=hashlib.sha256((R/'narration.wav').read_bytes()).hexdigest()
alignment=dict(engine='faster-whisper small CPU int8 real word timestamps, locked copy retained',duration=duration,narration_sha256=narration_hash,cues=rows,inter_phrase_gaps_seconds=gaps,actual_listening='pending')
(R/'alignment.json').write_text(json.dumps(alignment,ensure_ascii=False,indent=2))
def stamp(v,ass=False):
 if ass:
  c=round(v*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
 ms=round(v*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(R/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['end'])}\n{r['text']}" for i,r in enumerate(rows))+'\n')
header='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Blessing,Noto Sans CJK SC,68,&H00FFFFFF,&H00FFFFFF,&H00111111,&H00000000,-1,0,0,0,100,100,1,0,1,8,0,2,90,150,326,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
header=header.replace('SC,68,',f'SC,{a.font_size},').replace(',-1,0,0,0,100',',-1,-1,0,0,100').replace(',1,8,0,2,',',1,14,0,2,')
lines=[]
for r in rows:
 text=r['text']
 color=r'{\c&H008FA3FF&}' if text in ('一顺百顺','阖家幸福','平安顺遂') else ''
 lines.append(f"Dialogue: 0,{stamp(r['start'],True)},{stamp(r['end'],True)},Blessing,,0,0,0,,{color}{text}")
# Retain the exact v9 style header and fixed gold title; only cue times change.
v9=R.parents[0]/'revision-v9-20261015-caption'/'captions.ass'
old=v9.read_text(); header=old[:old.index('Dialogue: 0,')]
(R/'captions.ass').write_text(header+'\n'.join(lines)+'\n')
(R/'music-source.json').write_text(json.dumps(dict(source='original procedural composition; no external recordings',generator='scripts/align_v11.py',cleanup='original phrase-04 onset restored; only verified post-word tails shortened',reverb=dict(type='deterministic diffuse stereo convolution',seed=1105,ir_seconds=1.1,predelay_seconds=.025,wet_gain=.14),continuity='reverb computed after assembling narration; tails span both pauses; music duck release600ms',instruments='warm sine drone and sparse additive bells',key='C pentatonic',duration=duration,fade_in=.8,fade_out=1.2,mix_filter=filters),indent=2))
print('AUDIO_READY',R,flush=True)
