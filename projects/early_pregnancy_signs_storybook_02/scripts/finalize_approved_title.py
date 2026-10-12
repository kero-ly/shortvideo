"""220-only final delivery of the user-selected fused subtitles and outlined title."""
import hashlib,json,shutil,subprocess,time,uuid
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1]
assert str(ROOT)=='/home/ly/shortvideo'
source=ROOT/'runs/storybook-title-20261013-080452-b41f'
job=ROOT/'runs'/('storybook-final-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir()
print('JOB '+str(job),flush=True)
props=json.loads((source/'props.json').read_text());props['deliveryVersion']='storybook-v4-fused-outlined-title'
(job/'props.json').write_text(json.dumps(props,ensure_ascii=False,indent=2))
(job/'visual-review.json').write_text(json.dumps({'accepted':True,'source_review':str(source.relative_to(ROOT)),'basis':'User requested continue completion after fused-caption, bright-yellow title and outlined-title reviews.','full_human_playback':False,'human_listening':False},ensure_ascii=False,indent=2))
shutil.copy2(ROOT/'runs/storybook-compose-20261013-065713-485f/audio-source.json',job/'audio-source.json')
subprocess.run(['uv','run','python',str(P/'scripts/finalize.py'),str(job)],cwd=ROOT,check=True)
dest=ROOT/'deliveries'/job.name
for name in ['caption-audit.json','subtitles.srt']:shutil.copy2(source/name,dest/name)
page=(dest/'index.html').read_text().replace('已修复结尾旁白，加入原创轻快配乐，增大字幕；底部旁白字幕恢复深棕字和白色底，不加投影；左上角提示无背景底。','已修复结尾旁白并加入原创轻快配乐。下方统一融合主题标签与完整旁白字幕，保持深棕字和白色底、不加投影；上方亮黄色大标题配深棕描边，贯穿全片；左上角提示无背景底。')
(dest/'index.html').write_text(page)
qa=json.loads((dest/'qa.json').read_text());qa['caption_audit']='caption-audit.json';qa['title']={'text':props['persistentTitle'],'color':'#ffff00','font_size':90,'stroke':'6px #54351f','interval_frames':[0,1910]};qa['caption_timing_unchanged']=props['captions']==json.loads((source/'props.json').read_text())['captions'];qa['source_review']=str(source.relative_to(ROOT));(dest/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
manifest={'version':props['deliveryVersion'],'host':'220','run':str(job.relative_to(ROOT)),'source_review':str(source.relative_to(ROOT)),'duration_seconds':props['durationInFrames']/24,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(dest.iterdir()) if f.is_file() and f.name!='manifest.json'}}
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('FINAL_READY '+str(dest),flush=True)
