"""Run from 220 with uv run python. All results stay in a unique factory run."""
import json, os, sys, subprocess, shutil, math, wave, time, uuid, re
from pathlib import Path
SOURCE=Path(__file__).resolve().parent
ROOT=SOURCE.parents[1]
sys.path.insert(0,str(ROOT/'pipeline'))
from gpu_lock import acquire
job=ROOT/'runs'/('early-pregnancy-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4])
job.mkdir(parents=True)
(SOURCE/'latest-run.txt').write_text(str(job))
def run(stage,cmd,**kw):
    print(stage,flush=True)
    (job/'status.json').write_text(json.dumps({'stage':stage,'run':str(job)},ensure_ascii=False))
    with (job/(stage+'.log')).open('w') as log: subprocess.run([str(x) for x in cmd],stdout=log,stderr=subprocess.STDOUT,check=True,**kw)
config=json.loads((ROOT/'configs/resources.json').read_text())
episode=json.loads((SOURCE/'episode.json').read_text())
lock=acquire(ROOT/'.runtime/gpu-job.lock')
rows=subprocess.check_output(['nvidia-smi','--query-gpu=index,memory.free,utilization.gpu','--format=csv,noheader,nounits'],text=True)
idle=[list(map(int,r.split(','))) for r in rows.splitlines() if int(r.split(',')[1])>=12000 and int(r.split(',')[2])<=10]
if not idle: raise RuntimeError('No idle GPU with 12 GB free; do not interrupt shared jobs')
gpu=max(idle,key=lambda x:x[1])[0]
(job/'gpu-before.txt').write_text(rows)
plan=[dict(id=s['id'],text=s['text'],duration_ms=8000) for s in episode['scenes']]
(job/'narration-plan.json').write_text(json.dumps(plan,ensure_ascii=False))
n=config['narration'];cache=Path(n['runtime'])/'hf_cache'
def snapshot(repo):
    paths=sorted((cache/('models--'+repo)/'snapshots').glob('*'))
    if len(paths)!=1: raise RuntimeError('Ambiguous model snapshot '+repo)
    return paths[0]
env=os.environ.copy()
env.update({'CUDA_VISIBLE_DEVICES':str(gpu),'PYTHONDONTWRITEBYTECODE':'1','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','XDG_CACHE_HOME':str(ROOT/'.cache'),'HF_HOME':str(ROOT/'.cache/huggingface'),'TORCH_HOME':str(ROOT/'.cache/torch'),'NUMBA_CACHE_DIR':str(ROOT/'.cache/numba'),'MPLCONFIGDIR':str(ROOT/'.cache/matplotlib')})
run('narration',[n['python'],ROOT/'capabilities/narration/indextts2.py','--runtime-dir',n['runtime'],'--model-dir',n['models'],'--plan',job/'narration-plan.json','--reference-audio',n['reference'],'--output-dir',job/'audio','--manifest',job/'narration-manifest.json','--w2v-bert-dir',snapshot('facebook--w2v-bert-2.0'),'--maskgct-codec',snapshot('amphion--MaskGCT')/'semantic_codec/model.safetensors','--campplus-checkpoint',snapshot('funasr--campplus')/'campplus_cn_common.bin','--bigvgan-dir',snapshot('nvidia--bigvgan_v2_22khz_80band_256x'),'--emotion-alpha','0.45'],cwd=job,env=env)
lock.close()
manifest=json.loads((job/'narration-manifest.json').read_text())
cursor=0; captions=[]; audio_parts=[]
for scene,segment in zip(episode['scenes'],manifest['segments']):
    voice=segment['raw_duration_seconds'];frames=math.ceil((voice+0.65)*24)
    scene.update(start=cursor,frames=frames)
    chunks=[c for c in re.split(r'[，。？！；]',scene['text']) if c]
    total=sum(len(c) for c in chunks);t=cursor/24+0.12
    for c in chunks:
        dur=(voice-0.15)*len(c)/total
        captions.append({'text':c,'start':t,'end':t+dur});t+=dur
    padded=job/'audio'/(scene['id']+'-pad.wav')
    run('pad-'+scene['id'],['ffmpeg','-y','-i',job/'audio'/(scene['id']+'.wav'),'-af','apad','-t',frames/24,'-ar','48000',padded])
    audio_parts.append(padded);cursor+=frames
episode.update(durationInFrames=cursor,captions=captions)
(job/'props.json').write_text(json.dumps(episode,ensure_ascii=False))
(job/'concat.txt').write_text(''.join("file '"+str(p)+"'\n" for p in audio_parts))
run('concat',['ffmpeg','-y','-f','concat','-safe','0','-i',job/'concat.txt','-c','copy',job/'narration.wav'])
def timestamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(job/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"]}' for i,c in enumerate(captions)),encoding='utf-8')
renderer=ROOT/'renderers/remotion'
remotion=renderer/'node_modules/.bin/remotion'
entry=renderer/'src/EarlyPregnancy.jsx'
run('preview-render',[remotion,'render',entry,'EarlyPregnancy',job/'preview-visual.mp4','--props',job/'props.json','--scale','0.5','--concurrency','3','--codec','h264'],cwd=renderer)
run('preview-mix',['ffmpeg','-y','-i',job/'preview-visual.mp4','-i',job/'narration.wav','-map','0:v','-map','1:a','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','2','-c:a','aac','-movflags','+faststart',job/'preview.mp4'])
run('contact-sheet',['ffmpeg','-y','-i',job/'preview.mp4','-vf',f'fps=13/{cursor/24},scale=216:384,tile=5x3','-frames:v','1',job/'contact-sheet.jpg'])
print('PREVIEW_READY '+str(job),flush=True)
(job/'status.json').write_text(json.dumps({'stage':'preview_ready','run':str(job)}))
