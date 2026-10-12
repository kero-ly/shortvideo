"""220-only semantic caption rebuild, audio provenance audit, and voiced review."""
import difflib, hashlib, html, json, re, subprocess, time, uuid
from pathlib import Path

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
assert str(ROOT) == '/home/ly/shortvideo', 'Production belongs on 220'
job = ROOT / 'runs' / ('storybook-caption-fusion-' + time.strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:4])
job.mkdir()
print('JOB ' + str(job), flush=True)
props = json.loads((ROOT / 'runs/storybook-caption-restored-20261013-072152-12b7/props.json').read_text())
old = props['captions']
audio = ROOT / 'runs/storybook-audio-20261013-065657-a25b/narration.wav'
asr_audio = ROOT / 'runs/early-pregnancy-20261013-010143-e9a8/narration.wav'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(audio) == sha(asr_audio), 'Cannot reuse ASR timestamps for different audio'
asr_path = ROOT / 'runs/migration-backup-20261013/early_pregnancy_signs_01/asr.json'
asr = json.loads(asr_path.read_text())
clean = lambda s: re.sub(r'[^\u4e00-\u9fff0-9]', '', s).replace('21', '二十一')
spoken, times = '', []
for segment in asr:
    for word in segment['words']:
        chars = clean(word['word'])
        for i, c in enumerate(chars):
            spoken += c
            times.append((word['start'] + (word['end']-word['start'])*i/len(chars), word['start'] + (word['end']-word['start'])*(i+1)/len(chars)))
locked = ''.join(clean(s['text']) for s in props['scenes'])
assert locked == ''.join(clean(c['text']) for c in old), 'Old captions omit narration'
match = difflib.SequenceMatcher(None, locked, spoken, autojunk=False)
mapping, differences = {}, []
for tag, a, b, c, d in match.get_opcodes():
    if tag == 'equal':
        for i in range(b-a): mapping[a+i] = times[c+i]
    else:
        differences.append({'script': locked[a:b], 'asr': spoken[c:d], 'kind': tag, 'start': times[min(c,len(times)-1)][0]})
        left = times[min(c,len(times)-1)][0]
        right = times[d-1][1] if d > c else left
        for i in range(b-a): mapping[a+i] = (left+(right-left)*i/max(1,b-a), left+(right-left)*(i+1)/max(1,b-a))

# Group by a complete thought; source indices make fusion auditable.
groups = [[0,1],[2],[3,4],[5],[6,7],[8],[9,10],[11],[12],[13],[14],[15],[16,17],[18,19],[20],[21,22],[23],[24],[25,26],[27],[28,29],[30],[31],[32],[33,34],[35],[36,37],[38,39],[40,41]]
assert [i for g in groups for i in g] == list(range(42))
contexts = ['', '', '', '', '① 月经推迟', '', '② 容易累', '', '③ 乳房胀痛或敏感', '', '④ 恶心', '', '⑤ 对气味更敏感', '', '', '⑦ 口味变化', '', '⑧ 情绪起伏', '症状不是答案', '症状不是答案', '下一步：验孕', '验孕时间', '验孕时间', '月经日期不清楚时', '', '阴性，但月经没来？', '复测后的下一步', '就医提醒', '']
sentence_texts = [
 '月经还没来，身体又有点不一样？','先别急着猜答案。','早孕可能有这些变化，\n但每个人都不一样。',
 '第一，月经推迟。','尤其平时周期比较规律时，\n值得留意。',
 '第二，容易累。','平常做完不费力的事，\n也想坐下来歇一歇。',
 '第三，乳房胀痛或变得敏感。','不过，经前也可能这样。',
 '第四，恶心。','它不一定只在早晨出现。',
 '第五，对气味更敏感。','熟悉的味道，\n突然觉得受不了。',
 '第六，上厕所比平时频繁，\n尤其是小便次数增多。',
 '第七，口味变了。','以前爱吃的食物，\n现在可能不想碰。',
 '第八，情绪起伏比平时明显，','也可能只是众多变化之一。',
 '但请记住，有几条\n都不能直接说明怀孕，','没有这些反应也不能排除。','最可靠的下一步，\n是按说明做一次验孕。',
 '通常从月经推迟的\n第一天开始测。','如果不知道\n月经什么时候来，','就在上次无保护性行为\n至少二十一天后测。',
 '测得太早是阴性，\n月经又没来？','过几天再测一次。','第二次仍是阴性、月经还没来，\n可以咨询医生。',
 '要是出现明显腹痛或阴道出血，\n请及时就医。','先确认，再决定下一步，\n不用一个人靠猜。'
]
assert len(groups) == len(contexts) == len(sentence_texts)
assert ''.join(clean(t) for t in sentence_texts) == locked
offsets, cursor = [], 0
for c in old:
    offsets.append((cursor, cursor+len(clean(c['text'])))); cursor = offsets[-1][1]
