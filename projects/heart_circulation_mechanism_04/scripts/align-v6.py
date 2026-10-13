import json,hashlib,re,difflib,subprocess
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
R=Path('/home/ly/shortvideo/projects/heart_circulation_mechanism_04/runs/20261013-heart-v6');p=json.loads((R/'props.json').read_text())
cache=Path('/home/ly/shortvideo/.cache/asr-model-cache/models--Systran--faster-whisper-small/snapshots');m=WhisperModel(str(next(cache.iterdir())),device='cpu',compute_type='int8',cpu_threads=4)
rows=[]
clean=lambda t:re.sub(r'[^\u4e00-\u9fff0-9]','',t)
for s in p['shots']:
 a=R/'audio'/f"{s['id']}.wav";samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(a),'-ar','16000','-ac','1','-f','f32le','-']),dtype='<f4');segs,_=m.transcribe(samples,language='zh',word_timestamps=True,beam_size=5,vad_filter=False,initial_prompt=s['text'])
 words=[dict(text=w.word,start=w.start,end=w.end) for seg in segs for w in (seg.words or [])];assert words
 recognized=''.join(w['text'] for w in words);ratio=difflib.SequenceMatcher(None,clean(s['text']),clean(recognized)).ratio()
 assert words[-1]['end']<=s['audioDuration']+.1
 rows.append(dict(shot_id=s['id'],locked_text=s['text'],recognized_text=recognized,similarity=ratio,words=words,offset=s['audioStart'],sha256=hashlib.sha256(a.read_bytes()).hexdigest()))
 print(s['id'],ratio,flush=True)
(R/'word-alignment.json').write_text(json.dumps(dict(engine='faster-whisper small CPU int8; actual word timestamps, locked script retained',narration_sha256=hashlib.sha256((R/'narration.wav').read_bytes()).hexdigest(),shots=rows,actual_listening='pending'),ensure_ascii=False,indent=2))
