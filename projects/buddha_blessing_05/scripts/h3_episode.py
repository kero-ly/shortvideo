"""Submit a single local reference image to observed ComfyUI FL2VA nodes.

Use from 220 with uv run python; no model installation or shared process changes.
Jobs are unique; POST is never retried automatically. Resume by --resume-job.
"""
import argparse, hashlib, json, math, sys, time, urllib.request, urllib.parse, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
EPISODE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'pipeline'))
from gpu_lock import acquire

def request(base,path,data=None,headers=None,timeout=60):
    req=urllib.request.Request(base+path,data=data,headers=headers or {})
    with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)

def post(base,path,value):
    return request(base,path,json.dumps(value).encode(),{'Content-Type':'application/json'})

def upload(base,image):
    boundary='factory'+uuid.uuid4().hex
    name='factory_'+hashlib.sha256(image.read_bytes()).hexdigest()[:16]+'.png'
    body=(f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{name}"\r\nContent-Type: image/png\r\n\r\n').encode()+image.read_bytes()+f'\r\n--{boundary}--\r\n'.encode()
    out=request(base,'/upload/image',body,{'Content-Type':'multipart/form-data; boundary='+boundary})
    return (out.get('subfolder','')+'/'+out['name']).lstrip('/')

def main():
    p=argparse.ArgumentParser();p.add_argument('--image',type=Path);p.add_argument('--prompt-file',type=Path);p.add_argument('--shot',default='shot');p.add_argument('--frames',type=int,default=124);p.add_argument('--width',type=int,default=576);p.add_argument('--height',type=int,default=1024);p.add_argument('--seed',type=int,default=20261013);p.add_argument('--url',default='http://127.0.0.1:8199');p.add_argument('--resume-job',type=Path)
    p.add_argument('--graph',type=Path,default=ROOT/'capabilities/video-generation/h3_turbo8.json')
    a=p.parse_args();lock=acquire(ROOT/'.runtime/gpu-job.lock')
    if a.resume_job:
        job=a.resume_job;record=json.loads((job/'submission.json').read_text());pid=record['prompt_id']
    else:
        if not a.image or not a.prompt_file:raise ValueError('image and prompt-file required')
        if a.width%32 or a.height%32:raise ValueError('H3 dimensions must be multiples of 32')
        queue=request(a.url,'/queue')
        if queue.get('queue_running') or queue.get('queue_pending'):raise RuntimeError('Shared H3 queue is busy; nothing submitted')
        job=EPISODE/'runs'/('h3-'+a.shot+'-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:4]);job.mkdir(parents=True)
        graph=json.loads(a.graph.read_text())
        frame_count=5+17*math.ceil((max(124,a.frames)-5)/17)
        remote=upload(a.url,a.image)
        graph['300']={'class_type':'LoadImage','inputs':{'image':remote}}
        graph['104']['inputs'].update(prompt=a.prompt_file.read_text(),width=a.width,height=a.height,length=frame_count,first_frame=['300',0])
        graph['15']['inputs']['noise_seed']=a.seed
        graph['92']['inputs']['filename_prefix']='shortvideo-factory/'+job.name
        # Native generated audio is omitted: this episode uses separate narration.
        graph['91']['inputs'].pop('audio',None);graph.pop('23',None);graph.pop('24',None)
        (job/'workflow.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2))
        (job/'input.json').write_text(json.dumps({'image':str(a.image),'sha256':hashlib.sha256(a.image.read_bytes()).hexdigest(),'frames':frame_count,'seed':a.seed,'prompt':a.prompt_file.read_text(),'url':a.url},ensure_ascii=False,indent=2))
        # Save pre-submission state so a network failure does not imply safe retry.
        (job/'status.json').write_text(json.dumps({'stage':'submitting','note':'If interrupted here, inspect service history before resubmitting.'}))
        record=post(a.url,'/prompt',{'prompt':graph,'client_id':job.name})
        (job/'submission.json').write_text(json.dumps(record,indent=2));pid=record['prompt_id']
    print(json.dumps({'job':str(job),'prompt_id':pid}),flush=True)
    start=time.monotonic()
    while time.monotonic()-start<5400:
        history=request(a.url,'/history/'+pid)
        if pid in history:
            entry=history[pid];(job/'history.json').write_text(json.dumps(entry,ensure_ascii=False,indent=2))
            if entry.get('status',{}).get('status_str')=='error':raise RuntimeError('H3 execution failed; inspect '+str(job/'history.json'))
            if entry.get('status',{}).get('completed'):
                outputs=[]
                for node,out in entry.get('outputs',{}).items():
                    for values in out.values():
                        if not isinstance(values,list):continue
                        for item in values:
                            if isinstance(item,dict) and str(item.get('filename','')).lower().endswith('.mp4'):outputs.append(item)
                if not outputs:raise RuntimeError('Completed with no MP4 output; inspect history')
                item=outputs[0];url=a.url+'/view?'+urllib.parse.urlencode({k:item[k] for k in ['filename','subfolder','type'] if k in item})
                with urllib.request.urlopen(url,timeout=180) as r:(job/'clip.mp4').write_bytes(r.read())
                (job/'status.json').write_text(json.dumps({'stage':'completed','prompt_id':pid,'clip':str(job/'clip.mp4'),'elapsed_seconds':time.monotonic()-start},indent=2))
                print('H3_COMPLETE '+str(job/'clip.mp4'),flush=True);return
        if int(time.monotonic()-start)%30<5:print('H3 waiting '+str(round(time.monotonic()-start))+'s',flush=True)
        time.sleep(5)
    raise TimeoutError('H3 still pending; resume the saved prompt_id, do not submit again')

if __name__=='__main__':main()
