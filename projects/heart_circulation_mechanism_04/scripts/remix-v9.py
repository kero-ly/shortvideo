"""Music audibility revision, production only on 220; preserve v8 video packets."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

E=Path('/home/ly/shortvideo/projects/heart_circulation_mechanism_04')
OLD=E/'deliveries/20261013-heart-v8'
RUN=E/'runs/20261013-heart-v9'
OUT=E/'deliveries/20261013-heart-v9'
FILTER=('[0:a]aresample=48000,volume=1.25,asplit=2[voice][side];'
        '[1:a]volume=1.20[music];'
        '[music][side]sidechaincompress=threshold=0.08:ratio=2:attack=12:release=240[duck];'
        '[voice][duck]amix=inputs=2:normalize=0,'
        'loudnorm=I=-16:TP=-1.5:LRA=8:linear=false,aresample=48000[mix]')
def cmd(*a): return subprocess.run(a,check=True,capture_output=True,text=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def packets(p,s):return cmd('ffmpeg','-v','error','-i',str(p),'-map',s,'-c','copy','-f','hash','-hash','SHA256','-').stdout.strip()
assert not RUN.exists() and not OUT.exists(), 'unique revision required'
RUN.mkdir(parents=True)
cmd('ffmpeg','-v','warning','-i',str(OLD/'narration.wav'),'-i',str(OLD/'music-original.wav'),'-filter_complex',FILTER,'-map','[mix]','-ac','2',str(RUN/'mix.wav'))
cmd('ffmpeg','-v','warning','-i',str(OLD/'heart-circulation.mp4'),'-i',str(RUN/'mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-shortest','-movflags','+faststart',str(RUN/'heart-circulation.mp4'))
OUT.mkdir()
for p in OLD.iterdir():
    if p.suffix=='.png' or p.name in ['alignment.json','word-alignment.json','props.json','subtitles.srt','tts-manifest.json','narration.wav','music-original.wav','contact-sheet-index.json']:
        shutil.copy2(p,OUT/p.name)
for name in ['mix.wav','heart-circulation.mp4']:shutil.copy2(RUN/name,OUT/name)
video=OUT/'heart-circulation.mp4'
vh=packets(video,'0:v:0');assert vh==packets(OLD/video.name,'0:v:0')
assert packets(video,'0:a:0')!=packets(OLD/video.name,'0:a:0')
probe=json.loads(cmd('ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)).stdout)
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['pix_fmt'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'yuv420p','30/1',842)
assert (a['codec_name'],a['sample_rate'],a['channels'])==('aac','48000',2)
cmd('ffmpeg','-v','error','-i',str(video),'-f','null','-')
black=cmd('ffmpeg','-hide_banner','-i',str(video),'-vf','blackdetect=d=0.15:pix_th=0.08','-an','-f','null','-');assert 'black_start:' not in black.stderr
loud=cmd('ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-')
metrics=json.loads(loud.stderr[loud.stderr.rfind('{'):]);assert -19<=float(metrics['input_i'])<=-13 and float(metrics['input_tp'])<=-1
props=json.loads((OUT/'props.json').read_text());tail=842/30-props['shots'][-1]['audioStart']-props['shots'][-1]['audioDuration'];assert tail>=.6
music=json.loads((OLD/'music-source.json').read_text());music.update(revision='v9',voice_gain=1.25,music_gain=1.2,previous_music_gain=.6,music_gain_change_db=6.0206,ducking='threshold=0.08 ratio=2 attack=12 release=240',mix_filter=FILTER)
sources=json.loads((OLD/'sources.json').read_text());sources.update(music=music,lineage='v8 video packet copy + same narration/music sources -> v9 music +6.02dB and lighter ducking -> new AAC mix')
qa=dict(technical='passed',visual='identical video packets to v8',visual_stream_sha256=vh,loudness=metrics,frames=842,duration_seconds=842/30,tail_seconds=tail,decode='passed',black_frames='none >=0.15s',caption_timing='same source narration and byte-identical props/ASR/SRT',full_playback='pending browser check',actual_listening='pending user review',release='internal review')
for name,data in [('ffprobe',probe),('loudness',metrics),('music-source',music),('sources',sources),('qa',qa)]:
    (OUT/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
page=(OLD/'index.html').read_text().replace('v8 路径引导','v9 配乐增强').replace('配音与音乐保持 v7 比例。','背景音乐增益提高约 6 dB，减轻口播时的音乐压低；人声增益保持不变。').replace('../20261013-heart-v7/index.html','../20261013-heart-v8/index.html').replace('对比 v7','对比 v8')
(OUT/'index.html').write_text(page)
manifest=dict(revision=9,parent='20261013-heart-v8',files=[dict(path=p.name,sha256=sha(p),bytes=p.stat().st_size) for p in sorted(OUT.iterdir()) if p.is_file()])
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for name in ['qa','manifest','music-source','sources']:shutil.copy2(OUT/f'{name}.json',E/f'review/v9-{name}.json')
print(json.dumps(qa,ensure_ascii=False,indent=2))
