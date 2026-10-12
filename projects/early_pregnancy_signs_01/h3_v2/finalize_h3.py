"""Final render after visual preview review, followed by technical QA and delivery."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2];job=Path(sys.argv[1]);props=json.loads((job/'props.json').read_text());duration=props['durationInFrames']/24
approved=json.loads((P/'review/h3-clips.json').read_text())
assert all(approved.get(f'shot_{i:02}',{}).get('accepted') is True for i in range(1,14)),'Unreviewed H3 clip'
def run(stage,cmd,**kw):
 print(stage,flush=True)
 with (job/(stage+'.log')).open('w') as f:subprocess.run([str(x) for x in cmd],stdout=f,stderr=subprocess.STDOUT,check=True,**kw)
renderer=ROOT/'renderers/remotion';binary=renderer/'node_modules/.bin/remotion';entry=renderer/'src/EarlyPregnancyH3.jsx'
run('final-render',[binary,'render',entry,'EarlyPregnancyH3',job/'visual.mp4','--props',job/'props.json','--concurrency','4','--codec','h264','--crf','17'],cwd=renderer)
run('cover',[binary,'still',entry,'EarlyPregnancyH3Cover',job/'cover.png','--props',job/'props.json'],cwd=renderer)
mix=ROOT/'runs/early-pregnancy-20261013-010143-e9a8/mix.wav'
vp=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(job/'visual.mp4')],text=True))['streams'][0]
vf='scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p' if vp.get('color_range')=='pc' else 'format=yuv420p'
final=job/'early_pregnancy_h3_v2.mp4'
run('final-mix',['ffmpeg','-y','-i',job/'visual.mp4','-i',mix,'-map','0:v:0','-map','1:a:0','-vf',vf,'-c:v','libx264','-preset','fast','-crf','18','-threads','8','-color_range','tv','-colorspace','bt709','-c:a','aac','-b:a','192k','-t',duration,'-movflags','+faststart',final])
run('decode',['ffmpeg','-v','error','-xerror','-i',final,'-f','null','-'])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)],text=True))
(job/'probe.json').write_text(json.dumps(probe,indent=2));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
run('black-check',['ffmpeg','-hide_banner','-i',final,'-vf','blackdetect=d=.15:pix_th=.10','-an','-f','null','-'])
run('loudness',['ffmpeg','-hide_banner','-i',final,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-vn','-f','null','-'])
log=(job/'loudness.log').read_text();loud=json.loads(log[log.rfind('{'):])
checks={'resolution':[v['width'],v['height']]==[1080,1920],'fps':v['avg_frame_rate']=='24/1','frames':int(v['nb_read_frames'])==props['durationInFrames'],'codec':v['codec_name']=='h264' and v['pix_fmt']=='yuv420p','audio':a['codec_name']=='aac' and a['sample_rate']=='48000' and a['channels']==2,'duration':abs(float(probe['format']['duration'])-duration)<.15,'decode':True,'no_black_frames':'black_start:' not in (job/'black-check.log').read_text(),'loudness':-19<float(loud['input_i'])<-13,'peak':float(loud['input_tp'])<=-1,'h3_all_13':len(json.loads((P/'review/h3-clips.json').read_text()))==13}
qa={'passed':all(checks.values()),'checks':checks,'duration_seconds':duration,'loudness':loud,'native_h3_resolution':[576,1024],'delivery_resolution':[1080,1920],'voice':'Existing internal review narration; production usage rights of source voice not verified','sha256':hashlib.sha256(final.read_bytes()).hexdigest()}
(job/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
assert qa['passed'],checks
dest=ROOT/'deliveries'/job.name;dest.mkdir(exist_ok=True)
for name in ['early_pregnancy_h3_v2.mp4','cover.png','qa.json','props.json','contact-sheet.png']:shutil.copy2(job/name,dest/name)
shutil.copy2(ROOT/'deliveries/early-pregnancy-20261013-010143-e9a8/subtitles.srt',dest/'subtitles.srt')
shutil.copy2(P/'review/h3-clips.json',dest/'h3-clips.json')
manifest={'version':'h3-v2','run':str(job),'duration_seconds':duration,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(dest.iterdir()) if f.is_file() and f.name!='manifest.json'}}
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('DELIVERY '+str(dest),flush=True)
