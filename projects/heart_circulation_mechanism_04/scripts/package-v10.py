"""Package the directional-cue revision; run only on production host 220."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

E = Path('/home/ly/shortvideo/projects/heart_circulation_mechanism_04')
OLD = E / 'deliveries/20261013-heart-v9'
RUN = E / 'runs/20261013-heart-v10'
OUT = E / 'deliveries/20261013-heart-v10'

def command(*args):
    return subprocess.run(args, check=True, text=True, capture_output=True)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def packet_hash(p, stream):
    return command('ffmpeg', '-v', 'error', '-i', str(p), '-map', stream,
                   '-c', 'copy', '-f', 'hash', '-hash', 'SHA256', '-').stdout.strip()

assert not OUT.exists(), 'Never overwrite a previous delivery'
OUT.mkdir(parents=True)
for name in ['props.json', 'alignment.json', 'word-alignment.json', 'subtitles.srt',
             'music-source.json', 'tts-manifest.json', 'narration.wav', 'music-original.wav', 'mix.wav']:
    shutil.copy2(OLD / name, OUT / name)
shutil.copy2(RUN / 'heart-circulation.mp4', OUT / 'heart-circulation.mp4')
video = OUT / 'heart-circulation.mp4'
audio_hash = packet_hash(video, '0:a:0')
assert audio_hash == packet_hash(OLD / video.name, '0:a:0')
assert packet_hash(video, '0:v:0') != packet_hash(OLD / video.name, '0:v:0')
probe = json.loads(command('ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(video)).stdout)
(OUT / 'ffprobe.json').write_text(json.dumps(probe, indent=2))
command('ffmpeg', '-v', 'error', '-i', str(video), '-f', 'null', '-')
black = command('ffmpeg', '-hide_banner', '-i', str(video), '-vf', 'blackdetect=d=0.15:pix_th=0.08', '-an', '-f', 'null', '-')
assert 'black_start:' not in black.stderr
(RUN / 'blackdetect.log').write_text(black.stderr)
loud = command('ffmpeg', '-hide_banner', '-i', str(video), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-')
metrics = json.loads(loud.stderr[loud.stderr.rfind('{'):])
(OUT / 'loudness.json').write_text(json.dumps(metrics, indent=2))
v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
a = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
assert (v['width'],v['height'],v['r_frame_rate'],v['pix_fmt'],int(v['nb_frames'])) == (1080,1920,'30/1','yuv420p',842)
assert (a['codec_name'],a['sample_rate'],a['channels']) == ('aac','48000',2)
assert -19 <= float(metrics['input_i']) <= -13 and float(metrics['input_tp']) <= -1
props = json.loads((OUT / 'props.json').read_text())
tail = 842/30 - (props['shots'][-1]['audioStart']+props['shots'][-1]['audioDuration'])
assert tail >= .6
frames = []
for i,s in enumerate(props['shots'],1):
    for label,frame in [('start',s['start']),('middle',s['start']+s['frames']//2),('end',s['start']+s['frames']-1)]:
        name = f'shot{i:02}-{label}.png'
        command('ffmpeg','-v','error','-i',str(video),'-vf',f'select=eq(n\\,{frame}),scale=270:480','-frames:v','1',str(OUT/name))
        frames.append((name,frame))
for frame in [240,280,410,470,499,500,510,521,532,542,695,725]:
    name=f'frame-{frame}.png'
    shutil.copy2(RUN/name,OUT/name)
    frames.append((name,frame))
sample_frames=sorted(set(frame for _,frame in frames))
selection='+'.join(f'eq(n\\,{frame})' for frame in sample_frames)
command('ffmpeg','-v','error','-i',str(video),'-vf',
        f'select={selection},scale=270:480,tile=6x5:nb_frames={len(sample_frames)}',
        '-frames:v','1',str(OUT/'contact-sheet.png'))
(OUT/'contact-sheet-index.json').write_text(json.dumps(sample_frames))
shutil.copy2(OUT/'shot01-middle.png',OUT/'cover.png')
sources=json.loads((OLD/'sources.json').read_text())
sources['lineage']='v9 approved revision inputs -> Heart-v10.jsx bold flow cues, body silhouette and anchored vessel zoom -> Remotion 220 -> v9 AAC packet copy'
sources['renderer']={'path':'scripts/Heart-v10.jsx','sha256':sha(E/'scripts/Heart-v10.jsx')}
(OUT/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
qa=dict(technical='passed',resolution='1080x1920',frames=842,fps=30,decode='passed',
        black_frames='none >= 0.15s',loudness=metrics,tail_seconds=tail,
        audio_packets_sha256=audio_hash,audio='identical AAC packets to v9',
        timing='v9 props, narration, captions and ASR retained byte-for-byte',
        visual='pending contact-sheet review',full_playback='pending',actual_listening='pending user review',
        status='internal review, not publication approval')
(OUT/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>心脏循环 · v10 路径引导</title><style>body{background:#f6eddc;color:#593a2f;font:17px system-ui;margin:0}main{max-width:1000px;margin:auto;padding:24px;text-align:center}video{max-height:75vh;width:min(100%,380px);background:#222;border-radius:10px}button,a{display:inline-block;padding:12px;margin:5px;color:#593a2f}button{background:#ffdc68;border:0;border-radius:20px;cursor:pointer}.frames{display:flex;flex-wrap:wrap;justify-content:center}.frames img{width:150px}h1{font-size:28px}</style><main><h1>心脏循环 · v10 路径引导</h1><p>加粗血流方向、柔和闪动聚焦标记；全身改为人体，从腹部血管连续放大。保留 v9 增强音乐。</p><video id="v" controls playsinline preload="metadata" poster="cover.png" src="heart-circulation.mp4"></video><div><button onclick="seek(5.833333)">右心 → 肺部</button><button onclick="seek(12.066667)">左心 → 全身</button><button onclick="seek(0)">从头播放</button><button onclick="seek(15.8)">人体 → 血管放大</button><button onclick="seek(21.833333)">血液回到心脏</button></div><p><a href="../20261013-heart-v9/index.html">对比 v9</a><a href="heart-circulation.mp4" download>下载新版视频</a></p><div class="frames">'''
for frame in [240,280,410,470,499,500,510,521,532,542,695,725]:
    page+=f'<a href="frame-{frame}.png"><img src="frame-{frame}.png"><br>{frame/30:.2f} 秒</a>'
page+='</div><script>function seek(t){let v=document.getElementById("v");v.currentTime=t;v.play();}</script></main></html>'
(OUT/'index.html').write_text(page)
manifest=dict(revision=10,parent='20261013-heart-v9',files=[dict(path=p.name,sha256=sha(p),bytes=p.stat().st_size) for p in sorted(OUT.iterdir()) if p.is_file()])
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for name in ['qa','manifest','sources']:
    shutil.copy2(OUT/f'{name}.json',E/f'review/v10-{name}.json')
print(json.dumps(qa,ensure_ascii=False,indent=2))
