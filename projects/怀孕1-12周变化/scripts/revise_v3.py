import json,hashlib,subprocess,shutil,time,uuid,wave,array,math
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo'
old=P/'runs/compose-v2-20261014-010845-0510';props=json.loads((old/'props.json').read_text());job=P/'runs'/('revision-v3-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir();d=P/'deliveries'/job.name;d.mkdir(parents=True)
def run(name,cmd,cwd=None):
 print(name,flush=True)
 with (job/(name+'.log')).open('w') as f:subprocess.run(list(map(str,cmd)),stdout=f,stderr=subprocess.STDOUT,check=True,cwd=cwd)
# Reuse verified complete voice and actual word timing. No TTS or H3 rerun.
voice=P/props['narration'];assert hashlib.sha256(voice.read_bytes()).hexdigest()==props['narration_sha256']
with wave.open(str(voice)) as w:
 a=array.array('h',w.readframes(w.getnframes()));assert math.sqrt(sum(x*x for x in a)/len(a))>1000
sr=48000;duration=props['duration_seconds'];n=round(duration*sr);out=np.zeros((n,2),dtype=np.float32);beat=60/88
chords=[[60,64,67,71],[57,60,64,67],[53,57,60,64],[55,59,62,67]];melody=[76,79,76,74,72,76,74,72]
def note(t,midi,level,length=1.8,pan=0):
 start=round(t*sr);count=min(round(length*sr),n-start)
 if count<=0:return
 x=np.arange(count)/sr;f=440*2**((midi-69)/12);env=(1-np.exp(-x*55))*np.exp(-x*2.7);y=level*env*(np.sin(2*np.pi*f*x)+.18*np.sin(4*np.pi*f*x)+.05*np.sin(6*np.pi*f*x))
 out[start:start+count,0]+=y*(1-.3*pan);out[start:start+count,1]+=y*(1+.3*pan)
for b in range(int(duration/beat)+1):
 c=chords[(b//8)%4];note(b*beat,c[b%4],.095,2,(-1)**b*.4)
 if b%4==0:note(b*beat,c[0]-12,.07,2.5)
 if b%2==0:note((b+.5)*beat,melody[(b//2)%8],.06,1.6,(-1)**(b//2)*.5)
x=np.arange(n)/sr;out*= (np.minimum(x/1.2,1)*np.minimum((duration-x)/1.8,1))[:,None]
with wave.open(str(job/'music-original.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
filters='[0:a]aresample=48000,asplit=2[voice][side];[1:a]volume=0.6[music];[music][side]sidechaincompress=threshold=0.02:ratio=4:attack=15:release=350[duck];[voice][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000[mix]'
run('mix',['ffmpeg','-y','-i',voice,'-i',job/'music-original.wav','-filter_complex',filters,'-map','[mix]','-ar','48000','-ac','2',job/'mix.wav'])
source={'source':'original procedural music, no external recording','bpm':88,'key':'C major / A minor','instruments':'soft piano-like sine harmonics, warm low notes; no percussion','generator':'scripts/revise_v3.py','fade_in':1.2,'fade_out':1.8,'mix_filter':filters,'voice':props['narration'],'voice_sha256':props['narration_sha256'],'voice_rate':1.0,'voice_public_rights':'configured factory reference, public-use authorization not documented','change':'explicit audio stream mapping fixes prior silent soundtrack'};(job/'audio-source.json').write_text(json.dumps(source,ensure_ascii=False,indent=2))
r=ROOT/'renderers/remotion';entry=r/'src/PregnancyWeeksV3.jsx';shutil.copy2(P/'scripts/PregnancyWeeksV3.jsx',entry);(job/'props.json').write_text(json.dumps(props,ensure_ascii=False,indent=2))
run('preview',[r/'node_modules/.bin/remotion','render',entry,'PregnancyWeeks',job/'preview-visual.mp4','--props',job/'props.json','--scale','.5','--concurrency','3','--codec','h264','--pixel-format','yuv420p'],r)
run('preview-mux',['ffmpeg','-y','-i',job/'preview-visual.mp4','-i',job/'mix.wav','-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-vf','scale=in_range=full:out_range=tv,format=yuv420p','-color_range','tv','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',duration,'-movflags','+faststart',job/'preview.mp4'])
for i,s in enumerate(props['shots']):run('frame-'+str(i),['ffmpeg','-y','-ss',(s['start']+s['frames']*.5)/24,'-i',job/'preview.mp4','-frames:v','1','-vf','scale=270:480',job/f'frame-{i:02}.png'])
run('contact',['ffmpeg','-y','-framerate','1','-i',job/'frame-%02d.png','-vf','tile=4x4','-frames:v','1',job/'contact.png'])
(P/'review/latest-compose-v3.txt').write_text(str(job.relative_to(P)));print('PREVIEW_READY '+str(job),flush=True)
# Full-size output is authorized by the user's requested video revision.
run('render',[r/'node_modules/.bin/remotion','render',entry,'PregnancyWeeks',d/'visual.mp4','--props',job/'props.json','--concurrency','3','--codec','h264','--pixel-format','yuv420p','--crf','18'],r)
video=d/'怀孕1-12周变化-v3.mp4';run('mux',['ffmpeg','-y','-i',d/'visual.mp4','-i',job/'mix.wav','-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-vf','scale=in_range=full:out_range=tv,format=yuv420p','-color_range','tv','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',duration,'-movflags','+faststart',video])
run('decode',['ffmpeg','-v','error','-xerror','-i',video,'-f','null','-'])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True));v=next(x for x in probe['streams']if x['codec_type']=='video');a=next(x for x in probe['streams']if x['codec_type']=='audio');assert(v['width'],v['height'],v['r_frame_rate'],v['pix_fmt'],int(v['nb_frames']))==(1080,1920,'24/1','yuv420p',props['total_frames']);assert(a['codec_name'],a['sample_rate'],a['channels'])==('aac','48000',2);assert abs(float(a['duration'])-duration)<.05
pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-f','f32le','-ac','1','-ar','48000','-']),dtype=np.float32);rms=float(np.sqrt(np.mean(pcm**2)));assert rms>.02,'Silent/inaudible final audio'
for s in props['shots']:
 seg=pcm[round(s['audio_start']*sr):round((s['audio_start']+s['audio_duration'])*sr)];assert float(np.sqrt(np.mean(seg**2)))>.02,s['id']
run('loudness',['ffmpeg','-hide_banner','-i',video,'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-vn','-f','null','-'])
run('blackdetect',['ffmpeg','-hide_banner','-i',video,'-vf','blackdetect=d=0.1:pix_th=0.1','-an','-f','null','-'])
run('cover',['ffmpeg','-y','-ss','2.8','-i',video,'-frames:v','1',d/'cover.jpg'])
for src,name in [(job/'props.json','props.json'),(job/'audio-source.json','audio-source.json'),(P/'timeline/captions-v2.srt','captions.srt'),(P/'review/h3-clips-v2.json','source-index.json'),(P/'FACT_CHECK.md','FACT_CHECK.md'),(P/'PUBLISHING_DRAFT.md','PUBLISHING_DRAFT.md'),(job/'loudness.log','loudness.log'),(job/'blackdetect.log','blackdetect.log')]:shutil.copy2(src,d/name)
(d/'ffprobe.json').write_text(json.dumps(probe,indent=2));qa={'revision':3,'changes':['top-left gestational-week note','centered upper-middle narration captions','explicit voice audio mapping','original warm piano-like background music'],'technical':{'decode':True,'size':[1080,1920],'fps':24,'frames':props['total_frames'],'duration':duration,'audio':'AAC 48kHz stereo','final_audio_rms':rms,'per_shot_nonsilent':True},'native_generation_size':[576,1024],'caption_timing':'original actual word timestamps reused; voice unchanged','visual_sampling':'pending','full_playback':'pending','actual_listening':'pending','voice_public_rights':source['voice_public_rights'],'music':'original procedural composition, no external recording'};(d/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));manifest={x.name:{'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'bytes':x.stat().st_size}for x in d.iterdir()if x.is_file()and x.name!='manifest.json'};(d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));shutil.copy2(d/'qa.json',P/'review/delivery-qa-v3.json');shutil.copy2(d/'manifest.json',P/'review/delivery-manifest-v3.json');(P/'review/latest-delivery-v3.txt').write_text(str(d.relative_to(P)));print('DELIVERY_READY '+str(d),flush=True)
