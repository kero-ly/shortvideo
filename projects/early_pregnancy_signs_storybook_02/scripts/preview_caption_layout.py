"""Render each shot's proposed single lower subtitle region for visual review on 220."""
import json,subprocess,time,uuid,hashlib,html
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo'
job=ROOT/'runs'/('storybook-layout-preview-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir()
props=json.loads((ROOT/'runs/storybook-caption-restored-20261013-072152-12b7/props.json').read_text());props['subtitleLayout']='lower-single';(job/'props.json').write_text(json.dumps(props,ensure_ascii=False,indent=2))
renderer=ROOT/'renderers/remotion';rows=[]
for s in props['scenes']:
 candidates=[c for c in props['captions'] if s['start']/24<=c['start']<(s['start']+s['frames'])/24]
 c=min(candidates,key=lambda c:abs((c['start']+c['end'])/2-(s['start']+s['frames']*.45)/24));frame=round((c['start']+c['end'])*12)
 name=f"shot-{s['shot_id']}.png";print('render '+name,flush=True)
 with (job/(name+'.log')).open('w') as log:subprocess.run([str(renderer/'node_modules/.bin/remotion'),'still','src/StorybookExplainer.jsx','StorybookExplainer',str(job/name),'--props',str(job/'props.json'),'--frame',str(frame),'--scale','.5'],cwd=renderer,stdout=log,stderr=subprocess.STDOUT,check=True)
 rows.append({'shot_id':s['shot_id'],'title':s['title'],'caption':c['text'],'frame':frame,'image':name,'sha256':hashlib.sha256((job/name).read_bytes()).hexdigest()})
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>下方统一字幕 · 13镜预览</title><style>body{font:16px system-ui;background:#fff4de;color:#684630;margin:0}main{max-width:1180px;margin:auto;padding:22px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}img{width:100%;border-radius:12px}p{line-height:1.7}a{color:inherit}</style><main><h1>下方统一字幕 · 全13镜预览</h1><p>上方重复标题、说明和信息卡已合并为下方逐句字幕；旁白文案与关键事实不变。左上角提示移至距左28px、距顶32px，无背景底。下方字幕保持62px深棕字与浅白底，底边距280px。这是实际渲染静帧，供检查位置与遮挡。</p><div class="grid">'''+''.join(f'<section id="shot-{r["shot_id"]}"><h2>{r["shot_id"]} · {html.escape(r["title"])}</h2><a href="{r["image"]}"><img src="{r["image"]}" alt="{html.escape(r["caption"])}"></a><p>{html.escape(r["caption"])}</p></section>' for r in rows)+'</div></main></html>'
(job/'index.html').write_text(page);(job/'manifest.json').write_text(json.dumps({'status':'layout_preview_pending_user_review','subtitleLayout':'lower-single','frames':rows},ensure_ascii=False,indent=2));(P/'review/latest-caption-preview.txt').write_text(str(job));print('READY '+str(job),flush=True)
