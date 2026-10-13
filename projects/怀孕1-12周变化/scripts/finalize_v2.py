import json,hashlib,subprocess,shutil,time,uuid
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo'
job=P/(P/'review/latest-compose-v2.txt').read_text().strip();props=json.loads((job/'props.json').read_text());r=ROOT/'renderers/remotion'
d=P/'deliveries'/('pregnancy-weeks-v2-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);d.mkdir(parents=True)
def run(name,args,cwd=None):
 print(name,flush=True)
 with (d/(name+'.log')).open('w') as f:subprocess.run(list(map(str,args)),stdout=f,stderr=subprocess.STDOUT,check=True,cwd=cwd)
run('final-render',[r/'node_modules/.bin/remotion','render',r/'src/PregnancyWeeksEpisode.jsx','PregnancyWeeks',d/'visual.mp4','--props',job/'props.json','--concurrency','3','--codec','h264','--crf','18'],r)
run('final-mux',['ffmpeg','-y','-i',d/'visual.mp4','-i',job/'mix.wav','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',props['duration_seconds'],'-movflags','+faststart',d/'怀孕1-12周变化.mp4'])
video=d/'怀孕1-12周变化.mp4';run('decode',['ffmpeg','-v','error','-xerror','-i',video,'-f','null','-'])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True));(d/'ffprobe.json').write_text(json.dumps(probe,indent=2));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],v['pix_fmt'])==(1080,1920,'24/1','yuv420p');assert int(v['nb_frames'])==props['total_frames'];assert a['sample_rate']=='48000' and a['channels']==2
run('blackframes',['ffmpeg','-hide_banner','-i',video,'-vf','blackdetect=d=0.1:pix_th=0.1','-an','-f','null','-'])
run('loudness',['ffmpeg','-hide_banner','-i',video,'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-vn','-f','null','-'])
run('cover',['ffmpeg','-y','-ss','1','-i',video,'-frames:v','1',d/'cover.jpg'])
for src,name in [(job/'props.json','props.json'),(P/'timeline/captions-v2.srt','captions.srt'),(P/'review/h3-clips-v2.json','source-index.json'),(P/'FACT_CHECK.md','FACT_CHECK.md'),(P/'PUBLISHING_DRAFT.md','PUBLISHING_DRAFT.md')]:shutil.copy2(src,d/name)
last=props['shots'][-1];tail=props['duration_seconds']-last['audio_start']-last['audio_duration'];assert tail>=.6
qa={'technical':{'decode':True,'size':[1080,1920],'fps':24,'frames':props['total_frames'],'duration':props['duration_seconds'],'audio_rate':48000,'channels':2,'voice_tail_seconds':tail},'native_generation_size':[576,1024],'caption_alignment':'actual faster-whisper word timestamps matched to locked script','visual_sampling':'see episode review/h3-clips-v2.json and composition review','full_playback':'pending','actual_listening':'pending','voice_public_rights':'not documented in available records','music':None,'scope':'internal review; no platform publication performed'}
(d/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));manifest={x.name:{'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'bytes':x.stat().st_size} for x in d.iterdir() if x.is_file()};(d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(P/'review/latest-delivery-v2.txt').write_text(str(d.relative_to(P)));shutil.copy2(d/'qa.json',P/'review/delivery-qa-v2.json');shutil.copy2(d/'manifest.json',P/'review/delivery-manifest-v2.json');print('DELIVERY_READY '+str(d),flush=True)
