import json,subprocess,hashlib,shutil,html,math
from pathlib import Path
ROOT=Path('/home/ly/shortvideo');E=ROOT/'projects/heart_circulation_mechanism_04';RUN=E/'runs/20261013-heart-v4';D=E/'deliveries/20261013-heart-v4';D.mkdir(parents=True,exist_ok=True)
def run(args):return subprocess.run(args,text=True,capture_output=True,check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=RUN/'heart-circulation.mp4';probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(v)]).stdout);(RUN/'ffprobe.json').write_text(json.dumps(probe,indent=2))
result=run(['ffmpeg','-v','error','-i',str(v),'-f','null','-']);(RUN/'decode.log').write_text(result.stderr)
black=run(['ffmpeg','-hide_banner','-i',str(v),'-vf','blackdetect=d=0.15:pix_th=0.08','-an','-f','null','-']);(RUN/'blackdetect.log').write_text(black.stderr)
loud=run(['ffmpeg','-hide_banner','-i',str(v),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']);(RUN/'loudness.log').write_text(loud.stderr);metrics=json.loads(loud.stderr[loud.stderr.rfind('{'):]);(RUN/'loudness.json').write_text(json.dumps(metrics,indent=2))
props=json.loads((RUN/'props.json').read_text());shots=props['shots'];vs=next(x for x in probe['streams'] if x['codec_type']=='video');au=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert vs['width']==1080 and vs['height']==1920 and vs['pix_fmt']=='yuv420p' and vs['r_frame_rate']=='30/1' and int(vs['nb_frames'])==props['totalFrames']
assert au['codec_name']=='aac' and au['sample_rate']=='48000' and au['channels']==2
assert -19<=float(metrics['input_i'])<=-13 and float(metrics['input_tp'])<=-1
assert 'black_start:' not in black.stderr
end=shots[-1]['audioStart']+shots[-1]['audioDuration'];tail=props['totalFrames']/30-end;assert tail>=.8
for s in shots:assert s['audioStart']+s['audioDuration']<=(s['start']+s['frames'])/30
# All shot start/middle/end samples are extracted on the production host.
for i,s in enumerate(shots):
 for label,frame in [('start',s['start']),('middle',s['start']+s['frames']//2),('end',s['start']+s['frames']-1)]:
  run(['ffmpeg','-y','-v','error','-ss',str(frame/30),'-i',str(v),'-frames:v','1','-vf','scale=360:640',str(RUN/f'qa-{i+1}-{label}.png')])
run(['ffmpeg','-y','-v','error','-i',str(v),'-vf','fps=1/1.5,scale=180:320,tile=5x3','-frames:v','1',str(RUN/'contact-sheet.png')])
def ts(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
cues=[dict(shot_id=s['id'],source_indices=[i],start=s['audioStart'],end=s['audioStart']+s['audioDuration'],text=s['text'],context='One WAV per sentence; measured container duration, not word-aligned') for i,s in enumerate(shots)]
(D/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
(D/'alignment.json').write_text(json.dumps(dict(level='sentence_wav',narration_sha256=sha(E/'runs/20261013-heart-v1/narration.wav'),cues=cues),ensure_ascii=False,indent=2))
qa=dict(technical='passed',resolution='1080x1920 native vector rasterization',frames=props['totalFrames'],fps=30,duration_seconds=props['totalFrames']/30,loudness=metrics,tail_seconds=tail,decode='all frames decoded without error',black_frames='none >= 0.15 seconds',audio='AAC 48kHz stereo',caption_timing='sentence-level measured source WAV, not ASR/word-level; burned-in sentence shown during its shot',visual='See review/QA.md for actual visual inspection',full_playback='pending browser playback check',actual_listening='pending; automated waveform metrics do not constitute listening',release='internal review; no publication approval; external reference voice rights not independently confirmed')
(D/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
for name in ['heart-circulation.mp4','props.json','ffprobe.json','loudness.json','contact-sheet.png']+[f'shot{i:02}.png' for i in range(1,6)]:shutil.copy2(RUN/name,D/name)
shutil.copy2(RUN/'shot01.png',D/'cover.png')
shutil.copy2(E/'runs/20261013-heart-v1/preview.mp4',D/'preview-v1.mp4')
shutil.copy2(E/'runs/20261013-heart-v1/tts-manifest.json',D/'tts-manifest.json')
(D/'sources.json').write_text(json.dumps(dict(facts=[{'url':'https://www.nhlbi.nih.gov/health/heart/blood-flow','retrieved':'2026-10-13','use':'Right ventricle→lungs→left atrium/ventricle→body; oxygen exchange in lungs'}],art='Original SVG code, no Douyin pixels or music reused',audio='IndexTTS2; configured reference teacher_reference_24k.wav; internal review',music=None,lineage='original SVG source → deterministic shot frames → v1/v2/v4 render → narration mux; source hashes in production-plan'),ensure_ascii=False,indent=2))
cards=''.join(f'<article id="shot{i+1}"><a href="shot{i+1:02}.png"><img src="shot{i+1:02}.png" alt="镜头{i+1}"></a><div><h2>镜头 {i+1:02}</h2><p>{html.escape(s["text"])}</p><p>{s["start"]/30:.2f}–{(s["start"]+s["frames"])/30:.2f} 秒</p><button onclick="seek({s["start"]/30})">播放这段</button><p>{["心脏局部形变、手臂摆动，逐渐推近","连续推近肺循环；肺呼吸，氧气进入","连续下移到体循环；血流向组织","血管近景；分层红细胞前进，氧气向组织移动","回到全景；两条循环持续运转"][i]}</p></div></article>' for i,s in enumerate(shots))
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>心脏的小小运输队 · v4</title><style>body{margin:0;background:#f6eddc;color:#593a2f;font:17px system-ui}main{max-width:1050px;margin:auto;padding:28px}h1{font-size:34px}video{width:min(100%,380px);max-height:78vh;background:#222;border-radius:18px}header{text-align:center}a{color:#984b32}article{display:flex;gap:28px;background:#fff9ed;padding:20px;border-radius:18px;margin:24px 0}article img{width:200px;max-width:38vw;border-radius:12px}button{padding:12px 20px;border:0;background:#653c32;color:white;border-radius:10px;cursor:pointer}p{line-height:1.7}summary{cursor:pointer}footer{font-size:14px}</style><main><header><h1>心脏的小小运输队</h1><p>23 秒 · 原创二维机制动画 · 第四版</p><video id="v" controls playsinline preload="metadata" poster="cover.png" src="heart-circulation.mp4"></video><p><a href="heart-circulation.mp4">下载 1080p 视频</a> · <a href="subtitles.srt">字幕</a> · <a href="qa.json">技术检查</a></p></header><p>已优化：血流标签移出管壁、肺循环到体循环连续运镜、肺部换气与组织送氧、心脏局部收缩、图例独立底栏。颜色及比例为机制示意；未表达四腔、瓣膜等完整解剖结构。</p><details><summary>查看第一版对比</summary><video controls preload="none" src="preview-v1.mp4"></video></details>'''+cards+'''<footer><p>事实依据：<a href="https://www.nhlbi.nih.gov/health/heart/blood-flow">NIH/NHLBI · How Blood Flows through the Heart</a>。美术为原创 SVG；未复用抖音原图或音乐。当前为内部审阅样片，实际听审仍待确认。</p></footer></main><script>function seek(t){let v=document.getElementById('v');v.currentTime=t;v.play();v.scrollIntoView({behavior:'smooth',block:'center'})}</script></html>'''
(D/'index.html').write_text(page)
manifest={str(p.relative_to(D)):dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(D.iterdir()) if p.is_file() and p.name!='manifest.json'};(D/'manifest.json').write_text(json.dumps(manifest,indent=2))
(E/'review').mkdir(exist_ok=True)
for name in ['manifest.json','qa.json','sources.json','alignment.json','props.json']:
 shutil.copy2(D/name,E/'review'/('v4-'+name))
print(json.dumps(qa,ensure_ascii=False,indent=2));print(D)
