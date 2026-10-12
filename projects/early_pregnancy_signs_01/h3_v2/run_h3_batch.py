"""Serial H3 submission for reviewed references; preserve every task and output."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
timeline=json.loads((P.parent/'aligned-props.json').read_text())
out=P/'generated/h3';out.mkdir(parents=True,exist_ok=True)
manifest_path=P/'review/h3-clips.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
for sid in sys.argv[1:]:
    sid=sid.zfill(2);name='shot_'+sid
    if name in manifest and (ROOT/manifest[name]['clip']).is_file():print('RECORDED '+name,flush=True);continue
    image=P/f'references/shots/openlux_shot_{sid}_v1.png'
    assert image.is_file(),f'Missing reviewed reference {image}'
    frames=timeline['scenes'][int(sid)-1]['frames']
    log=out/f'{name}-{time.strftime("%Y%m%d-%H%M%S")}.log'
    cmd=[sys.executable,str(ROOT/'capabilities/video-generation/h3_comfy.py'),'--image',str(image),'--prompt-file',str(P/f'prompts/shot_{sid}_h3.txt'),'--shot','pregnancy-'+sid,'--frames',str(frames),'--width','576','--height','1024','--seed',str(20261013+int(sid))]
    print('START '+name,flush=True)
    with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
    if r.returncode:raise RuntimeError('H3 failed or busy: inspect '+str(log)+'; do not automatically retry')
    lines=log.read_text().splitlines();clip=Path(next(x.removeprefix('H3_COMPLETE ') for x in lines if x.startswith('H3_COMPLETE ')))
    manifest[name]={'clip':str(clip.relative_to(ROOT)),'sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'image':str(image.relative_to(ROOT)),'reference_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'target_frames':frames,'review':'pending video review'}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print('DONE '+name,flush=True)
