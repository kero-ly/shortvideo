import json,os,sys,subprocess,time,uuid,hashlib,math,wave
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo'
sys.path.insert(0,str(ROOT/'pipeline'));from gpu_lock import acquire
assert json.loads((P/'production-plan.json').read_text())['status']=='production_approved'
s=json.loads((P/'storyboard/revision-v4.json').read_text())
job=P/'runs'/('audio-v4-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir(parents=True)
(P/'review/latest-audio-v4.txt').write_text(str(job.relative_to(P)))
plan=[dict(id=x['id'],text=x['narration'],duration_ms=x['estimated_seconds']*1000) for x in s['shots']];(job/'tts-plan.json').write_text(json.dumps(plan,ensure_ascii=False))
n=json.loads((ROOT/'configs/resources.json').read_text())['narration'];cache=Path(n['runtime'])/'hf_cache'
def snap(repo):
 paths=list((cache/('models--'+repo)/'snapshots').iterdir());assert len(paths)==1;return paths[0]
with acquire(ROOT/'.runtime/gpu-job.lock'):
 rows=subprocess.check_output(['nvidia-smi','--query-gpu=index,memory.free,utilization.gpu','--format=csv,noheader,nounits'],text=True);(job/'gpu-preflight.txt').write_text(rows)
 idle=[list(map(int,r.split(','))) for r in rows.splitlines() if int(r.split(',')[1])>=12000 and int(r.split(',')[2])<=10];assert idle,'No idle GPU'
 gpu=max(idle,key=lambda x:x[1])[0]
 env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=str(gpu),PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',XDG_CACHE_HOME=str(ROOT/'.cache'),HF_HOME=str(ROOT/'.cache/huggingface'),TORCH_HOME=str(ROOT/'.cache/torch'),NUMBA_CACHE_DIR=str(ROOT/'.cache/numba'),MPLCONFIGDIR=str(ROOT/'.cache/matplotlib'))
 cmd=[n['python'],str(ROOT/'capabilities/narration/indextts2.py'),'--runtime-dir',n['runtime'],'--model-dir',n['models'],'--plan',str(job/'tts-plan.json'),'--reference-audio',n['reference'],'--output-dir',str(job/'audio'),'--manifest',str(job/'tts-manifest.json'),'--w2v-bert-dir',str(snap('facebook--w2v-bert-2.0')),'--maskgct-codec',str(snap('amphion--MaskGCT')/'semantic_codec/model.safetensors'),'--campplus-checkpoint',str(snap('funasr--campplus')/'campplus_cn_common.bin'),'--bigvgan-dir',str(snap('nvidia--bigvgan_v2_22khz_80band_256x')),'--emotion-alpha','0.45']
 with (job/'tts.log').open('w') as log:subprocess.run(cmd,cwd=job,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
segments=[];cursor=0;pcm=[];rate=None
for i,x in enumerate(s['shots']):
 f=job/'audio'/(x['id']+'.wav')
 with wave.open(str(f),'rb') as w:
  assert w.getsampwidth()==2 and w.getnchannels()==1
  if rate:assert rate==w.getframerate()
  rate=w.getframerate();data=w.readframes(w.getnframes());duration=w.getnframes()/rate
 lead=.15;tail=.85 if i==15 else .4;frames=math.ceil((duration+lead+tail)*24);samples=round(frames/24*rate)
 padded=b'\0'*round(lead*rate)*2+data;pcm.append(padded+b'\0'*(samples-len(padded)//2)*2)
 segments.append(dict(id=x['id'],text=x['narration'],phase=x['phase'],screen_text=x['screen_text'],start=cursor,frames=frames,audio_start=cursor/24+lead,audio_duration=duration,audio=str(f.relative_to(P)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),production_frames=5+17*math.ceil((max(124,frames)-5)/17)));cursor+=frames
with wave.open(str(job/'narration.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(b''.join(pcm))
evidence={'engine':'IndexTTS2','reference':n['reference'],'reference_sha256':hashlib.sha256(Path(n['reference']).read_bytes()).hexdigest(),'voice_source_status':'configured factory reference, public-use authorization not documented in available project records','music':None,'tempo':1.0,'fps':24,'total_frames':cursor,'duration_seconds':cursor/24,'narration':str((job/'narration.wav').relative_to(P)),'narration_sha256':hashlib.sha256((job/'narration.wav').read_bytes()).hexdigest(),'shots':segments}
(P/'timeline').mkdir(exist_ok=True);(P/'timeline/audio-v4.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n');(P/'review/audio-evidence-v4.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n');print('AUDIO_READY '+str(job),flush=True)
