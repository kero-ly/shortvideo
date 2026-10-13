import json, os, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; E=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT)); from pipeline.gpu_lock import acquire
job=E/'runs'/('tts-v1-'+time.strftime('%Y%m%d-%H%M%S')); job.mkdir(parents=True,exist_ok=False)
texts=['愿佛光照耀你。','平安喜乐。','诸事顺遂。','家旺，财旺，子孙旺。','愿你阖家幸福。','岁岁安康。']
plan=[dict(id=f'phrase-{i+1:02}',text=t,duration_ms=2500) for i,t in enumerate(texts)]
(job/'tts-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2))
n=json.loads((ROOT/'configs/resources.json').read_text())['narration']; cache=Path(n['runtime'])/'hf_cache'
def snap(repo): return next((cache/('models--'+repo)/'snapshots').iterdir())
env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES='7',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',XDG_CACHE_HOME=str(ROOT/'.cache'),HF_HOME=str(ROOT/'.cache/huggingface'),TORCH_HOME=str(ROOT/'.cache/torch'),NUMBA_CACHE_DIR=str(ROOT/'.cache/numba'),MPLCONFIGDIR=str(ROOT/'.cache/matplotlib'))
lock=acquire(ROOT/'.runtime/gpu-job.lock')
free=int(subprocess.check_output(['nvidia-smi','--id=7','--query-gpu=memory.free','--format=csv,noheader,nounits']).strip());assert free>=12000,free
cmd=[n['python'],str(ROOT/'capabilities/narration/indextts2.py'),'--runtime-dir',n['runtime'],'--model-dir',n['models'],'--plan',str(job/'tts-plan.json'),'--reference-audio',n['reference'],'--output-dir',str(job/'audio'),'--manifest',str(job/'tts-manifest.json'),'--w2v-bert-dir',str(snap('facebook--w2v-bert-2.0')),'--maskgct-codec',str(snap('amphion--MaskGCT')/'semantic_codec/model.safetensors'),'--campplus-checkpoint',str(snap('funasr--campplus')/'campplus_cn_common.bin'),'--bigvgan-dir',str(snap('nvidia--bigvgan_v2_22khz_80band_256x')),'--emotion-alpha','0.45']
print('TTS_JOB '+str(job),flush=True)
subprocess.run(cmd,cwd=job,env=env,check=True)
print('TTS_COMPLETE '+str(job),flush=True)
