"""Extract five frames and validate every recorded H3 clip without re-generation."""
import json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
m=json.loads((P/'review/h3-clips.json').read_text())
report={}
for key,x in sorted(m.items()):
 clip=ROOT/x['clip'];probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(clip)],text=True));v=next(s for s in probe['streams'] if s['codec_type']=='video');n=int(v['nb_frames'])
 assert v['width']==576 and v['height']==1024 and v['r_frame_rate']=='24/1',(key,v)
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(clip),'-f','null','-'],check=True)
 select='+'.join(f'eq(n\\,{round((n-1)*fraction)})' for fraction in [0,.25,.5,.75,1])
 target=P/f'review/{key}_h3.jpg'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(clip),'-vf',f'select={select},scale=216:384,tile=5x1','-frames:v','1',str(target)],check=True)
 report[key]={'frames':n,'seconds':float(probe['format']['duration']),'resolution':[v['width'],v['height']],'full_decode':True,'contact':str(target.relative_to(P))}
(P/'review/h3-technical.json').write_text(json.dumps(report,indent=2))
print('H3 clips decoded and five-frame contacts generated:',len(report))
