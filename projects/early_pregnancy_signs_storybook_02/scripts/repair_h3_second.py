"""Server-only serial H3 generation; no automatic resubmission of failed requests."""
import hashlib,json,subprocess,sys,time,socket
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1]
assert str(ROOT)=='/home/ly/shortvideo','Video work must run on 220'
d=json.loads((P/'shots.plan.json').read_text());assert d['status']=='production_approved'
review=P/'review';review.mkdir(exist_ok=True);manifest_path=review/'h3-clips.json'
m=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
for sid in sys.argv[1:]:
 x=next(s for s in d['shots'] if s['id']==sid)
 if sid in m:
  assert (ROOT/m[sid]['clip']).is_file();print('RECORDED '+sid,flush=True);continue
 image=P/x['reference_image'];assert hashlib.sha256(image.read_bytes()).hexdigest()==x['reference_sha256']
 logdir=ROOT/'runs'/('storybook-submit-'+sid+'-'+time.strftime('%Y%m%d-%H%M%S'));logdir.mkdir()
 cmd=[sys.executable,str(ROOT/'capabilities/video-generation/h3_comfy.py'),'--image',str(image),'--prompt-file',str(P/f'prompts/shots/shot_{sid}_motion_v3.txt'),'--shot','storybook-'+sid,'--frames',str(x['production_frames']),'--width','576','--height','1024','--seed',str(20263020+int(sid)),'--graph',str(ROOT/'capabilities/video-generation/h3_baseline20.json')]
 print('START '+sid+' '+str(logdir),flush=True)
 with (logdir/'submit.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError('Inspect '+str(logdir/'submit.log')+'; do not resubmit automatically')
 line=next(s for s in (logdir/'submit.log').read_text().splitlines() if s.startswith('H3_COMPLETE '));clip=Path(line[len('H3_COMPLETE '):])
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(clip)],text=True));v=next(s for s in probe['streams'] if s['codec_type']=='video');n=int(v['nb_frames'])
 assert v['width']==576 and v['height']==1024 and n>=x['production_frames']
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(clip),'-f','null','-'],check=True)
 sel='+'.join(f'eq(n\\,{round((n-1)*q)})' for q in [0,.125,.25,.375,.5,.625,.75,.875,1])
 contact=review/f'shot_{sid}_h3.jpg';subprocess.run(['ffmpeg','-v','error','-y','-i',str(clip),'-vf',f'select={sel},scale=180:320,tile=9x1','-frames:v','1',str(contact)],check=True)
 m[sid]={'clip':str(clip.relative_to(ROOT)),'sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'reference':x['reference_image'],'reference_sha256':x['reference_sha256'],'frames':n,'target_frames':x['production_frames'],'decode':True,'accepted':False,'contact':str(contact.relative_to(P))}
 manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print('DONE '+sid,flush=True)
