"""Original procedural 104 BPM pluck/percussion bed; no external recordings."""
import json,wave,subprocess
from pathlib import Path
import numpy as np
E=Path('/home/ly/shortvideo/projects/heart_circulation_mechanism_04');R=E/'runs/20261013-heart-v6'
p=json.loads((R/'props.json').read_text());duration=p['totalFrames']/30;sr=48000;n=round(duration*sr);out=np.zeros((n,2));rng=np.random.default_rng(613);beat=60/104
# Cmaj7 / Am7 / Fmaj7 / G6, sparse pentatonic melody, warm sine plucks.
chords=[[60,64,67,71],[57,60,64,67],[53,57,60,64],[55,59,62,64]];melody=[76,79,81,79,74,76,72,74]
def add(t,note,level,length=.55,pan=0):
 start=round(t*sr);count=min(round(length*sr),n-start)
 if count<=0:return
 x=np.arange(count)/sr;freq=440*2**((note-69)/12);env=(1-np.exp(-x*180))*np.exp(-x*6)
 y=level*env*(np.sin(2*np.pi*freq*x)+.22*np.sin(4*np.pi*freq*x))
 out[start:start+count,0]+=y*(1-pan*.3);out[start:start+count,1]+=y*(1+pan*.3)
for b in range(int(duration/beat)+1):
 t=b*beat;c=chords[(b//8)%4];add(t,c[b%4],.12,.8,(-1)**b*.5)
 if b%2==0:add(t+.5*beat,melody[(b//2)%8],.075,.5,(-1)**b*.6)
 if b%4==0:add(t,c[0]-24,.13,.5)
 start=round(t*sr);count=min(round(.06*sr),n-start)
 if count>0:
  x=np.arange(count)/sr;y=rng.normal(0,1,count)*np.exp(-x*90)*.018;out[start:start+count]+=y[:,None]
time=np.arange(n)/sr;fade=np.minimum(time/.7,1)*np.minimum((duration-time)/1.2,1);out*=fade[:,None]
with wave.open(str(R/'music-original.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
filters='[0:a]aresample=48000,volume=1.4,asplit=2[voice][side];[1:a]volume=0.48[music];[music][side]sidechaincompress=threshold=0.025:ratio=5:attack=12:release=240[duck];[voice][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=8:linear=false,aresample=48000[mix]'
subprocess.run(['ffmpeg','-y','-v','warning','-i',str(R/'narration.wav'),'-i',str(R/'music-original.wav'),'-filter_complex',filters,'-map','[mix]','-ac','2',str(R/'mix.wav')],check=True)
(R/'music-source.json').write_text(json.dumps(dict(source='original procedural composition; no external recordings',generator='scripts/music-v6.py',bpm=104,key='C major',instruments='sine pluck, bass and seeded noise percussion',seed=613,mix_filter=filters,fade_in=.7,fade_out=1.2,duration=duration),indent=2))
