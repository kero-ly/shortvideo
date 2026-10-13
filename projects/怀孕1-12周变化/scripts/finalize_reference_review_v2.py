from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parents[1]
def read(p):return json.loads((P/p).read_text())
def write(p,v):(P/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
s=read('storyboard/draft-v2.json')
assert all(x.get('reference_frame') and (P/x['reference_frame']).exists() for x in s['shots'])
notes=[
'卧室原图延伸，人物服装与主要家具保持；完整站姿，上方留白。',
'夫妻日历场景；日历准确日期和孕周由后期叠加，不能使用生成标记作为日期依据。',
'沙发、水杯、薄毯场景保持；医学气泡已移除。',
'背侧面牵手构图；不强求转脸，以轻握手和呼吸为主。',
'窗边坐姿、宽松衣服，无夸张孕肚。',
'验孕棒有细小灰色标记，不能解读为检测结果；后期不特写诊断条纹。',
'妻子轻掩口，丈夫持水陪伴；手和杯保持轻动作。',
'沙发靠垫、水杯完整；人物手部接触靠垫区域需H3逐帧复核。',
'厨房掩口、小餐陪伴；手持餐盘动作只缓慢放下。',
'厨房妻子已持勺，动作改为轻抬勺，不重复拿起。',
'阅读手册，双人服装保持；书页无医学图示，轻翻页需要动画检查。',
'同一阅读情境，桌面道具与座位保持；鞋款出现差异，后期取中景避开脚部。',
'候诊夫妻、预约单、牵手；人物较小，上方适合信息排版。',
'厨房双餐盘、小份餐食；丈夫轻放一盘，不增加其他动作。',
'同一候诊区，妻子持水；表情平静，无惊恐或血腥示意。',
'窗边牵手收束，保留原图暖色卧室。']
for x,n in zip(s['shots'],notes):
 x['visual_review_status']='reviewed_candidate_pending_user_approval';x['visual_review_notes']=n
s['status']='storyboard_review_pending'
s['shots'][3]['frame_plan']='夫妻背侧面牵手站在画面下半部，上方留白；不生成解剖图'
s['shots'][3]['action']='两人轻握手、自然呼吸，保持背侧面构图'
s['shots'][9]['action']='妻子将已握住的勺子轻抬，丈夫安静陪伴'
s['shots'][11]['camera']='轻推近至中景，避开脚部'
s['shots'][3]['motion_prompt']='The couple remains in the existing rear three-quarter view, softly holding hands with subtle breathing. Keep faces, clothes, hands, room and furniture stable. Slow gentle push-in. No new people, no text, no anatomy graphics.'
s['shots'][9]['motion_prompt']='The seated woman gently lifts the spoon already held in her hand. Her husband stays seated beside her with a calm supportive expression. Preserve identities, clothing, kitchen, plates and table. Gentle slow push-in. No text, no extra hands or props.'
s['shots'][11]['motion_prompt']='The woman lightly points to the open booklet while her husband looks down to read. Preserve both identities, clothing, table, cup, books and room. Slow push toward a medium shot, keeping feet outside the final framing. No text, no medical graphics.'
for i in [3,9,11]:(P/f"prompts/shots/{s['shots'][i]['id']}-motion-v2.txt").write_text(s['shots'][i]['motion_prompt']+'\n')
write('storyboard/draft-v2.json',s)
p=read('production-plan.json');p['status']='storyboard_review_pending'
p['tools'][0]['episode_status']='16 original-scene reference extensions returned actual PNGs; visually reviewed as storyboard candidates, not user-approved production assets'
p['tools'][0]['evidence']='review/reference-frames-v2.json'
p['tools'][1]['evidence']='review/server-preflight-v2.json'
for x,y in zip(p['shots'],s['shots']):
 x['reference_frame']=y['reference_frame'];x['reference_frame_sha256']=y['reference_frame_sha256']
write('production-plan.json',p)
records=[]
for f in sorted((P/'runs').glob('reference-extension-v2-*/*-manifest.json')):
 if f.name=='batch-manifest.json':continue
 records.append(read(str(f.relative_to(P))))
write('review/generation-evidence-v2.json',{'attempts':records,'timeout_note':'HTTP504 attempts may have been processed or billed remotely; no result received. Any retry is a separately recorded attempt, never automatic.'})
write('review/visual-qa-v2.json',{'version':2,'reviewed_at':datetime.datetime.now().isoformat(),'scope':'static reference images only; no animation/audio QA','status':'candidate_review_complete_pending_user_approval','items':[{'id':x['id'],'sha256':x['reference_frame_sha256'],'notes':x['visual_review_notes']} for x in s['shots']],'limitations':['No medical professional review','Generated faces and props are approximate extensions, not pixel-identical source copies','H3 motion and actual text-safe layout require subsequent production QA','Shot12 shoe variation: frame as medium shot','Shot06 test-stick markings are not diagnostic information']})
(P/'OUTPUTS.md').write_text('''# 怀孕1–12周变化

当前阶段：用户原始参考直接延伸，16镜完整图文v2待批准。无交付视频。

- [完整16镜图文v2](review/storyboard-v2.html)：实际首帧、旁白、文字、动作、时长和工具路线。
- [编号图文Markdown](storyboard/package-v2.md)
- [当前方案](PREPRODUCTION-v2.md)
- [实际图片及源图哈希](review/reference-frames-v2.json)
- [逐镜静态视觉检查](review/visual-qa-v2.json)
- [生成请求证据（含失败记录）](review/generation-evidence-v2.json)
- [事实核对](FACT_CHECK.md)
- [发布文案草案](PUBLISHING_DRAFT.md)
- [制作计划](production-plan.json)

历史：[v1方案](review/preproduction-v1.html)、[角色探索](review/character-review-v1.html)。独立母版已被用户跳过，不用于v2。

用户已指定原图人物和风格；尚未批准完整图文v2。配音、H3和合成尚未开始。
''')
for name in ['PREPRODUCTION.md']:
 f=P/name;t=f.read_text();marker='> 历史版本：当前采用用户原图直接延伸，见 [完整图文v2](review/storyboard-v2.html)。独立母版不用于本版。\n\n'
 if not t.startswith(marker):f.write_text(marker+t)
for name in ['preproduction-v1.html','character-review-v1.html']:
 f=P/'review'/name;t=f.read_text();banner='<div style="padding:18px;background:#fff2cd;color:#243e35">历史版本：已按用户要求跳过独立母版。<a href="storyboard-v2.html">查看当前完整16镜图文v2</a></div>'
 if banner not in t:
  if '<body>' in t:t=t.replace('<body>','<body>'+banner,1)
  elif '<main>' in t:t=t.replace('<main>','<main>'+banner,1)
  else:raise ValueError(name)
  f.write_text(t)
print('review state finalized; no production approval recorded')
