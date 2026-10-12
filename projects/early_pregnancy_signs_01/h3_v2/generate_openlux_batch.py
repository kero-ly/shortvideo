"""Invoke the user's OpenLux skill for explicitly selected independent shots.

Run locally with uv run --no-project --with requests python ... 03 05.
No automatic retry; existing outputs are skipped and provider errors halt new calls.
"""
import concurrent.futures,hashlib,json,subprocess,sys,threading,time
from pathlib import Path
P=Path(__file__).resolve().parent
HELPER=Path('/Users/ly/.codex/skills/openlux-gpt-image/scripts/openlux_image.py')
stop=threading.Event()
def one(sid):
    if stop.is_set():return
    output=P/f'references/shots/openlux_shot_{sid}_v1.png'
    if output.exists():print('EXISTS '+sid,flush=True);return
    prompt=(P/f'prompts/shot_{sid}_image.txt').read_text()
    prompt+='\n关键：保留上传图中的同一个人物身份、头发长度与分缝、服装款式和配色、绘画线条与阴影风格；只改变姿势、表情、道具、构图和场景。输出必须是单个场景，不保留原来的白底立绘布局。'
    args=[sys.executable,str(HELPER),'--mode','edit','--image',str(P/'references/character/openlux_character_master_v1.png'),'--prompt',prompt,'--size','1024x1536','--quality','high','--timeout','600','--output',str(output)]
    print('START '+sid,flush=True)
    r=subprocess.run(args,capture_output=True,text=True)
    audit={'shot':sid,'source':'references/character/openlux_character_master_v1.png','prompt':prompt,'returncode':r.returncode,'provider_response':r.stdout,'error':r.stderr}
    if output.exists():audit['sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
    (P/f'review/openlux_shot_{sid}_v1.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
    print(sid,r.stdout or r.stderr,flush=True)
    if r.returncode:stop.set();raise RuntimeError('OpenLux failed; no retry: '+sid)
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures=[ex.submit(one,x.zfill(2)) for x in sys.argv[1:]]
        for f in concurrent.futures.as_completed(futures):f.result()
