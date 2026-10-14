"""220-only composition and technical QA; no generated-frame padding or looping."""
import argparse, hashlib, json, shutil, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--version',default='v1');p.add_argument('--voice-usage',default='configured teacher reference; source record limited to internal testing; public use pending confirmation');p.add_argument('--clip',type=Path,required=True);p.add_argument('--audio-job',type=Path,required=True);p.add_argument('--stage',choices=['preview','final'],required=True);a=p.parse_args()
DURATION=18.625;FRAMES=447
E=Path(__file__).resolve().parents[1];clip=a.clip.resolve();audio=a.audio_job.resolve()
def run(name,args,job):
 result=subprocess.run([str(s) for s in args],capture_output=True,text=True);(job/(name+'.log')).write_text(result.stdout+result.stderr);assert result.returncode==0,(name,result.stderr[-1500:]);return result
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(clip)]));stream=next(s for s in probe['streams'] if s['codec_type']=='video')
assert float(stream['duration'])>=DURATION and stream['width']==576 and stream['height']==1024
align=json.loads((audio/'alignment.json').read_text());assert align['duration']==DURATION
assert hashlib.sha256((audio/'narration.wav').read_bytes()).hexdigest()==align['narration_sha256']
assert DURATION-max(c['audio_end'] for c in align['cues'])>=.6
for i,c in enumerate(align['cues']):
 assert c['start']<c['end']<=DURATION
 if i: assert align['cues'][i-1]['end']<=c['start']
 assert hashlib.sha256((audio/'audio'/f"{c['id']}.wav").read_bytes()).hexdigest()==c['sha256']
job=E/('runs' if a.stage=='preview' else 'deliveries')/(a.stage+'-'+a.version+'-'+time.strftime('%Y%m%d-%H%M%S'));job.mkdir(parents=True,exist_ok=False)
size='576:1024' if a.stage=='preview' else '1080:1920'
output=job/('preview.mp4' if a.stage=='preview' else 'buddha-blessing-v6.mp4')
run('render',['ffmpeg','-y','-i',clip,'-i',audio/'mix.wav','-map','0:v:0','-map','1:a:0','-vf',f"scale={size}:flags=lanczos,ass={audio/'captions.ass'},format=yuv420p",'-frames:v',str(FRAMES),'-r','24','-c:v','libx264','-crf','18','-preset','medium','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(DURATION),'-movflags','+faststart',output],job)
run('full-decode',['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'],job)
finalprobe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)]));(job/'ffprobe.json').write_text(json.dumps(finalprobe,indent=2))
v=next(s for s in finalprobe['streams'] if s['codec_type']=='video');s=next(s for s in finalprobe['streams'] if s['codec_type']=='audio')
assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and v['nb_frames']==str(FRAMES) and v['r_frame_rate']=='24/1'
assert s['codec_name']=='aac' and s['sample_rate']=='48000' and s['channels']==2
assert abs(float(finalprobe['format']['duration'])-DURATION)<.05
black=run('black-check',['ffmpeg','-hide_banner','-i',output,'-vf','blackdetect=d=0.1:pix_th=0.02','-an','-f','null','-'],job)
assert 'black_start:' not in black.stderr
loud=run('loudness',['ffmpeg','-hide_banner','-i',output,'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=8:print_format=json','-f','null','-'],job)
measurement=json.loads(loud.stderr[loud.stderr.rfind('{'):]);assert -19<=float(measurement['input_i'])<=-13;assert float(measurement['input_tp'])<=-1
run('cover',['ffmpeg','-y','-ss','7.8','-i',output,'-frames:v','1',job/'cover.jpg'],job)
run('contact',['ffmpeg','-y','-i',output,'-vf','fps=1,scale=216:384,tile=5x4','-frames:v','1',job/'contact-sheet.jpg'],job)
for t in [0,5,10,14.5,18]:run('frame-'+str(t),['ffmpeg','-y','-ss',str(t),'-i',output,'-frames:v','1',job/f'frame-{t}.png'],job)
for name in ['captions.srt','captions.ass','alignment.json','music-source.json','tts-manifest.json']:shutil.copy2(audio/name,job/name)
qa=dict(technical='passed: full decode, 447 frames at24fps, H264/yuv420p, AAC48k stereo, no black intervals',duration=DURATION,native_resolution=[576,1024],output_resolution=[v['width'],v['height']],loudness_lufs=float(measurement['input_i']),true_peak_dbtp=float(measurement['input_tp']),caption_timing='actual phrase WAV + faster-whisper word timestamps; locked copy kept; no character interpolation',narration_tail_seconds=DURATION-max(c['audio_end'] for c in align['cues']),visual_review='pending',full_playback='pending',actual_listening='pending',voice_usage=a.voice_usage,user_approval='review/approval-v6.json',stage=a.stage)
(job/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
source=dict(master=str(E/'runs/image-v5-20261014-0800/master-v5.png'),master_sha256=hashlib.sha256((E/'runs/image-v5-20261014-0800/master-v5.png').read_bytes()).hexdigest(),clip=str(clip),clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),native_frames=int(stream['nb_frames']),native_duration=float(stream['duration']),trim='native447frames retained; no retiming, looping or frozen frames',narration=str(audio/'narration.wav'),narration_sha256=align['narration_sha256'],mix=str(audio/'mix.wav'),mix_sha256=hashlib.sha256((audio/'mix.wav').read_bytes()).hexdigest(),reference_preprocess='Lanczos aspect-preserving cover with center crop;1024x1792→576x1024; approx0.78% removed at each horizontal edge')
(job/'sources.json').write_text(json.dumps(source,ensure_ascii=False,indent=2))
files=[dict(path=str(f.relative_to(job)),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(job.iterdir()) if f.is_file()]
(job/'manifest.json').write_text(json.dumps(dict(episode_id='buddha_blessing_05',stage=a.stage,files=files),ensure_ascii=False,indent=2))
print('DELIVERY '+str(job),flush=True)
