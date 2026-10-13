"""Bounded OpenLux edits from original scene refs. No automatic paid retries."""
from pathlib import Path
import argparse,subprocess,sys,json,datetime,hashlib
from concurrent.futures import ThreadPoolExecutor,as_completed
from PIL import Image
P=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--shots',nargs='+',required=True);parser.add_argument('--workers',type=int,default=1);args=parser.parse_args()
assert 1<=args.workers<=3
board=json.loads((P/'storyboard/draft-v2.json').read_text())
shots=[x for x in board['shots'] if x['id'] in args.shots];assert len(shots)==len(args.shots)
job='reference-extension-v2-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
r=P/'runs'/job;r.mkdir(parents=True,exist_ok=False)
print(json.dumps({'job':job,'shots':args.shots,'workers':args.workers},ensure_ascii=False),flush=True)
def generate(shot):
 sid=shot['id'];out=r/(sid+'-raw.png');prompt=P/'prompts/shots'/(sid+'-image-v2.txt')
 target=P/'references/shots/v2'/(sid+'.png');assert not target.exists(),str(target)
 result=subprocess.run([sys.executable,'/Users/ly/.codex/skills/openlux-gpt-image/scripts/openlux_image.py','--mode','edit','--image',str(P/shot['reference_source']),'--prompt',prompt.read_text(),'--size','1024x1792','--quality','high','--output',str(out),'--timeout','240'],capture_output=True,text=True)
 (r/(sid+'-result.log')).write_text(result.stdout+'\n'+result.stderr)
 rec={'shot':sid,'job':job,'input':shot['reference_source'],'input_sha256':shot['reference_input_sha256'],'prompt':str(prompt.relative_to(P)),'log':str((r/(sid+'-result.log')).relative_to(P)),'exit_code':result.returncode,'status':'failed','output':None,'automatic_retry':False}
 if result.returncode==0:
  response=json.loads(result.stdout);im=Image.open(out);im.verify();target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(out.read_bytes())
  rec.update(status='generated_pending_visual_review',output=str(target.relative_to(P)),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),actual_size=list(Image.open(target).size),response=response)
 else:rec['error']=result.stderr.strip()
 (r/(sid+'-manifest.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 return rec
all_records=[]
with ThreadPoolExecutor(max_workers=args.workers) as pool:
 futures={pool.submit(generate,shot):shot for shot in shots}
 for fut in as_completed(futures):
  try:rec=fut.result()
  except Exception as e:rec={'shot':futures[fut]['id'],'status':'local_error','error':str(e)}
  all_records.append(rec);print(json.dumps(rec,ensure_ascii=False),flush=True)
  for shot in board['shots']:
   if shot['id']==rec['shot']:
    shot['reference_frame_status']=rec['status'];shot['reference_frame']=rec.get('output');shot['generation_evidence']=str((r/(rec['shot']+'-manifest.json')).relative_to(P))
    if rec.get('sha256'):shot['reference_frame_sha256']=rec['sha256'];shot['actual_size']=rec['actual_size']
  (P/'storyboard/draft-v2.json').write_text(json.dumps(board,ensure_ascii=False,indent=2)+'\n')
(r/'batch-manifest.json').write_text(json.dumps(all_records,ensure_ascii=False,indent=2)+'\n')
print('batch complete',flush=True)
