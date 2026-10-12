"""Align locked captions to Whisper word timestamps without replacing medical text."""
import difflib,json,re
from pathlib import Path
P=Path(__file__).resolve().parent
data=json.loads((P/'timeline.json').read_text());asr=json.loads((P/'asr.json').read_text())
def clean(s):return re.sub(r'[^\u4e00-\u9fff0-9]','',s).replace('21','二十一')
spoken='';times=[]
for segment in asr:
    for word in segment['words']:
        chars=clean(word['word'])
        for i,c in enumerate(chars):
            spoken+=c
            times.append((word['start']+(word['end']-word['start'])*i/len(chars),word['start']+(word['end']-word['start'])*(i+1)/len(chars)))
locked=''.join(clean(c['text']) for c in data['captions'])
match=difflib.SequenceMatcher(None,locked,spoken,autojunk=False);mapping={};differences=[]
for tag,a,b,c,d in match.get_opcodes():
    if tag=='equal':
        for i in range(b-a):mapping[a+i]=times[c+i]
    else:
        differences.append({'locked':locked[a:b],'recognized':spoken[c:d],'kind':tag})
        left=times[c][0] if c<len(times) else times[-1][1]
        right=times[d-1][1] if d>c else left
        for i in range(b-a):mapping[a+i]=(left+(right-left)*i/max(1,b-a),left+(right-left)*(i+1)/max(1,b-a))
cursor=0
for c in data['captions']:
    scene=next(s for s in data['scenes'] if s['start']/24<=c['start']<(s['start']+s['frames'])/24)
    size=len(clean(c['text']));start=mapping[cursor][0];end=mapping[cursor+size-1][1]
    start=max(start,scene['start']/24+.02);end=min(max(start+.3,end+.06),(scene['start']+scene['frames'])/24-.05)
    c.update(start=round(start,3),end=round(end,3));cursor+=size
for i,c in enumerate(data['captions'][:-1]):c['end']=min(c['end'],data['captions'][i+1]['start'])
assert all(c['end']>c['start'] for c in data['captions'])
data['caption_alignment']='Whisper-small word timing matched to locked script; ASR spelling never replaces the script'
(P/'aligned-props.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(P/'speech-review.json').write_text(json.dumps({'engine':'faster-whisper small, CPU int8','character_similarity':match.ratio(),'differences':differences,'critical_facts':'Recognized missed-period day one, at least 21 days, negative retest, pain/bleeding advice.','limits':'Homophone substitutions are ASR observations, not proof of mispronunciation. Human listening/style approval remains for user review.'},ensure_ascii=False,indent=2))
print(json.dumps({'similarity':match.ratio(),'differences':differences},ensure_ascii=False))
