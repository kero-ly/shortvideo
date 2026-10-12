"""Final render after visual preview review, followed by technical QA and delivery."""
import hashlib,json,shutil,subprocess,sys,html
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo';job=Path(sys.argv[1]);props=json.loads((job/'props.json').read_text());duration=props['durationInFrames']/24
assert json.loads((job/'visual-review.json').read_text())['accepted'] is True, 'Preview needs visual review'
approved=json.loads((P/'review/h3-clips.json').read_text())
assert all(approved.get(f'{i:02}',{}).get('accepted') is True for i in range(1,14)),'Unreviewed H3 clip'
def run(stage,cmd,**kw):
 print(stage,flush=True)
 with (job/(stage+'.log')).open('w') as f:subprocess.run([str(x) for x in cmd],stdout=f,stderr=subprocess.STDOUT,check=True,**kw)
renderer=ROOT/'renderers/remotion';binary=renderer/'node_modules/.bin/remotion';entry=renderer/'src/StorybookExplainer.jsx'
run('final-render',[binary,'render',entry,'StorybookExplainer',job/'visual.mp4','--props',job/'props.json','--concurrency','4','--codec','h264','--crf','17'],cwd=renderer)
run('cover',[binary,'still',entry,'StorybookCover',job/'cover.png','--props',job/'props.json'],cwd=renderer)
mix=ROOT/props['mix_path']
vp=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(job/'visual.mp4')],text=True))['streams'][0]
vf='scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p' if vp.get('color_range')=='pc' else 'format=yuv420p'
final=job/'early_pregnancy_storybook.mp4'
run('final-mix',['ffmpeg','-y','-i',job/'visual.mp4','-i',mix,'-map','0:v:0','-map','1:a:0','-vf',vf,'-c:v','libx264','-preset','fast','-crf','18','-threads','8','-color_range','tv','-colorspace','bt709','-c:a','aac','-b:a','192k','-t',duration,'-movflags','+faststart',final])
run('decode',['ffmpeg','-v','error','-xerror','-i',final,'-f','null','-'])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)],text=True))
(job/'probe.json').write_text(json.dumps(probe,indent=2));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
run('black-check',['ffmpeg','-hide_banner','-i',final,'-vf','blackdetect=d=.15:pix_th=.10','-an','-f','null','-'])
run('loudness',['ffmpeg','-hide_banner','-i',final,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-vn','-f','null','-'])
log=(job/'loudness.log').read_text();loud=json.loads(log[log.rfind('{'):])
audioqa=json.loads((ROOT/props['mix_path']).with_name('audio-qa.json').read_text())
checks={'complete_narration':audioqa['complete_narration'],'ending_tail':audioqa['ending_tail_seconds']>=.6,'audio_duration':abs(float(a['duration'])-duration)<.15,'resolution':[v['width'],v['height']]==[1080,1920],'fps':v['avg_frame_rate']=='24/1','frames':int(v['nb_read_frames'])==props['durationInFrames'],'codec':v['codec_name']=='h264' and v['pix_fmt']=='yuv420p','audio':a['codec_name']=='aac' and a['sample_rate']=='48000' and a['channels']==2,'duration':abs(float(probe['format']['duration'])-duration)<.15,'decode':True,'no_black_frames':'black_start:' not in (job/'black-check.log').read_text(),'loudness':-19<float(loud['input_i'])<-13,'peak':float(loud['input_tp'])<=-1,'h3_all_13':len(json.loads((P/'review/h3-clips.json').read_text()))==13}
qa={'passed':all(checks.values()),'checks':checks,'duration_seconds':duration,'loudness':loud,'native_h3_resolution':[576,1024],'delivery_resolution':[1080,1920],'visual_review':'Nine sampled frames per H3 shot and composition contact reviewed; no full human playback or listening claimed','voice':'Existing internal review narration; production usage rights of source voice not verified','sha256':hashlib.sha256(final.read_bytes()).hexdigest()}
(job/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
assert qa['passed'],checks
for i,s in enumerate(props['scenes']):
 run(f'final-frame-{i:02}',['ffmpeg','-y','-ss',(s['start']+s['frames']*.45)/24,'-i',final,'-frames:v','1','-vf','scale=270:480',job/f'final-frame-{i:02}.png'])
run('final-contact',['ffmpeg','-y','-framerate','1','-i',job/'final-frame-%02d.png','-vf','tile=5x3:color=0xfff4de','-frames:v','1',job/'contact-sheet.png'])
dest=ROOT/'deliveries'/job.name;dest.mkdir(exist_ok=True)
for name in ['early_pregnancy_storybook.mp4','cover.png','qa.json','props.json','contact-sheet.png','audio-source.json','visual-review.json']:shutil.copy2(job/name,dest/name)
def timestamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(dest/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"]}' for i,c in enumerate(props['captions'])))
shutil.copy2(mix.with_name('audio-qa.json'),dest/'audio-qa.json')
shutil.copy2(P/'review/h3-clips.json',dest/'h3-clips.json')
chapters=''.join(f'<button onclick="document.querySelector(\'video\').currentTime={x["start"]/24}">{x["shot_id"]} · {html.escape(x["title"])}</button>' for x in props['scenes'])
page=f"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>早孕8个信号 · 视频审阅</title><style>body{{margin:0;background:#fff4de;color:#684630;font:16px system-ui}}main{{max-width:1080px;margin:auto;padding:24px}}.layout{{display:flex;gap:24px;flex-wrap:wrap}}video{{width:min(100%,405px);max-height:82vh;background:#684630;border-radius:16px}}aside{{flex:1;min-width:260px}}button,a{{display:inline-block;padding:10px 14px;margin:5px;border-radius:12px;border:1px solid #d9c7ae;color:#684630;background:#fff9ed;cursor:pointer}}p{{line-height:1.8}}</style><main><h1>早孕可能出现的8个信号</h1><p>奶油绘本科普 · 内部审阅版 · 13镜 · {duration:.2f}秒 · 1080×1920 / 24fps</p><div class="layout"><video controls playsinline preload="metadata" poster="cover.png" src="early_pregnancy_storybook.mp4"></video><aside><h2>按分镜查看</h2>{chapters}<p>角色母版 → 完整参考帧 → H3人物动画 → Remotion图文 → FFmpeg混音与质检。H3原生576×1024，交付放大到1080×1920。</p><p>已做逐镜抽帧、合成抽帧和自动技术QA；未完成完整人工播放及实际听审。已修复结尾旁白，加入原创轻快配乐，增大字幕并调整左上角提示。声线公开使用权尚未核实。</p><a href="early_pregnancy_storybook.mp4" download>下载MP4</a><a href="subtitles.srt">字幕SRT</a><a href="qa.json">质检记录</a><a href="../../projects/early_pregnancy_signs_storybook_02/REVIEW.html">查看已批准分镜方案</a></aside></div></main></html>"""
(dest/'index.html').write_text(page)
manifest={'version':'storybook-v2','run':str(job),'duration_seconds':duration,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(dest.iterdir()) if f.is_file() and f.name!='manifest.json'}}
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('DELIVERY '+str(dest),flush=True)
