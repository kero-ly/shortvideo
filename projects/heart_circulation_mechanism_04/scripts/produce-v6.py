import json,os,subprocess,sys,math,wave,time
from pathlib import Path
ROOT=Path('/home/ly/shortvideo'); E=ROOT/'projects/heart_circulation_mechanism_04'; JOB=E/'runs/20261013-heart-v6'; JOB.mkdir(parents=True,exist_ok=True)
if (JOB/'tts-manifest.json').exists():raise RuntimeError('Historical run exists; allocate a new job ID before another synthesis')
sys.path.insert(0,str(ROOT));from pipeline.gpu_lock import acquire
texts=['心脏就像一台泵，靠收缩和舒张推动血液。','右侧心脏把血液送到肺部，在这里完成气体交换。','血液回到左侧心脏，再被送往全身。','红细胞沿着血管前进，把氧送到身体各处。','血液再回到心脏，两条循环接力，持续运转。']
plan=[dict(id=f'shot-{i+1:02}',text=t,duration_ms=6000,emotion_vector=[.48,0,0,0,0,0,.16,.36]) for i,t in enumerate(texts)];
for i,p in enumerate(plan):p['emotion_vector']=[[.42,0,0,0,0,0,.25,.33],[.5,0,0,0,0,0,.12,.38],[.4,0,0,0,0,0,.18,.42],[.62,0,0,0,0,0,.13,.25],[.4,0,0,0,0,0,.08,.52]][i]
(JOB/'tts-plan.json').write_text(json.dumps(plan,ensure_ascii=False))
n=json.loads((ROOT/'configs/resources.json').read_text())['narration'];cache=Path(n['runtime'])/'hf_cache'
def snap(repo):return next((cache/('models--'+repo)/'snapshots').iterdir())
env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES='6',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',XDG_CACHE_HOME=str(ROOT/'.cache'),HF_HOME=str(ROOT/'.cache/huggingface'),TORCH_HOME=str(ROOT/'.cache/torch'),NUMBA_CACHE_DIR=str(ROOT/'.cache/numba'),MPLCONFIGDIR=str(ROOT/'.cache/matplotlib'))
cmd=[n['python'],str(ROOT/'projects/heart_circulation_mechanism_04/scripts/tts-v6.py'),'--runtime-dir',n['runtime'],'--model-dir',n['models'],'--plan',str(JOB/'tts-plan.json'),'--reference-audio',n['reference'],'--output-dir',str(JOB/'audio'),'--manifest',str(JOB/'tts-manifest.json'),'--w2v-bert-dir',str(snap('facebook--w2v-bert-2.0')),'--maskgct-codec',str(snap('amphion--MaskGCT')/'semantic_codec/model.safetensors'),'--campplus-checkpoint',str(snap('funasr--campplus')/'campplus_cn_common.bin'),'--bigvgan-dir',str(snap('nvidia--bigvgan_v2_22khz_80band_256x')),'--emotion-alpha','0.85']
import fcntl
lock=(ROOT/'.runtime/gpu-job.lock').open('a+')
print('Queued on factory GPU lock',flush=True)
fcntl.flock(lock.fileno(),fcntl.LOCK_EX)
with lock:
 free=int(subprocess.check_output(['nvidia-smi','--id=6','--query-gpu=memory.free','--format=csv,noheader,nounits']).strip())
 assert free>=12000,('GPU6 insufficient free VRAM',free)
 subprocess.run(cmd,cwd=JOB,env=env,check=True)
segments=[];start=0;pcm=[];rate=None
for i,p in enumerate(plan):
 with wave.open(str(JOB/'audio'/f"{p['id']}.wav"),'rb') as w:
  assert w.getsampwidth()==2 and w.getnchannels()==1
  if rate:assert rate==w.getframerate()
  rate=w.getframerate();data=w.readframes(w.getnframes());duration=w.getnframes()/rate
 lead=.3;frames=math.ceil((duration+lead+(.9 if i==4 else .4))*30)
 samples=round(frames/30*rate);data=b'\0'*round(lead*rate)*2+data;pcm.append(data+b'\0'*(samples-len(data)//2)*2)
 segments.append(dict(id=p['id'],text=p['text'],duration_ms=round(frames/30*1000),start=start,frames=frames,audioStart=start/30+lead,audioDuration=duration));start+=frames
with wave.open(str(JOB/'narration.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(b''.join(pcm))
(JOB/'props.json').write_text(json.dumps(dict(shots=segments,totalFrames=start,revision=6),ensure_ascii=False,indent=2))
print('READY',start,flush=True)
