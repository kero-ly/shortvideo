"""Compose only actual H3 clips with locked captions and existing review narration."""
import hashlib,json,subprocess,time,uuid,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
props=json.loads((P.parent/'aligned-props.json').read_text());clips=json.loads((P/'review/h3-clips.json').read_text())
assert all(f'shot_{i:02}' in clips for i in range(1,14)),'All 13 H3 clips are required'
assert all(clips[f'shot_{i:02}'].get('accepted') is True for i in range(1,14)),'Every H3 clip must pass visual review before composition'
job=ROOT/'runs'/('h3-compose-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir(parents=True)
(P/'review/latest-compose.txt').write_text(str(job))
def run(stage,cmd,**kw):
 print(stage,flush=True)
 with (job/(stage+'.log')).open('w') as f:subprocess.run([str(x) for x in cmd],stdout=f,stderr=subprocess.STDOUT,check=True,**kw)
renderer=ROOT/'renderers/remotion';assetbase='h3-episodes/'+job.name;assets=renderer/'public'/assetbase;assets.mkdir(parents=True)
shutil.copy2(P/'references/shots/openlux_shot_01_v1.png',assets/'cover-source.png')
for i,scene in enumerate(props['scenes'],1):
 src=ROOT/clips[f'shot_{i:02}']['clip'];target=assets/f'shot_{i:02}.mp4'
 run(f'prepare-{i:02}',['ffmpeg','-y','-i',src,'-an','-vf','scale=576:1024:force_original_aspect_ratio=increase,crop=576:1024,fps=24,tpad=stop_mode=clone:stop_duration=3,format=yuv420p','-frames:v',scene['frames'],'-c:v','libx264','-crf','17','-preset','fast',target])
props['assetBase']=assetbase;(job/'props.json').write_text(json.dumps(props,ensure_ascii=False,indent=2))
bin=renderer/'node_modules/.bin/remotion';entry=renderer/'src/EarlyPregnancyH3.jsx'
run('preview-render',[bin,'render',entry,'EarlyPregnancyH3',job/'preview-visual.mp4','--props',job/'props.json','--scale','.5','--concurrency','3','--codec','h264'],cwd=renderer)
mix=ROOT/'runs/early-pregnancy-20261013-010143-e9a8/mix.wav'
assert mix.exists(),'Review narration/music mix missing'
run('preview-mix',['ffmpeg','-y','-i',job/'preview-visual.mp4','-i',mix,'-c:v','copy','-c:a','aac','-t',props['durationInFrames']/24,'-movflags','+faststart',job/'preview.mp4'])
for i,s in enumerate(props['scenes']):
 run(f'frame-{i:02}',['ffmpeg','-y','-ss',(s['start']+s['frames']*.5)/24,'-i',job/'preview.mp4','-frames:v','1','-vf','scale=270:480',job/f'frame-{i:02}.png'])
run('contact',['ffmpeg','-y','-framerate','1','-i',job/'frame-%02d.png','-vf','tile=5x3:color=0xfaf5eb','-frames:v','1',job/'contact-sheet.png'])
print('PREVIEW_READY '+str(job),flush=True)
