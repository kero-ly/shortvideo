import json,re,difflib,hashlib,subprocess
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];assert str(ROOT)=='/home/ly/shortvideo'
t=json.loads((P/'timeline/audio-v4.json').read_text());cache=ROOT/'.cache/asr-model-cache/models--Systran--faster-whisper-small/snapshots';model=WhisperModel(str(next(cache.iterdir())),device='cpu',compute_type='int8',cpu_threads=6)
clean=lambda s:re.sub(r'[^\u4e00-\u9fff0-9]','',s)
cues=[];evidence=[];maps=[]
for shot in t['shots']:
 audio=P/shot['audio'];assert hashlib.sha256(audio.read_bytes()).hexdigest()==shot['sha256']
 samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32)
 attempts=[];candidates=[]
 for prompt in [shot['text'],None]:
  segs,info=model.transcribe(samples,language='zh',word_timestamps=True,beam_size=5,vad_filter=False,initial_prompt=prompt)
  candidate=[{'text':w.word,'start':float(w.start),'end':float(w.end)} for seg in segs for w in (seg.words or [])]
  score=difflib.SequenceMatcher(None,clean(shot['text']),clean(''.join(w['text'] for w in candidate)),autojunk=False).ratio()
  attempts.append({'prompt':prompt,'similarity':score,'word_count':len(candidate)});candidates.append((score,candidate))
  if score>=.98:break
 words=max(candidates,key=lambda x:x[0])[1]
 assert words,shot['id'];spoken='';owners=[]
 for i,w in enumerate(words):
  for c in clean(w['text']):spoken+=c;owners.append(i)
 locked=clean(shot['text']);match=difflib.SequenceMatcher(None,locked,spoken,autojunk=False);mapping={}
 for block in match.get_matching_blocks():
  for k in range(block.size):mapping[block.a+k]=owners[block.b+k]
 # Matched actual words bound each semantic phrase; no proportional timing allocation.
 cursor=0;shotcues=[]
 phrases=[x for x in re.findall(r'[^，。？！：；]+[，。？！：；]?',shot['text']) if clean(x)]
 for pi,phrase in enumerate(phrases):
  n=len(clean(phrase));inds=sorted(set(mapping[k] for k in range(cursor,cursor+n) if k in mapping));cursor+=n
  assert inds,('Unaligned phrase',shot['id'],phrase)
  if pi==0:inds=sorted(set([0]+inds))
  if pi==len(phrases)-1:inds=sorted(set(inds+[len(words)-1]))
  start=shot['audio_start']+words[inds[0]]['start'];end=shot['audio_start']+words[inds[-1]]['end']
  shotcues.append({'shot_id':shot['id'],'text':phrase,'start':round(start,3),'end':round(end,3),'source_indices':inds})
 for i,c in enumerate(shotcues):c['end']=round(min(shotcues[i+1]['start'] if i+1<len(shotcues) else (shot['start']+shot['frames'])/24-.04,max(c['end']+.12,c['start']+.3)),3)
 cues+=shotcues;evidence.append({'shot_id':shot['id'],'audio_sha256':shot['sha256'],'words':words,'recognition_attempts':attempts,'similarity':match.ratio(),'differences':[{'kind':tag,'locked':locked[a:b],'recognized':spoken[c:d]} for tag,a,b,c,d in match.get_opcodes() if tag!='equal']})
 maps.append({'shot_id':shot['id'],'original_screen_text':shot['screen_text'],'destination':'week heading plus complete narration cues; no duplicated screen paragraph','cue_indices':list(range(len(cues)-len(shotcues),len(cues)))})
 print(shot['id'],match.ratio(),flush=True)
(P/'timeline/captions-v4.json').write_text(json.dumps({'engine':'faster-whisper small CPU int8; matched real word boundaries','narration_sha256':t['narration_sha256'],'cues':cues},ensure_ascii=False,indent=2))
(P/'review/alignment-evidence-v4.json').write_text(json.dumps({'shots':evidence,'semantic_mapping':maps,'listening':'pending'},ensure_ascii=False,indent=2))
def stamp(s):
 ms=round(s*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(P/'timeline/captions-v4.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
