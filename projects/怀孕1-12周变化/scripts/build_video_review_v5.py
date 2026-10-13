# -*- coding: utf-8 -*-
import json,html
from pathlib import Path
P=Path(__file__).resolve().parents[1];t=json.loads((P/'timeline/audio-v5.json').read_text());c=json.loads((P/'timeline/captions-v5.json').read_text());latest=P/'review/latest-delivery-v5.txt';delivery=latest.read_text().strip() if latest.exists() else None;compose=(P/'review/latest-compose-v5.txt').read_text().strip();video='../'+delivery+'/怀孕1-12周变化-v5.mp4' if delivery else '../'+compose+'/preview.mp4'
parts=['<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>怀孕1—12周变化｜成片审阅 v5</title><style>body{background:#faf4e8;color:#344338;font-family:system-ui;max-width:1000px;margin:auto;padding:24px}video{max-height:75vh;width:100%;background:#efe7d7}button,a{color:#346451}article{background:white;border-radius:16px;padding:18px;margin:14px 0}button{padding:8px 14px;border:1px solid #c9d5c4;border-radius:12px;background:#f5f8ef}small{color:#65705e}</style><h1>怀孕 1—12 周变化</h1><p>沿用你提供的母版与已批准的16镜头分镜。v5：第二周配音读音修正；音乐提高约6dB；大号黄字描边主标题居中；全部16段口播与字幕已改写，称呼更贴近妈妈的感受，结尾为“给温暖的你”。</p><p><a href="copy-v4.html">完整文案修改对照</a></p><video id="v" controls preload="metadata" src="'+video+'"></video><p><a href="'+video+'" download>下载视频</a> · <a href="../timeline/captions-v5.srt">字幕 SRT</a> · <a href="storyboard-v2.html">已批准分镜</a></p><p><small>画面原生生成576×1024，最终合成1080×1920。完整听审待确认；工厂参考声线的公开使用授权尚无记录。</small></p>']
for s in t['shots']:
 start=s['start']/24;parts.append(f'<article><button onclick="seek({start})">{s["id"]} · {html.escape(s["phase"])} · {start:.1f}秒</button><p>{html.escape(s["text"])}</p>')
 for x in c['cues']:
  if x['shot_id']==s['id']:parts.append(f'<p><button onclick="seek({x["start"]})">{x["start"]:.2f}s</button> {html.escape(x["text"])}</p>')
 parts.append('</article>')
parts.append('<script>function seek(t){const v=document.getElementById("v");v.currentTime=t;v.play()}</script></html>');(P/'review/video-v5.html').write_text(''.join(parts))
