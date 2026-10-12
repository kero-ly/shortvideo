"""Rebuild approved scene narration and synthesize original light instrumental on 220."""
import array,hashlib,json,math,random,subprocess,time,uuid,wave
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo'
props=json.loads((P/'timeline.json').read_text());duration=props['durationInFrames']/24
job=ROOT/'runs'/('storybook-audio-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir()
source=ROOT/'runs/early-pregnancy-20261013-010143-e9a8/audio';checks=[];parts=[]
def run(cmd):subprocess.run(list(map(str,cmd)),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
for s in props['scenes']:
 src=source/(s['id']+'.wav');d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(src)]));slot=s['frames']/24
 assert d<=slot-.6,(s['id'],d,slot)
 dest=job/(s['id']+'.wav');run(['ffmpeg','-y','-i',src,'-af','apad','-t',slot,'-ar',48000,'-ac',1,'-c:a','pcm_s16le',dest]);parts.append(dest)
 checks.append({'id':s['id'],'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'speech_end':s['start']/24+d,'slot_end':(s['start']+s['frames'])/24,'complete':True})
(job/'concat.txt').write_text(''.join("file '"+str(p)+"'\n" for p in parts));run(['ffmpeg','-y','-f','concat','-safe',0,'-i',job/'concat.txt','-c','copy',job/'narration.wav'])
# Original C-major / A-minor light plucked instrumental, 104 BPM, deterministic arrangement.
sr=24000;n=round(duration*sr);buf=array.array('f',[0])*n;rng=random.Random(20261013);beat=60/104
chords=[[60,64,67],[57,60,64],[53,57,60],[55,59,62]]
def note(start,midi,length,amp):
 f=440*2**((midi-69)/12);offset=int(start*sr)
 for i in range(min(int(length*sr),n-offset)):
  t=i/sr;env=min(1,t/.009)*math.exp(-t*4.5)*min(1,(length-t)/.08)
  buf[offset+i]+=amp*env*(math.sin(2*math.pi*f*t)+.25*math.sin(4*math.pi*f*t)+.08*math.sin(6*math.pi*f*t))
for b in range(math.ceil(duration/beat)):
 start=b*beat;ch=chords[(b//4)%4];note(start,ch[b%3]+12,beat*1.5,.16);note(start+beat/2,ch[(b+1)%3]+12,beat*.8,.08)
 if b%2==0:note(start,ch[0]-12,beat*1.8,.12)
 for i in range(min(int(.065*sr),n-int(start*sr))):buf[int(start*sr)+i]+=(rng.random()*2-1)*.024*math.exp(-i/sr*65)
pcm=array.array('h',(int(max(-1,min(1,v))*32767) for v in buf))
with wave.open(str(job/'music-original.wav'),'wb') as w:w.setparams((1,2,sr,n,'NONE','not compressed'));w.writeframes(pcm.tobytes())
# Music is independently leveled, lightly ducked under narration, then mixed and normalized.
run(['ffmpeg','-y','-i',job/'narration.wav','-i',job/'music-original.wav','-filter_complex',f'[0:a]loudnorm=I=-17:TP=-2:LRA=11,aresample=48000,asplit=2[v][side];[1:a]loudnorm=I=-25:TP=-5:LRA=7,aresample=48000,afade=t=in:d=1.2,afade=t=out:st={duration-2}:d=2[m];[m][side]sidechaincompress=threshold=0.04:ratio=2:attack=25:release=350:makeup=1[duck];[v][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad[out]','-map','[out]','-t',duration,'-ar',48000,'-ac',2,job/'mix.wav'])
qa={'complete_narration':all(s['complete'] for s in checks),'segments':checks,'duration_seconds':duration,'ending_tail_seconds':duration-checks[-1]['speech_end'],'music':{'source':'original procedural composition','tempo_bpm':104,'style':'light plucked melody, soft bass and shaker','seed':20261013,'music_lufs_before_ducking':-25,'voice_lufs_before_mix':-17,'mix_target_lufs':-16},'listening':'Full human listening pending'}
(job/'audio-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));props['mix_path']=str((job/'mix.wav').relative_to(ROOT));(P/'timeline.json').write_text(json.dumps(props,ensure_ascii=False,indent=2));print(job,flush=True)
