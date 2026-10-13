import json,hashlib,shutil,subprocess,time,uuid
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo'
t=json.loads((P/'timeline/audio-v2.json').read_text());c=json.loads((P/'timeline/captions-v2.json').read_text());m=json.loads((P/'review/h3-clips-v2.json').read_text());assert c['narration_sha256']==t['narration_sha256']
job=P/'runs'/('compose-v2-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir();(P/'review/latest-compose-v2.txt').write_text(str(job.relative_to(P)))
r=ROOT/'renderers/remotion';base='pregnancy-weeks/'+job.name;assets=r/'public'/base;assets.mkdir(parents=True)
def run(name,args,cwd=None):
 print(name,flush=True)
 with (job/(name+'.log')).open('w') as f:subprocess.run(list(map(str,args)),stdout=f,stderr=subprocess.STDOUT,check=True,cwd=cwd)
for s in t['shots']:
 x=m[s['id']];assert x['accepted'];src=P/x['clip'];assert hashlib.sha256(src.read_bytes()).hexdigest()==x['sha256'];assert x['frames']>=s['frames']
 run('prepare-'+s['id'],['ffmpeg','-y','-i',src,'-an','-vf','fps=24,format=yuv420p','-frames:v',s['frames'],'-c:v','libx264','-crf','17','-preset','fast',assets/(s['id']+'.mp4')])
props=dict(t,cues=c['cues'],assetBase=base);(job/'props.json').write_text(json.dumps(props,ensure_ascii=False,indent=2));voice=P/t['narration'];assert hashlib.sha256(voice.read_bytes()).hexdigest()==t['narration_sha256']
run('normalize',['ffmpeg','-y','-i',voice,'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','2',job/'mix.wav'])
entry=P/'scripts/PregnancyWeeks.jsx';shutil.copy2(entry,r/'src/PregnancyWeeksEpisode.jsx');binary=r/'node_modules/.bin/remotion'
run('preview-render',[binary,'render',r/'src/PregnancyWeeksEpisode.jsx','PregnancyWeeks',job/'preview-visual.mp4','--props',job/'props.json','--scale','.5','--concurrency','3','--codec','h264'],r)
run('preview-mux',['ffmpeg','-y','-i',job/'preview-visual.mp4','-i',job/'mix.wav','-c:v','copy','-c:a','aac','-b:a','192k','-t',t['duration_seconds'],'-movflags','+faststart',job/'preview.mp4'])
for i,s in enumerate(t['shots']):run('frame-'+str(i),['ffmpeg','-y','-ss',(s['start']+s['frames']*.5)/24,'-i',job/'preview.mp4','-frames:v','1','-vf','scale=270:480',job/f'frame-{i:02}.png'])
run('contact',['ffmpeg','-y','-framerate','1','-i',job/'frame-%02d.png','-vf','tile=4x4','-frames:v','1',job/'contact.png'])
print('PREVIEW_READY '+str(job),flush=True)
