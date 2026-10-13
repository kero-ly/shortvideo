import json,re,hashlib,subprocess
from pathlib import Path
import numpy as np
P=Path('/home/ly/shortvideo/projects/怀孕1-12周变化');d=P/'deliveries/revision-v3-20261014-025947-ece0';job=P/'runs'/d.name
q=json.loads((d/'qa.json').read_text());l=json.loads(re.search(r'\{\s*"input_i".*?\}',(d/'loudness.log').read_text(),re.S).group());assert -19<=float(l['input_i'])<=-13;assert float(l['input_tp'])<=-1
assert not re.search(r'black_start:',(d/'blackdetect.log').read_text())
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-f','f32le','-ac','1','-ar','48000','-']),dtype=np.float32)
a=pcm(d/'怀孕1-12周变化-v3.mp4');b=pcm(job/'mix.wav');n=min(len(a),len(b));corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.99
q['technical'].update({'integrated_lufs':float(l['input_i']),'true_peak_dbtp':float(l['input_tp']),'black_intervals':0,'final_audio_correlation_with_approved_mix':corr});q['visual_sampling']={'reviewer':'Codex','scope':'16 midpoint preview frames, 4x4 mobile-scale contact sheet','result':'top-left note and centered upper-middle captions visible; sampled captions do not overlap faces','limits':'not full playback; first/end/action frames not inspected'}
(d/'qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2));m={x.name:{'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'bytes':x.stat().st_size}for x in d.iterdir()if x.is_file()and x.name!='manifest.json'};(d/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
for name,target in [('qa.json','delivery-qa-v3.json'),('manifest.json','delivery-manifest-v3.json')]: (P/'review'/target).write_bytes((d/name).read_bytes())
print(json.dumps(q,ensure_ascii=False))
