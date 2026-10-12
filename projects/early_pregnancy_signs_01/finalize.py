"""Finalize the reviewed run. Invoke with uv run python finalize.py /absolute/run."""
import array, hashlib, json, math, re, shutil, subprocess, sys, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];job=Path(sys.argv[1]);renderer=ROOT/'renderers/remotion'
def run(stage,cmd,**kw):
    print(stage,flush=True)
    with (job/(stage+'.log')).open('w') as log:subprocess.run([str(x) for x in cmd],stdout=log,stderr=subprocess.STDOUT,check=True,**kw)
p=json.loads((job/'props.json').read_text());duration=p['durationInFrames']/24
# Join tiny subtitle fragments such as 第一 / 月经推迟 for comfortable reading.
captions=[];pending=None
for c in p['captions']:
    if pending:
        c=dict(text=pending['text']+'，'+c['text'],start=pending['start'],end=c['end']);pending=None
    if len(c['text'])<=3:pending=c
    else:captions.append(c)
if pending:captions.append(pending)
p['captions']=captions
(job/'props.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
def stamp(t):
    v=round(t*1000);return f'{v//3600000:02}:{v//60000%60:02}:{v//1000%60:02},{v%1000:03}'
(job/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(captions)),encoding='utf-8')
# Original restrained ambient cue, synthesized here; no third-party recording.
sr=24000; samples=array.array('f',[0.0])*math.ceil(duration*sr)
chords=[[48,55,60,64,71],[45,52,57,60,67],[41,48,53,57,64],[43,50,55,59,69]]
for k in range(math.ceil(duration/1.5)):
    start=k*1.5; notes=chords[(k//4)%4];midi=notes[[0,2,3,4][k%4]];hz=440*2**((midi-69)/12)
    for j in range(min(int(3.5*sr),len(samples)-int(start*sr))):
        t=j/sr;env=min(1,t/.025)*math.exp(-1.45*t)
        val=(math.sin(2*math.pi*hz*t)+.22*math.sin(4*math.pi*hz*t)+.06*math.sin(6*math.pi*hz*t))*env*.075
        samples[int(start*sr)+j]+=val
pcm=array.array('h')
for i,v in enumerate(samples):
    t=i/sr;fade=min(1,t/2,max(0,(duration-t)/3));pcm.append(round(max(-1,min(1,v*fade))*32767))
if sys.byteorder!='little':pcm.byteswap()
with wave.open(str(job/'music.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
run('audio-mix',['ffmpeg','-y','-i',job/'narration.wav','-i',job/'music.wav','-filter_complex','[0:a]loudnorm=I=-16:TP=-2:LRA=9[a];[1:a]volume=0.30[b];[a][b]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.84:level=false[out]','-map','[out]','-ar','48000','-ac','2',job/'mix.wav'])
bin=renderer/'node_modules/.bin/remotion';entry=renderer/'src/EarlyPregnancy.jsx'
run('final-render',[bin,'render',entry,'EarlyPregnancy',job/'final-visual.mp4','--props',job/'props.json','--concurrency','4','--codec','h264','--crf','18','--pixel-format','yuv420p'],cwd=renderer)
run('final-mux',['ffmpeg','-y','-i',job/'final-visual.mp4','-i',job/'mix.wav','-map','0:v:0','-map','1:a:0','-vf','scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','18','-threads','8','-color_range','tv','-colorspace','bt709','-c:a','aac','-b:a','192k','-t',duration,'-movflags','+faststart',job/'early_pregnancy_signs_v1.mp4'])
run('cover',[bin,'still',entry,'EarlyPregnancyCover',job/'cover.png'],cwd=renderer)
run('decode',['ffmpeg','-v','error','-xerror','-i',job/'early_pregnancy_signs_v1.mp4','-f','null','-'])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(job/'early_pregnancy_signs_v1.mp4')],text=True))
(job/'probe.json').write_text(json.dumps(probe,indent=2))
run('blackcheck',['ffmpeg','-hide_banner','-i',job/'early_pregnancy_signs_v1.mp4','-vf','blackdetect=d=0.15:pix_th=0.10','-an','-f','null','-'])
run('loudness',['ffmpeg','-hide_banner','-i',job/'early_pregnancy_signs_v1.mp4','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-vn','-f','null','-'])
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
log=(job/'loudness.log').read_text();level=json.loads(log[log.rfind('{'):])
checks={'resolution':[v['width'],v['height']]==[1080,1920],'fps':v['avg_frame_rate']=='24/1','frames':int(v['nb_read_frames'])==p['durationInFrames'],'h264':v['codec_name']=='h264','pixel_format':v['pix_fmt']=='yuv420p','audio_aac':a['codec_name']=='aac','audio_rate':a['sample_rate']=='48000','stereo':a['channels']==2,'duration':abs(float(probe['format']['duration'])-duration)<.15,'full_decode':True,'no_black_frames':'black_start:' not in (job/'blackcheck.log').read_text(),'voice_loudness':-19<float(level['input_i'])<-13,'true_peak':float(level['input_tp'])<=-1.0,'captions_ordered':all(c['end']>c['start'] and (i==0 or c['start']>=captions[i-1]['end']-.01) for i,c in enumerate(captions))}
qa={'passed':all(checks.values()),'checks':checks,'duration_seconds':duration,'loudness':level,'visual_review':'Preview contact sheet reviewed; sitting pose corrected before final render. Final still review pending.','speech_review':'Whisper-small matched 97.7% of script characters. Critical facts recognized. See speech-review.json for homophone differences; no human listening approval claimed.','subtitle_timing':p.get('caption_alignment','Estimated from voice duration'),'sha256':hashlib.sha256((job/'early_pregnancy_signs_v1.mp4').read_bytes()).hexdigest()}
(job/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
if not qa['passed']:raise RuntimeError('Technical QA failed: '+str(checks))
# Per-scene stills (rather than evenly spaced samples which can miss short scenes).
for i,s in enumerate(p['scenes']):
    run('frame-'+s['id'],['ffmpeg','-y','-ss',(s['start']+s['frames']*.55)/24,'-i',job/'early_pregnancy_signs_v1.mp4','-frames:v','1','-vf','scale=270:480',job/f'frame-{i:02}.png'])
run('final-contact',['ffmpeg','-y','-framerate','1','-i',job/'frame-%02d.png','-vf','tile=5x3:color=0xfaf5eb','-frames:v','1',job/'contact-sheet-final.png'])
destination=ROOT/'deliveries'/job.name;destination.mkdir(exist_ok=True)
for name in ['early_pregnancy_signs_v1.mp4','cover.png','subtitles.srt','qa.json','contact-sheet-final.png','narration-manifest.json','props.json']:
    shutil.copy2(job/name,destination/name)
(job/'status.json').write_text(json.dumps({'stage':'rendered_and_technical_qa_passed','delivery':str(destination)},ensure_ascii=False))
print('DELIVERY '+str(destination),flush=True)
