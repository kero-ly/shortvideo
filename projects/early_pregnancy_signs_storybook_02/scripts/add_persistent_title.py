"""220-only full-length review render with an explicit persistent title."""
import hashlib, json, subprocess, time, uuid, shutil
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1]
assert str(ROOT)=='/home/ly/shortvideo'
source=ROOT/'runs/storybook-caption-fusion-20261013-074646-2632'
job=ROOT/'runs'/('storybook-title-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir()
print('JOB '+str(job),flush=True)
props=json.loads((source/'props.json').read_text());props['persistentTitle']='早孕可能出现的 8 个信号'
(job/'props.json').write_text(json.dumps(props,ensure_ascii=False,indent=2))
r=ROOT/'renderers/remotion'
def run(stage,cmd,cwd=None):
 print(stage,flush=True)
 with (job/(stage+'.log')).open('w') as f:subprocess.run(list(map(str,cmd)),cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=True)
run('render',[r/'node_modules/.bin/remotion','render','src/StorybookExplainer.jsx','StorybookExplainer',job/'visual.mp4','--props',job/'props.json','--scale','.5','--concurrency','3','--codec','h264'],r)
run('mix',['ffmpeg','-y','-i',job/'visual.mp4','-i',ROOT/props['mix_path'],'-c:v','copy','-c:a','aac','-t',props['durationInFrames']/24,'-movflags','+faststart',job/'preview.mp4'])
run('decode',['ffmpeg','-v','error','-xerror','-i',job/'preview.mp4','-f','null','-'])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(job/'preview.mp4')]))
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert int(v['nb_read_frames'])==1910 and v['avg_frame_rate']=='24/1'
assert abs(float(a['duration'])-1910/24)<.15
for s in props['scenes']:
 run('frame-'+s['shot_id'],['ffmpeg','-y','-ss',(s['start']+s['frames']*.45)/24,'-i',job/'preview.mp4','-frames:v','1','-vf','scale=270:480',job/('shot-'+s['shot_id']+'.png')])
run('last-frame',['ffmpeg','-y','-ss',1909/24,'-i',job/'preview.mp4','-frames:v','1',job/'last-frame.png'])
run('contact',['ffmpeg','-y','-framerate','1','-start_number','1','-i',job/'shot-%02d.png','-vf','tile=5x3','-frames:v','1',job/'contact.png'])
for name in ['caption-audit.json','subtitles.srt']:shutil.copy2(source/name,job/name)
page=(source/'index.html').read_text().replace('src="preview-fused.mp4"','src="preview.mp4"').replace('字幕融合与语音对齐 · 完整审阅','全片黄字标题 · 视频审阅').replace('下方一个字幕块：短主题标签＋完整语义字幕。','上方黄字标题“早孕可能出现的 8 个信号”贯穿全片。<br>下方一个字幕块：短主题标签＋完整语义字幕。')
(job/'index.html').write_text(page)
qa={'resolution':[v['width'],v['height']],'frames':1910,'fps':24,'duration_seconds':1910/24,'full_decode':True,'title':props['persistentTitle'],'title_style':{'color':'#ffff00','font_size':90,'top':120,'side_inset':20},'title_interval_frames':[0,1910],'narration_and_caption_timing_unchanged':props['captions']==json.loads((source/'props.json').read_text())['captions'],'human_listening':False}
(job/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(job/'manifest.json').write_text(json.dumps({'status':'title_preview_pending_review','source_run':str(source.relative_to(ROOT)),'host':'220','files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in job.iterdir() if f.suffix in ('.json','.mp4','.png','.html','.srt') and f.name!='manifest.json'}},ensure_ascii=False,indent=2))
print('REVIEW_READY '+str(job),flush=True)
