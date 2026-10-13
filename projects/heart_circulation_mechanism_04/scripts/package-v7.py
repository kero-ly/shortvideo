"""Package the v7 audio-only revision on the 220 production host."""
import hashlib
import html
import json
import shutil
import subprocess
from pathlib import Path

E = Path('/home/ly/shortvideo/projects/heart_circulation_mechanism_04')
OLD = E / 'deliveries/20261013-heart-v6'
RUN = E / 'runs/20261013-heart-v7'
OUT = E / 'deliveries/20261013-heart-v7'
FILTER = ('[0:a]aresample=48000,volume=1.25,asplit=2[voice][side];'
          '[1:a]volume=0.60[music];'
          '[music][side]sidechaincompress=threshold=0.025:ratio=5:attack=12:release=240[duck];'
          '[voice][duck]amix=inputs=2:normalize=0,'
          'loudnorm=I=-16:TP=-1.5:LRA=8:linear=false,aresample=48000[mix]')


def command(*args):
    return subprocess.run(args, check=True, text=True, capture_output=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def video_packets(path):
    output = command('ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
                     '-c', 'copy', '-f', 'hash', '-hash', 'SHA256', '-').stdout
    return output.strip()


assert RUN.joinpath('mix.wav').is_file() and RUN.joinpath('heart-circulation.mp4').is_file()
assert not OUT.exists(), 'v7 delivery already exists'
OUT.mkdir(parents=True)
for name in ['alignment.json', 'contact-sheet.png', 'cover.png', 'music-original.wav',
             'narration.wav', 'props.json', 'subtitles.srt', 'tts-manifest.json',
             'word-alignment.json'] + [f'shot{i:02}.png' for i in range(1, 6)]:
    shutil.copy2(OLD / name, OUT / name)
shutil.copy2(OLD / 'heart-circulation.mp4', OUT / 'preview-v6.mp4')
for name in ['mix.wav', 'heart-circulation.mp4']:
    shutil.copy2(RUN / name, OUT / name)

video_hash = video_packets(OLD / 'heart-circulation.mp4')
assert video_hash == video_packets(OUT / 'heart-circulation.mp4'), 'visual stream changed'
probe = json.loads(command('ffprobe', '-v', 'error', '-show_format', '-show_streams',
                           '-of', 'json', str(OUT / 'heart-circulation.mp4')).stdout)
(OUT / 'ffprobe.json').write_text(json.dumps(probe, indent=2))
command('ffmpeg', '-v', 'error', '-i', str(OUT / 'heart-circulation.mp4'), '-f', 'null', '-')
black = command('ffmpeg', '-hide_banner', '-i', str(OUT / 'heart-circulation.mp4'),
                '-vf', 'blackdetect=d=0.15:pix_th=0.08', '-an', '-f', 'null', '-')
assert 'black_start:' not in black.stderr
loud = command('ffmpeg', '-hide_banner', '-i', str(OUT / 'heart-circulation.mp4'),
               '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-')
metrics = json.loads(loud.stderr[loud.stderr.rfind('{'):])
(OUT / 'loudness.json').write_text(json.dumps(metrics, indent=2))
props = json.loads((OUT / 'props.json').read_text())
vs = next(s for s in probe['streams'] if s['codec_type'] == 'video')
au = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
assert (vs['width'], vs['height'], vs['r_frame_rate'], vs['pix_fmt']) == (1080, 1920, '30/1', 'yuv420p')
assert int(vs['nb_frames']) == props['totalFrames'] == 842
assert (au['codec_name'], au['sample_rate'], au['channels']) == ('aac', '48000', 2)
assert -19 <= float(metrics['input_i']) <= -13 and float(metrics['input_tp']) <= -1
tail = props['totalFrames'] / 30 - (props['shots'][-1]['audioStart'] + props['shots'][-1]['audioDuration'])
assert tail >= 0.6

music = json.loads((OLD / 'music-source.json').read_text())
music.update(generator='scripts/music-v6.py; reused unchanged', mix_filter=FILTER,
             voice_gain=1.25, music_gain=0.60, previous_voice_gain=1.4,
             previous_music_gain=0.48, revision='v7 mix only')
(OUT / 'music-source.json').write_text(json.dumps(music, ensure_ascii=False, indent=2))
sources = json.loads((OLD / 'sources.json').read_text())
sources['music'] = music
sources['lineage'] = 'v6 visual/narration/music/captions unchanged -> v7 audio remix -> video stream copy and AAC remux'
(OUT / 'sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2))
qa = dict(technical='passed', revision='v7 mix only', resolution='1080x1920',
          frames=842, fps=30, duration_seconds=842 / 30, loudness=metrics,
          tail_seconds=tail, decode='all frames decoded without error',
          black_frames='none >= 0.15 seconds', audio='AAC 48kHz stereo',
          visual_stream_sha256=video_hash, visual='bit-identical video packets to v6',
          caption_timing='v6 narration and alignment files reused byte-for-byte',
          full_playback='pending browser playback check',
          actual_listening='pending; user to compare v7 and v6 balance',
          release='internal review; no publication approval; reference voice rights not independently confirmed')
(OUT / 'qa.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2))

cards = ''.join(
    f'<article><a href="shot{i:02}.png"><img src="shot{i:02}.png" alt="镜头{i}"></a>'
    f'<div><h2>镜头 {i:02}</h2><p>{html.escape(s["text"])}</p>'
    f'<p>{s["start"]/30:.2f}–{(s["start"]+s["frames"])/30:.2f} 秒</p>'
    f'<button onclick="seek({s["start"]/30})">播放这段</button></div></article>'
    for i, s in enumerate(props['shots'], 1))
page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>心脏的小小运输队 · v7</title><style>body{margin:0;background:#f6eddc;color:#593a2f;font:17px system-ui}main{max-width:1050px;margin:auto;padding:28px}h1{font-size:34px}video{width:min(100%,380px);max-height:78vh;background:#222;border-radius:8px}header{text-align:center}a{color:#984b32}article{display:flex;gap:28px;background:#fff9ed;padding:20px;border-radius:8px;margin:24px 0}article img{width:200px;max-width:38vw;border-radius:8px}button{padding:12px 20px;border:0;background:#653c32;color:white;border-radius:8px;cursor:pointer}p{line-height:1.7}summary{cursor:pointer}footer{font-size:14px}</style><main><header><h1>心脏的小小运输队</h1><p>第七版 · 声音比例调整</p><video id="v" controls playsinline preload="metadata" poster="cover.png" src="heart-circulation.mp4"></video><p><a href="heart-circulation.mp4">下载 1080p 视频</a> · <a href="subtitles.srt">字幕</a> · <a href="qa.json">技术检查</a></p></header><p>人声稍降，背景音乐稍升；画面、文案、配音演绎和时长与第六版一致。</p><details><summary>对比第六版混音</summary><video controls preload="none" src="preview-v6.mp4"></video></details>''' + cards + '''<footer><p>原创配乐，未使用抖音原声。颜色和结构为科普示意。当前为内部审阅样片，实际听感待确认。</p></footer></main><script>function seek(t){let v=document.getElementById('v');v.currentTime=t;v.play();v.scrollIntoView({behavior:'smooth',block:'center'})}</script></html>'''
(OUT / 'index.html').write_text(page)
manifest = {p.name: dict(sha256=sha(p), bytes=p.stat().st_size)
            for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'manifest.json'}
(OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2))
for name in ['manifest.json', 'qa.json', 'sources.json', 'music-source.json']:
    shutil.copy2(OUT / name, E / 'review' / ('v7-' + name))
print(json.dumps(qa, ensure_ascii=False, indent=2))
print(OUT)