captions = []
for indices, context, text in zip(groups, contexts, sentence_texts):
    s = next(s for s in props['scenes'] if s['start']/24 <= old[indices[0]]['start'] < (s['start']+s['frames'])/24)
    first, last = offsets[indices[0]][0], offsets[indices[-1]][1]-1
    speech_start, speech_end = mapping[first][0], mapping[last][1]
    assert speech_end > speech_start
    start = max(s['start']/24, speech_start)
    captions.append({'text':text,'context':context,'start':round(start,3),'end':round(min(speech_end+.12,(s['start']+s['frames'])/24-.04),3),'speech_start':speech_start,'speech_end':speech_end,'source_indices':indices,'shot_id':s['shot_id']})
for i,c in enumerate(captions):
    s = next(s for s in props['scenes'] if s['shot_id']==c['shot_id'])
    # Hold through punctuation pauses to avoid flicker; don't advance the next spoken sentence.
    c['end'] = round(captions[i+1]['start'] if i+1<len(captions) and captions[i+1]['shot_id']==c['shot_id'] else (s['start']+s['frames'])/24-.04,3)
    assert c['start'] < c['end'] and c['end'] >= c['speech_end']-.08
    assert max(len(line) for line in c['text'].splitlines()) <= 17, c
props.update(captions=captions,subtitleLayout='lower-fused',caption_alignment='Exact same narration SHA256 as original ASR; complete thought grouping, per-cue word timestamps; human hearing review pending')
(job/'props.json').write_text(json.dumps(props,ensure_ascii=False,indent=2))
coverage=[]
for s in props['scenes']:
    cs=[c for c in captions if c['shot_id']==s['shot_id']]
    assert clean(s['text'])==''.join(clean(c['text']) for c in cs)
    coverage.append({'shot_id':s['shot_id'],'upper_title':s['title'],'upper_note':s['note'],'narration':s['text'],'cues':cs,'fusion':'标题主题融入第一句及后续下方短标签；与旁白同义的说明以完整句保留。未口播的休息/关怀语不伪装成逐字字幕。关键事实已由旁白字幕完整表达。'})
