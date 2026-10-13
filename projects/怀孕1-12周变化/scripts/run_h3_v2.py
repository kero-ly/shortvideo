import hashlib,json,subprocess,sys,time,uuid,urllib.request
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo'
assert json.loads((P/'production-plan.json').read_text())['status']=='production_approved'
b=json.loads((P/'storyboard/approved-v2.json').read_text());t=json.loads((P/'timeline/audio-v2.json').read_text())
f=P/'review/h3-clips-v2.json';m=json.loads(f.read_text()) if f.exists() else {}
for sid in sys.argv[1:]:
 if sid in m:print('RECORDED '+sid,flush=True);continue
 x=next(x for x in b['shots'] if x['id']==sid);a=next(x for x in t['shots'] if x['id']==sid);image=P/x['reference_frame']
 assert hashlib.sha256(image.read_bytes()).hexdigest()==x['reference_frame_sha256']
 job=P/'runs'/('h3-submit-'+sid+'-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir()
 rows=subprocess.check_output(['nvidia-smi','--query-gpu=index,memory.free,utilization.gpu','--format=csv,noheader,nounits'],text=True);(job/'gpu-preflight.txt').write_text(rows)
 queue=json.load(urllib.request.urlopen('http://127.0.0.1:8199/queue',timeout=10));assert not queue['queue_running'] and not queue['queue_pending'],'Shared queue busy; nothing submitted'
 print('START '+sid+' '+str(job),flush=True)
 cmd=[sys.executable,str(P/'scripts/h3_episode.py'),'--image',str(image),'--prompt-file',str(P/f'prompts/shots/{sid}-motion-v2.txt'),'--shot',sid,'--frames',str(a['production_frames']),'--width','576','--height','1024','--seed',str(20261030+int(sid[-2:]))]
 with (job/'submit.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError('Inspect '+str(job/'submit.log')+'; no automatic resubmission')
 clip=Path(next(l for l in (job/'submit.log').read_text().splitlines() if l.startswith('H3_COMPLETE '))[12:])
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(clip)],text=True));v=next(v for v in probe['streams'] if v['codec_type']=='video');n=int(v['nb_frames']);assert v['width']==576 and v['height']==1024 and n>=a['frames']
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(clip),'-f','null','-'],check=True)
 select='+'.join(f'eq(n\\,{round((n-1)*q)})' for q in [0,.125,.25,.375,.5,.625,.75,.875,1]);contact=job/'motion-contact.jpg'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(clip),'-vf',f'select={select},scale=216:384,tile=9x1','-frames:v','1',str(contact)],check=True)
 m[sid]={'clip':str(clip.relative_to(P)),'sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'reference':x['reference_frame'],'reference_sha256':x['reference_frame_sha256'],'frames':n,'target_frames':a['frames'],'decode':True,'accepted':False,'contact':str(contact.relative_to(P))}
 f.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print('DONE '+sid,flush=True)
