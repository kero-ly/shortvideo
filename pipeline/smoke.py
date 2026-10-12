#!/usr/bin/env python3
"""Generate real speech + animation, mux, inspect and deliver a fresh test video."""
import argparse, hashlib, json, math, os, re, shutil, subprocess, sys, time, uuid, wave
from pathlib import Path
from gpu_lock import acquire
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--gpu',type=int,required=True)
    args=parser.parse_args()
    gpu_lock=acquire(ROOT/'.runtime/gpu-job.lock')
    config=json.loads((ROOT/'configs/resources.json').read_text())
    job=ROOT/'runs'/('smoke-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6])
    job.mkdir(parents=True)
    status={'job':str(job),'stage':'starting','status':'running'}
    def save(): (job/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False))
    def run(stage,cmd,**kwargs):
        status['stage']=stage;save();print(stage,flush=True)
        with (job/(stage+'.log')).open('w') as log:
            subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True,**kwargs)
    save()
    try:
        rows=subprocess.check_output(['nvidia-smi','--query-gpu=index,memory.free,utilization.gpu','--format=csv,noheader,nounits'],text=True)
        selected=[list(map(int,r.split(','))) for r in rows.splitlines() if int(r.split(',')[0])==args.gpu]
        if not selected or selected[0][1]<12000 or selected[0][2]>10:
            raise RuntimeError('Selected GPU is not currently sufficiently idle/free; choose another GPU')
        (job/'gpu-before.txt').write_text(rows)
        text='画面、旁白和字幕，正在同一条时间线上运行。'
        plan=[{'id':'narration','text':text,'duration_ms':6000}]
        (job/'narration-plan.json').write_text(json.dumps(plan,ensure_ascii=False))
        n=config['narration']; cache=Path(n['runtime'])/'hf_cache'
        def snapshot(repo):
            paths=sorted((cache/('models--'+repo)/'snapshots').glob('*'))
            if len(paths)!=1: raise RuntimeError('Expected exactly one configured snapshot for '+repo)
            return paths[0]
        env=os.environ.copy()
        env.update({'CUDA_VISIBLE_DEVICES':str(args.gpu),'PYTHONDONTWRITEBYTECODE':'1','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','XDG_CACHE_HOME':str(ROOT/'.cache'),'HF_HOME':str(ROOT/'.cache/huggingface'),'TORCH_HOME':str(ROOT/'.cache/torch'),'NUMBA_CACHE_DIR':str(ROOT/'.cache/numba'),'MPLCONFIGDIR':str(ROOT/'.cache/matplotlib')})
        run('narration',[n['python'],str(ROOT/'capabilities/narration/indextts2.py'),'--runtime-dir',n['runtime'],'--model-dir',n['models'],'--plan',str(job/'narration-plan.json'),'--reference-audio',n['reference'],'--output-dir',str(job),'--manifest',str(job/'narration-manifest.json'),'--w2v-bert-dir',str(snapshot('facebook--w2v-bert-2.0')),'--maskgct-codec',str(snapshot('amphion--MaskGCT')/'semantic_codec/model.safetensors'),'--campplus-checkpoint',str(snapshot('funasr--campplus')/'campplus_cn_common.bin'),'--bigvgan-dir',str(snapshot('nvidia--bigvgan_v2_22khz_80band_256x')),'--emotion-alpha',str(n['emotion_alpha'])],cwd=job,env=env)
        with wave.open(str(job/'narration.wav')) as wav: voice_seconds=wav.getnframes()/wav.getframerate()
        frames=max(144,math.ceil((voice_seconds+0.6)*24)); duration=frames/24
        (job/'props.json').write_text(json.dumps({'durationInFrames':frames,'caption':text},ensure_ascii=False))
        renderer=ROOT/'renderers/remotion'
        run('render',[str(renderer/'node_modules/.bin/remotion'),'render','src/index.jsx','FactorySmoke',str(job/'visual.mp4'),'--props',str(job/'props.json'),'--codec','h264','--concurrency','2'],cwd=renderer)
        ffmpeg=config['tools']['ffmpeg'];ffprobe=config['tools']['ffprobe']
        run('mix',[ffmpeg,'-hide_banner','-y','-i',str(job/'visual.mp4'),'-i',str(job/'narration.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11,apad','-ar','48000','-ac','2','-c:a','aac','-t',str(duration),'-movflags','+faststart',str(job/'final.mp4')])
        run('decode',[ffmpeg,'-v','error','-xerror','-i',str(job/'final.mp4'),'-f','null','-'])
        probe=json.loads(subprocess.check_output([ffprobe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(job/'final.mp4')],text=True))
        (job/'probe.json').write_text(json.dumps(probe,indent=2))
        video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
        run('audio-level',[ffmpeg,'-hide_banner','-i',str(job/'final.mp4'),'-vn','-af','volumedetect','-f','null','-'])
        log=(job/'audio-level.log').read_text();m=re.search(r'mean_volume: ([-\d.]+) dB',log)
        checks={'size':(video['width'],video['height'])==(540,960),'fps':video['avg_frame_rate']=='24/1','frames':int(video['nb_read_frames'])==frames,'audio_rate':audio['sample_rate']=='48000','audio_channels':audio['channels']==2,'duration':abs(float(probe['format']['duration'])-duration)<0.15,'audible':bool(m) and -45<float(m.group(1))<-3,'full_decode':True}
        run('contact-sheet',[ffmpeg,'-hide_banner','-y','-i',str(job/'final.mp4'),'-vf',f'fps=3/{duration},scale=270:480,tile=3x1','-frames:v','1',str(job/'contact-sheet.jpg')])
        report={'checks':checks,'passed':all(checks.values()),'voice_seconds':voice_seconds,'duration_seconds':duration,'frames':frames,'sha256':hashlib.sha256((job/'final.mp4').read_bytes()).hexdigest(),'limits':['Infrastructure smoke only; no ASR verification or production style approval','H3, Music3, Blender, Godot and FreeCAD are not exercised by this smoke']}
        (job/'qa.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
        if not report['passed']: raise RuntimeError('QA failed; see qa.json')
        destination=ROOT/'deliveries'/job.name;destination.mkdir()
        for name in ['final.mp4','contact-sheet.jpg','qa.json','narration-manifest.json']: shutil.copy2(job/name,destination/name)
        status.update(status='passed',stage='complete',delivery=str(destination));save()
        print(json.dumps(status,ensure_ascii=False),flush=True)
    except Exception as e:
        status.update(status='failed',error=str(e));save();print(json.dumps(status,ensure_ascii=False),flush=True);raise

if __name__=='__main__': main()
