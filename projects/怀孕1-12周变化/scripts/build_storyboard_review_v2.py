"""Create complete image-and-script review page from actual v2 reference frames."""
from pathlib import Path
import json,html,hashlib
from urllib.parse import quote
from PIL import Image,ImageOps,ImageDraw
P=Path(__file__).resolve().parents[1]
esc=html.escape
s=json.loads((P/'storyboard/draft-v2.json').read_text())
items=[];missing=[];inventory=[]
for i,x in enumerate(s['shots'],1):
 image=x.get('reference_frame');exists=bool(image and (P/image).exists())
 if not exists:missing.append(x['id'])
 if exists:
  size=list(Image.open(P/image).size);digest=hashlib.sha256((P/image).read_bytes()).hexdigest();assert digest==x['reference_frame_sha256']
  inventory.append({'shot_id':x['id'],'path':image,'sha256':digest,'size':size,'input':x['reference_source'],'input_sha256':x['reference_input_sha256'],'prompt':f"prompts/shots/{x['id']}-image-v2.txt",'motion_prompt':f"prompts/shots/{x['id']}-motion-v2.txt",'generation_evidence':x['generation_evidence'],'review_status':x.get('visual_review_status','pending')})
  src='../'+quote(image,safe='/');visual=f'<a href="{src}" target="_blank"><img src="{src}" alt="第{i}镜实际生成场景首帧"></a><span>实际生成首帧 · {size[0]}×{size[1]} · 点击原图放大</span>'
 else:visual='<div class="placeholder">该镜首帧未完成</div>'
 original='../'+quote(x['reference_source'],safe='/')
 items.append(f'''<article id="{x['id']}"><div class="visual">{visual}</div><div class="copy"><small>{i:02d} / 16 · 预计{x['estimated_seconds']}秒</small><h2>{esc(x['phase'])}</h2><p class="voice">{esc(x['narration'])}</p><p><b>屏幕文字</b><br>{esc(x['screen_text'])}</p><p><b>首帧意图</b> {esc(x['frame_plan'])}</p><p><b>动作</b> {esc(x['action'])}</p><p><b>镜头</b> {esc(x['camera'])}</p><p class="muted">OpenLux场景延伸 → 220 H3轻动作 → IndexTTS2独立旁白 → Remotion精准中文 → FFmpeg/QA。计划路线；本期动画/声音尚未制作。</p><a href="{original}" target="_blank">对应用户原始参考</a><details><summary>图像及英文动画提示词</summary><pre>{esc(x['image_prompt'])}\n\n{esc(x['motion_prompt'])}</pre></details></div></article>''')
