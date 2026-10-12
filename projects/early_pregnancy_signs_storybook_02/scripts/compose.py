"""Server-only new episode composition, sound reuse verification, QA and delivery."""
import hashlib,json,subprocess,sys,time,uuid,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1]
assert str(ROOT)=='/home/ly/shortvideo','Only render on 220'
props=json.loads((P/'timeline.json').read_text());clips=json.loads((P/'review/h3-clips.json').read_text());plan=json.loads((P/'shots.plan.json').read_text())
assert plan['status']=='production_approved'
for s in props['scenes']:
 x=clips[s['shot_id']];assert x['accepted'] is True,s['shot_id'];assert hashlib.sha256((ROOT/x['clip']).read_bytes()).hexdigest()==x['sha256']
job=ROOT/'runs'/('storybook-compose-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir();(P/'review/latest-compose.txt').write_text(str(job))
def run(stage,cmd,**kw):
 print(stage,flush=True)
 with (job/(stage+'.log')).open('w') as f:subprocess.run([str(x) for x in cmd],stdout=f,stderr=subprocess.STDOUT,check=True,**kw)
renderer=ROOT/'renderers/remotion';base='storybook-episodes/'+job.name;assets=renderer/'public'/base;assets.mkdir(parents=True)
shutil.copy2(P/plan['shots'][0]['reference_image'],assets/'cover-source.png')
for s in props['scenes']:
 src=ROOT/clips[s['shot_id']]['clip']
 assert clips[s['shot_id']]['frames']>=s['frames'], 'Insufficient clip duration'
 run('prepare-'+s['shot_id'],['ffmpeg','-y','-i',src,'-an','-vf','fps=24,format=yuv420p','-frames:v',s['frames'],'-c:v','libx264','-crf','17','-preset','fast',assets/f"shot_{s['shot_id']}.mp4"])
props['assetBase']=base;(job/'props.json').write_text(json.dumps(props,ensure_ascii=False,indent=2));mix=ROOT/props['mix_path'];assert mix.exists()
(job/'audio-source.json').write_text(json.dumps({'source':str(mix.relative_to(ROOT)),'sha256':hashlib.sha256(mix.read_bytes()).hexdigest(),'narration':'Complete IndexTTS2 scene WAVs reconstructed to the approved scene starts; see audio-qa.json','music':'Original light plucked instrumental, 104 BPM, synthesized on 220','scope':'internal_review_voice_rights_unverified'},ensure_ascii=False,indent=2))
binary=renderer/'node_modules/.bin/remotion';entry=renderer/'src/StorybookExplainer.jsx';duration=props['durationInFrames']/24
run('preview-render',[binary,'render',entry,'StorybookExplainer',job/'preview-visual.mp4','--props',job/'props.json','--scale','.5','--concurrency','3','--codec','h264'],cwd=renderer)
run('preview-mix',['ffmpeg','-y','-i',job/'preview-visual.mp4','-i',mix,'-c:v','copy','-c:a','aac','-t',duration,'-movflags','+faststart',job/'preview.mp4'])
for i,s in enumerate(props['scenes']):
 run(f'frame-{i:02}',['ffmpeg','-y','-ss',(s['start']+s['frames']*.45)/24,'-i',job/'preview.mp4','-frames:v','1','-vf','scale=270:480',job/f'frame-{i:02}.png'])
run('contact',['ffmpeg','-y','-framerate','1','-i',job/'frame-%02d.png','-vf','tile=5x3:color=0xfff4de','-frames:v','1',job/'contact-sheet.png'])
print('PREVIEW_READY '+str(job),flush=True)