audit={'status':'automatic_alignment_checked_human_review_pending','audio_sha256':sha(audio),'asr_audio_sha256':sha(asr_audio),'asr_json_sha256':sha(asr_path),'reused_asr_reason':'The current narration WAV and ASR source WAV are byte-identical, checked on 220 in this job','asr_similarity':match.ratio(),'asr_differences':differences,'old_cues':42,'new_cues':len(captions),'complete_script_coverage':True,'complete_source_index_coverage':True,'scene_boundaries_checked':True,'full_listening_completed':False,'limitations':'ASR word boundaries are estimates, not ear-verified timing. Homophone substitutions need review. Scene audio duration alone does not prove cue synchronization.','scenes':coverage}
(job/'caption-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print('AUDIT_READY '+str(job),flush=True)
renderer=ROOT/'renderers/remotion'
def run(stage,cmd,cwd=None):
    print(stage,flush=True)
    with (job/(stage+'.log')).open('w') as log: subprocess.run(list(map(str,cmd)),cwd=cwd,stdout=log,stderr=subprocess.STDOUT,check=True)
run('render',[renderer/'node_modules/.bin/remotion','render','src/StorybookExplainer.jsx','StorybookExplainer',job/'visual.mp4','--props',job/'props.json','--scale','.5','--concurrency','3','--codec','h264'],renderer)
duration=props['durationInFrames']/24
run('mix',['ffmpeg','-y','-i',job/'visual.mp4','-i',ROOT/props['mix_path'],'-c:v','copy','-c:a','aac','-t',duration,'-movflags','+faststart',job/'preview.mp4'])
run('decode',['ffmpeg','-v','error','-xerror','-i',job/'preview.mp4','-f','null','-'])
for s in props['scenes']:
    cs=[c for c in captions if c['shot_id']==s['shot_id']]
    c=cs[min(1,len(cs)-1)]
    run('frame-'+s['shot_id'],['ffmpeg','-y','-ss',(c['start']+c['end'])/2,'-i',job/'preview.mp4','-frames:v','1',job/('shot-'+s['shot_id']+'.png')])
run('contact',['ffmpeg','-y','-framerate','1','-start_number','1','-i',job/'shot-%02d.png','-vf','scale=270:480,tile=5x3','-frames:v','1',job/'contact.png'])
def stamp(t):
    n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
(job/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(captions)))
sections=''
for s in coverage:
    cues=''.join(f'<tr><td>{c["start"]:.3f}–{c["end"]:.3f}</td><td>{html.escape(c["context"])}</td><td>{html.escape(c["text"]).replace(chr(10),"<br>")}</td><td><button onclick="seek({c["start"]})">播放此句</button></td></tr>' for c in s['cues'])
    sections+=f'<section><h2>{s["shot_id"]} · {html.escape(s["upper_title"])}</h2><p>原上方说明：{html.escape(s["upper_note"])}</p><p>{html.escape(s["fusion"])}</p><table><thead><tr><th>显示时间</th><th>同块主题标签</th><th>完整旁白字幕</th><th>听审</th></tr></thead><tbody>{cues}</tbody></table></section>'
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>字幕融合与语音对齐 · 完整审阅</title><style>body{margin:0;background:#fff4de;color:#684630;font:16px system-ui}main{max-width:1080px;margin:auto;padding:24px}video{width:360px;max-width:100%;max-height:75vh}section{margin:24px 0;padding:18px;background:#fff9ee;border-radius:16px}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:12px;border-bottom:1px solid #ddcbbb}p{line-height:1.8}button{padding:8px;color:inherit;cursor:pointer}#player{position:sticky;top:0;background:#fff4de;z-index:2;display:flex;gap:24px;flex-wrap:wrap;padding:10px}</style><main><h1>字幕融合与语音对齐 · 完整审阅</h1><div id="player"><video controls playsinline preload="metadata" src="preview.mp4"></video><aside><p>下方一个字幕块：短主题标签＋完整语义字幕。<br>已含主题的开场句不重复标签。<br>42个碎片字幕重组为29个语义段。<br>保持同镜停顿期间稳定，按实际语音切换。</p><p>当前旁白与原ASR源WAV哈希完全一致。<br>已检查全稿覆盖、词级时间及镜头边界。<br>尚未完成逐句耳听验收；自动结果不能代替听审。</p><a href="caption-audit.json">对齐与内容核对记录</a> · <a href="subtitles.srt">SRT</a></aside></div>'''+sections+'''</main><script>function seek(t){const v=document.querySelector('video');v.currentTime=t;v.play();}</script></html>'''
(job/'index.html').write_text(page)
(job/'manifest.json').write_text(json.dumps({'status':'voiced_preview_pending_review','host':'220','files':{p.name:sha(p) for p in job.iterdir() if p.suffix in ('.mp4','.png','.json','.srt','.html') and p.name!='manifest.json'}},ensure_ascii=False,indent=2))
(P/'review/latest-fused-caption.txt').write_text(str(job))
print('REVIEW_READY '+str(job),flush=True)