ready=not missing
status='全套16张实际场景首帧已完成，图文v2待确认。' if ready else '实际场景首帧生成中；缺项：'+', '.join(missing)
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>怀孕1–12周变化 · 全分镜图文v2</title><style>*{box-sizing:border-box}body{margin:0;background:#f7f1e7;color:#2b423d;font:16px/1.75 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}main{max-width:1150px;margin:auto;padding:32px 24px}h1{font-size:38px;line-height:1.3}h2{font-size:25px;margin:4px 0}.intro,.status,article,.notes{background:#fffdf9;border:1px solid #e1d8c9;border-radius:18px;padding:24px;margin:24px 0}.status{background:#eef2e5}article{display:grid;grid-template-columns:45% 1fr;gap:28px;scroll-margin-top:16px}.visual img{width:100%;display:block;border-radius:12px}.visual span,small,.muted{font-size:13px;color:#74786b}.voice{font-size:21px;font-weight:600;border-left:3px solid #bd8269;padding-left:14px}p{margin:12px 0}b,a{color:#537b68}pre{white-space:pre-wrap;font:13px/1.6 monospace}nav{display:flex;flex-wrap:wrap;gap:10px}nav a{border-radius:20px;background:#e9e3d6;padding:5px 12px;text-decoration:none}.overview{width:100%}.placeholder{min-height:400px;display:grid;place-items:center;background:#eee6d9}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}@media(max-width:720px){main{padding:16px}article,.grid{grid-template-columns:1fr}h1{font-size:29px}}</style><main><small>图文版本 v2 · 用户原参考直接延伸 · 非成片</small><h1>怀孕1–12周变化<br>宝宝在长大，妈妈也在努力。</h1><section class="intro"><p>9:16目标成片｜16镜｜估计97秒，真实时长由实际配音决定。</p><p><b>用户选定方向：</b>直接以原始场景图为模板与人物、服装、画风依据，跳过独立母版。已生成的单人母版和设计页不进入本版制作。</p><p><b>传播设计：</b>开头用孕周计算的反常识吸引注意；逐周索引提供收藏价值；妈妈感受建立共鸣；准爸爸清单和结尾提供转发理由。</p></section><section class="status"><b>'''+esc(status)+'''</b><p>本页全部按镜号列出实际首帧、中文旁白、屏幕文字、时长、动作、运镜及工具路线。首帧中的文字留白用于后期精确排版；当前图片不含最终字幕。</p><p>图片请求1024×1792，实际尺寸逐镜显示。最终1080×1920合成输出；H3既有原生案例为576×1024/24fps，当前镜头尚未实测。没有TTS、H3或视频渲染任务被提交。</p></section>'''
if ready:
 page+='<section class="notes"><h2>完整首帧总览</h2><a href="../runs/storyboard-review-v2/contact-sheet.jpg"><img class="overview" src="../runs/storyboard-review-v2/contact-sheet.jpg" alt="16镜实际首帧总览"></a></section>'
page+='<nav>'+''.join(f'<a href="#{x["id"]}">{i:02d} {esc(x["phase"])}</a>' for i,x in enumerate(s['shots'],1))+'</nav>'+''.join(items)+'''<section class="notes"><h2>声音、字幕与验收计划</h2><p>温柔清晰的成年女声，独立旁白，无对口型要求。IndexTTS2参考音频使用范围和实际声线在配音前登记；音乐仅使用来源明确的低音量无歌词素材，否则省略。音频长度与对齐数据完成后再建立字幕时间线。</p><p>一层旁白字幕配简短孕周标题，避免重复信息；避开脸、手及抖音右侧按钮和底部说明区。实际手机尺度静帧检查后提供完整带声样片，再做技术、画面、内容和听审QA。</p><p>用户原图中的胚胎/子宫气泡不作为医学真实性依据；人物动画只做生活动作。受精等必要概念用后期示意点阵/箭头表达，并标“示意，非真实比例”。</p><p><a href="../FACT_CHECK.md">逐镜医学来源</a> · <a href="../PUBLISHING_DRAFT.md">发布文案草案</a> · <a href="../PREPRODUCTION-v2.md">v2方案与用户选择</a></p><p>角色方向已由用户原图指定；本完整图文v2尚未获制作批准。确认图文版本后才进入配音、H3与合成，不另加三镜图片审批。</p></section></main></html>'''
(P/'review/storyboard-v2.html').write_text(page)
(P/'review/reference-frames-v2.json').write_text(json.dumps({'revision':2,'status':'complete_pending_user_approval' if ready else 'partial','missing':missing,'assets':inventory},ensure_ascii=False,indent=2)+'\n')
if ready:
 out=P/'runs/storyboard-review-v2';out.mkdir(parents=True,exist_ok=True)
 sheet=Image.new('RGB',(1280,2480),'#f5eee3');d=ImageDraw.Draw(sheet)
 for i,x in enumerate(s['shots']):
  im=Image.open(P/x['reference_frame']).convert('RGB');im.thumbnail((300,570))
  col=i%4;row=i//4;left=col*320+(320-im.width)//2;top=row*620+35
  sheet.paste(im,(left,top));d.text((col*320+12,row*620+10),f"{i+1:02d} / {x['id']}",fill='#243e35')
 sheet.save(out/'contact-sheet.jpg',quality=93)
 md=['# 怀孕1–12周变化 · 完整图文v2','','用户原始场景图直接延伸；无独立母版。图文v2待批准，未制作音频和视频。','']
 for i,x in enumerate(s['shots'],1):
  md += [f"## {i:02d} · {x['phase']}",'',f"![实际首帧](../{x['reference_frame']})",'',f"旁白：{x['narration']}",'',f"屏幕文字：{x['screen_text']}",'',f"预计{x['estimated_seconds']}秒；动作：{x['action']}；运镜：{x['camera']}。",'',f"来源：{x['reference_source']}。工具：OpenLux → 220 H3 → IndexTTS2 → Remotion/FFmpeg。",'']
 (P/'storyboard/package-v2.md').write_text('\n'.join(md))
print('review written; actual frames',len(inventory),'missing',missing)
