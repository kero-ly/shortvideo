"""Record observed v10 review evidence and refresh the delivery manifest on 220."""
import hashlib
import json
import shutil
from pathlib import Path

E = Path('/home/ly/shortvideo/projects/heart_circulation_mechanism_04')
D = E / 'deliveries/20261013-heart-v10'
qa = json.loads((D/'qa.json').read_text())
qa['visual'] = 'Reviewed all five shot start/middle/end frames and frames 240,280,410,470,499,500,510,521,532,542,695,725. Bold chevrons follow blood tracks; rounded breathing corner brackets; body silhouette and abdominal vessel expansion; title/captions readable.'
qa['full_playback'] = {'status':'completed in IAB', 'duration':28.066667, 'currentTime':28.066667, 'ended':True, 'videoWidth':1080, 'videoHeight':1920, 'error':None}
qa['actual_listening'] = 'pending user review; browser playback is not auditory review'
qa['media_sync'] = '45 delivery file SHA256 values checked locally against server manifest before review finalization; timing/captions/audio source files byte-identical to v9'
(D/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
manifest = json.loads((D/'manifest.json').read_text())
manifest['files'] = [dict(path=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(D.iterdir()) if p.is_file() and p.name!='manifest.json']
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for name in ['qa','manifest','sources']:
    shutil.copy2(D/f'{name}.json',E/f'review/v10-{name}.json')
print('Review evidence saved; manifest refreshed.')
