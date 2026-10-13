import json,time,subprocess,hashlib
from pathlib import Path
P=Path('/Users/ly/Desktop/project/shortvideo/projects/怀孕1-12周变化');R=P.parents[1];remote='/home/ly/shortvideo/projects/怀孕1-12周变化'
# One finite production task. Rendering and audio/model work stay on 220.
status=P/'review/v5-job-local.log'
with status.open('w') as log:
 deadline=time.time()+7200
 while time.time()<deadline:
  x=subprocess.run(['ssh','ly@8.92.9.220','cat '+remote+'/review/latest-delivery-v5.txt'],capture_output=True,text=True)
  if x.returncode==0 and x.stdout.strip():delivery=x.stdout.strip();break
  time.sleep(30)
 else:raise RuntimeError('Timed out waiting for admitted production task')
 subprocess.run(['ssh','ly@8.92.9.220','cd /home/ly/shortvideo && uv run --with numpy python projects/怀孕1-12周变化/scripts/verify_delivery_v5.py'],stdout=log,stderr=log,check=True)
 d=P/delivery;d.mkdir(parents=True,exist_ok=True)
 subprocess.run(['rsync','-a','--exclude','visual.mp4','ly@8.92.9.220:'+remote+'/'+delivery+'/',str(d)+'/'],stdout=log,stderr=log,check=True)
 for name in ['delivery-qa-v5.json','delivery-manifest-v5.json','latest-delivery-v5.txt','latest-compose-v5.txt','audio-evidence-v5.json','alignment-evidence-v5.json','latest-audio-v5.txt']:
  subprocess.run(['rsync','-a','ly@8.92.9.220:'+remote+'/review/'+name,str(P/'review')+'/'],stdout=log,stderr=log,check=True)
 for name in ['audio-v5.json','captions-v5.json','captions-v5.srt']:
  subprocess.run(['rsync','-a','ly@8.92.9.220:'+remote+'/timeline/'+name,str(P/'timeline')+'/'],stdout=log,stderr=log,check=True)
 m=json.loads((d/'manifest.json').read_text())
 for f in d.iterdir():
  if f.name!='manifest.json':assert hashlib.sha256(f.read_bytes()).hexdigest()==m[f.name]['sha256'],f.name
 subprocess.run(['python3',str(P/'scripts/build_video_review_v5.py')],cwd=R,stdout=log,stderr=log,check=True)
 (P/'review/v5-local-download.json').write_text(json.dumps({'delivery':delivery,'downloaded_sha256_verified':True,'visual_sampling':'pending','actual_listening':'pending'},ensure_ascii=False,indent=2))
 print('LOCAL_DELIVERY_READY '+str(d),file=log,flush=True)
