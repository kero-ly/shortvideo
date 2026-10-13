"""Author episode-only preproduction evidence; does not render video."""
from pathlib import Path
import json, hashlib, html
ROOT=Path(__file__).resolve().parents[3]
P=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
# All timings are editorial estimates until narration exists.
rows=[
('开场',1,7,'怀孕第1周，通常还没受精？看懂这12周，也看见妈妈的辛苦。','孕1—12周变化｜宝宝 × 妈妈','夫妻在卧室靠近，女主轻扶小腹，腹部不明显隆起','男主轻扶女主肩，女主转头微笑','缓慢推进'),
('第1周',2,5,'孕周从末次月经第一天算，不是从受精那天算。','第1周｜孕周从末次月经第一天算','夫妻坐餐桌前查看空白日历，妻子手指落在一格','妻子指向日历，丈夫轻点头','固定中景，日历重点由后期图形强调'),
('第2周',3,5,'第2周，身体为排卵做准备。周期不同，排卵时间也不同。','第2周｜准备排卵；按末次月经起算，周期不同时间可有差异','女主坐客厅沙发饮水，丈夫递上薄毯；移除原图医学气泡','丈夫把毯子放在她身侧','固定中景'),
('第3周',4,6,'第3周前后，可能发生受精。细胞分裂，随后向子宫移动。','第3周前后｜受精 → 分裂 → 移动','夫妻牵手站在左下部，右上空白供后期概念路径；不生成解剖图','两人轻握手，眼神自然交汇','缓慢拉近'),
('第4周',4,5,'到第4周前后，着床通常已经发生，但你可能还没有明显感觉。','第4周前后｜通常已着床；可能无明显症状','夫妻坐明亮窗边，人物下半区，上方留白供概念点阵','妻子将手轻放腹前，丈夫微笑','轻推近'),
('第5周',5,6,'第5周，脑、脊髓和心脏正在发育。停经、犯困，也可能让你发现怀孕。','第5周｜脑、脊髓、心脏正在发育','女主坐床边看空白验孕棒，男主坐侧边陪伴；检测标识后期添加且非诊断','妻子低头看手中物件，丈夫看向她','固定中景'),
('第6周',6,6,'第6周，四肢芽开始出现。恶心可能找上门，而且不只发生在早晨。','第6周｜四肢芽开始出现；孕吐不限早晨','妻子坐床边轻掩口，丈夫拿常温水杯，背景不含胚胎图','丈夫将水放近，妻子轻呼气','轻推近'),
('第7周',6,5,'第7周，脑部快速发育，小胳膊继续长。妈妈可能依然很累。','第7周｜脑部快速发育；手臂继续长','妻子靠沙发休息，丈夫拿靠垫放她背后','丈夫轻调整靠垫，妻子放松肩膀','固定中景'),
('第8周',7,6,'第8周，四肢继续发育。闻到饭味就难受，真的不是矫情。','第8周｜四肢继续发育；气味可能诱发恶心','厨房妻子轻掩鼻口，丈夫拿一份清淡小餐，移除浓烈红色菜肴','丈夫将餐碟缓缓放在桌上','固定中景'),
('第9周',7,5,'第9周，面部轮廓更清楚，手脚继续发育。孕吐和疲倦可能还在。','第9周｜面部、手脚继续发育','餐桌妻子面对小份清淡食物，丈夫坐旁陪伴，不劝吃','妻子缓慢拿起勺子，丈夫安静点头','轻推近'),
('第10周',8,6,'第10周，宝宝已经有小动作，但妈妈通常还感觉不到胎动。','第10周｜有小动作 ≠ 妈妈能感觉胎动','夫妻翻看空白孕期手册，原图胎儿气泡移除，不用真实医学报告','夫妻缓慢翻一页，相视微笑','轻微侧移'),
('第11周',8,5,'第11周，小手指、脚趾逐渐分开，身体仍在快速成长。','第11周｜手指、脚趾逐渐分开','同一客厅餐桌夫妻看孕期手册，上方留出信息区','妻子轻指一页，丈夫低头阅读','轻推近'),
('第12周',10,7,'第12周，头臀长大约五厘米。器官还在发育，产检继续按医生安排。','第12周｜头臀长约5厘米；器官继续发育','夫妻坐产科候诊区，持空白预约单，人物腹部不夸张','丈夫轻握妻子手，两人看向诊室方向','缓慢推进'),
('陪伴行动',7,8,'准爸爸能做的：分担家务，准备她吃得下的小餐，陪她休息、产检。','伴侣清单｜分担家务 · 小餐 · 陪伴','暖色厨房丈夫备小餐，女主坐桌旁休息，同原厨房布局','丈夫把小餐放下，女主轻点头','固定中景'),
('必要提醒',9,8,'每个人反应不同。出血、明显腹痛，或吐到喝不进水，要及时就医。','出血 / 明显腹痛 / 喝不进水 → 及时就医','不用原图卫生巾与三格拼图，改为单幅候诊区夫妻等待；非惊恐画面','丈夫轻陪伴，妻子平静握水杯','固定中景'),
('结尾',1,7,'肚子还没显出来，不代表她不辛苦。收藏对照孕周，转给陪你迎接宝宝的人。','看不见的变化，也值得被理解｜关注，继续了解孕期变化','夫妻窗边牵手，原卧室暖色柔光，顶部留白，无遮挡人物','两人牵手自然靠近，轻微微笑','缓慢拉远')]
shots=[]
for i,(week,ref,dur,voice,text,frame,action,camera) in enumerate(rows,1):
 sid=f'shot-{i:02d}'
 image_prompt=f'Create one 9:16 portrait frame in the supplied warm 2D hand-drawn illustration style. Preserve the adult woman and adult man identities, hairstyles, cream blouse and long navy skirt for her, navy sweater and olive trousers for him. Early pregnancy: no exaggerated belly. Complete consistent room with furniture and props. Scene brief: {frame}. Action starting pose: {action}. Keep upper 18 percent calm and uncluttered for a title, the bottom 22 percent calm for captions, and avoid important objects at the right edge. No words, numbers, watermark, speech bubble, fetus or anatomy illustration. Gentle adult proportions, natural hands. One scene only, no collage.'
 motion_prompt=f'Warm hand-drawn animation, consistent adult couple in a quiet complete room. One subtle natural gesture, {action}. {camera}. Stable faces, clothing and room layout. Blank calm wall areas. Slow gentle motion. No scene change.'
 # Bilingual draft prompts; normalize motion to concise English before H3 submission.
 shots.append(dict(id=sid,phase=week,estimated_seconds=dur,narration=voice,screen_text=text,reference_source=f'怀孕1到12周（无文字版）参考图/landscape-scene-{ref:02d}.png',frame_plan=frame,action=action,camera=camera,method='character-scenario',route=['OpenLux gpt-image-2 edit portrait reference','220 H3 character motion','220 Remotion exact Chinese labels and conceptual graphics','FFmpeg encode/QA'],image_prompt=image_prompt,motion_prompt_draft=motion_prompt,reference_frame_status='not_generated_pending_character_review'))
for s in shots:
 q=P/'prompts'/'shots';q.mkdir(exist_ok=True)
 (q/f"{s['id']}-image-v1.txt").write_text(s['image_prompt']+'\n')
 (q/f"{s['id']}-motion-draft-v1.txt").write_text(s['motion_prompt_draft']+'\n')
save(P/'storyboard/draft-v1.json',{'revision':1,'status':'draft_not_production_approved','timing':'editorial_estimate_only','estimated_total_seconds':sum(s['estimated_seconds'] for s in shots),'shots':shots})
inputs=[]
for f in sorted((P/'怀孕1到12周（无文字版）参考图').glob('*.png')):
 from PIL import Image
 im=Image.open(f)
 inputs.append({'path':str(f.relative_to(P)),'sha256':sha(f),'size':list(im.size),'source':'user_supplied_reference','authorization':'user requested design and animation based on these references','public_reuse_rights':'not_independently_verified','use':'visual direction; no downloaded third-party footage'})
save(P/'review/input-media-v1.json',{'assets':inputs})
preset_path='styles/presets/2d-handdrawn-warm-light-muted-daily-explainer.json'
preset=json.loads((ROOT/preset_path).read_text())
components=[dict(c,sha256=sha(ROOT/c['path'])) for c in preset['components'].values()]
overrides={'visual_basis':'user-supplied warm hand-drawn adult couple; preserve original identities and clothes','aspect_ratio':'9:16','target_delivery_size':[1080,1920],'tone':'empathetic factual explanation, no fear appeals','format':'week-by-week dual narrative: fetal development and maternal experience','duration':'estimated 95–110 seconds; determined by real TTS later','anatomy':'no model-generated anatomy motion; optional non-anatomical symbolic overlays labeled schematic','voice':'warm clear adult female; reference and authorization to be selected before TTS','music':'optional very low instrumental with verified source; otherwise omit','captions':'one narration caption layer plus short nonduplicative week heading; right/bottom Douyin UI reserve'}
plan={'episode_id':'怀孕1-12周变化','revision':1,'status':'character_review_pending','brief':{'topic':'怀孕1—12周变化','audience':'母婴账号：孕早期女性、备孕家庭及准爸爸','key_points':['孕周从末次月经起算，避免把受精周龄当孕周','每周发育要点和妈妈感受并列','伴侣行动建议提供转发理由','症状因人而异，异常就医'],'goals':['关注增长','点赞与情绪共鸣','收藏与转发价值'],'metrics_note':'creative objectives, no performance guarantee'},'selection':{'basis':'User explicitly supplied reference images; agent selected closest registered preset with episode-only overrides, pending review','preset':{'id':preset['id'],'version':preset['version'],'path':preset_path,'sha256':sha(ROOT/preset_path)},'components':components,'overrides':overrides},'resolved':{'status':'draft_not_locked','preset':preset,'component_configs':{k:json.loads((ROOT/c['path']).read_text()) for k,c in preset['components'].items()},'episode_overrides':overrides},'methods':['character-scenario'],'tools':[{'capability':'image','provider':'OpenLux gpt-image-2','status':'configured','episode_status':'character generation requested; outputs pending'},{'capability':'video','provider':'220 H3 ComfyUI','status':'configured','episode_status':'SSH reachable; no H3 task or current API verification yet'},{'capability':'narration','provider':'IndexTTS2 on 220','status':'configured','episode_status':'voice reference not selected; not run'},{'capability':'composition','provider':'Remotion + FFmpeg on 220','status':'configured','episode_status':'new episode renderer adaptation not implemented'}],'shots':[{'id':s['id'],'method':s['method'],'route':s['route']} for s in shots],'approvals':[{'scope':'reference inspection, editorial design and bounded character exploration','revision':1,'evidence':'2026-10-13 user requested designing script and animation based on supplied images for an end-to-end Douyin video; no actual candidate character/storyboard version approved yet'}]}
save(P/'production-plan.json',plan)
body='\n'.join(f"### {s['id']} · {s['phase']} · 预计{s['estimated_seconds']}秒\n\n旁白：{s['narration']}\n\n屏幕文字：{s['screen_text']}\n\n首帧计划：{s['frame_plan']}\n\n动作：{s['action']}；运镜：{s['camera']}。\n\n原始参考：{s['reference_source']}（不是最终首帧）。\n" for s in shots)
(P/'PREPRODUCTION.md').write_text('''# 怀孕1—12周变化 · 前期方案 v1

状态：character_review_pending。全套中文文案与镜头草案已编写；最终竖屏首帧尚未生成；未开始配音、H3、合成和渲染。

## 内容与传播设计

用户目标：母婴账号，争取涨粉、点赞和转发。推荐95–110秒，9:16；真实时长以配音为准，不强行加速。

核心：宝宝每周的变化与妈妈看不见的付出。开头用“第1周通常还没有受精”建立知识价值，日历/周次进度条帮助追踪。中段以每周一个发育重点为主，不堆尺寸与器官名；生活情境交替呈现疲倦、气味敏感与伴侣支持。结尾明确“收藏对照孕周、转给陪伴者”的用途，关注提示仅在屏幕一次，避免连续索要互动。

备选结构：纯逐周发育图鉴适合查询但情绪联系较少；纯伴侣陪伴故事更易共鸣但削弱本题知识覆盖。本版采用双线结构，保持1—12周为主体。

这些是设计假设，尚无本账号基线或AB数据，不称为爆款模型。发布后建议记录3秒留存、平均观看/完播、每千播放收藏/分享/新增关注，再决定下一期节奏。未获本账号数据访问权限，不读取账号私有信息。

## 参考与画风

用户提供10张无文字参考图，多数约16:9，三张3:2；保留温暖居家、成年夫妻、柔和深色线稿。女主黑色长卷发、米白上衣、深蓝长裙；男主黑色短发、深蓝上衣、橄榄绿裤。既有成人比例，不改圆脸Q版。使用暖色手绘preset v1作基底，本期覆盖记录于production-plan；不修改共享风格。

横图不能直接中央裁成竖屏。角色确认后逐镜重新构图；顶部约18%、底部约22%保持可读空间，右侧避免关键内容；具体安全区以手机审阅校准。第9张是三格拼图，仅作为提醒意图参考，重做为单场景，不直接图生视频。

## 医学表达与图示边界

孕周是从末次月经第一天计算的产科孕周；约28天周期是讲述框架，排卵/着床时间会变，必要时由超声核对孕周。本期不宣称固定周数一定能见胎心，不用孕吐强弱判胎儿状态，不说12周一定停止孕吐或绝对安全。不把NHS英国产检时间直接套中国。

准确中文、日期、发育概念由后期渲染。原图内子宫/胚胎气泡不是已审核医学图；人物H3镜头移除这些元素，只生成生活动作。如采用受精—移动—着床示意，用概念点阵/箭头且标“示意，非真实比例”，不声称解剖动画准确。每周成长在内容卡中表达，不让H3自行把胚胎变形成婴儿。

## 角色与连续性

按原始scene01派生单人母版一张、人物设定表一张，均是候选，需实际看图确认。男主身份以原始scene01/02为参考，后续全套首帧保持一致。女主早孕不画明显晚孕肚。三套居家场景：卧室浅木床/左窗，客厅米色沙发/绿抱枕/木书架，厨房浅绿柜体/木桌；另有产科候诊区。服装、发型、色板与道具布局统一。

## 制作路线与依赖

OpenLux编辑竖屏参考帧 → 220 H3轻动作（候选Turbo8，失败最多两次有限返修）→ 220 IndexTTS2独立旁白 → 按真实声音建立时间线 → 220 Remotion叠加精确文字/进度条 → FFmpeg输出与QA。无口型同步要求。原生H3既有案例为576×1024/24fps，最终1080×1920是合成放大，不能称为原生高清。

预计请求：角色2张；角色确认后16张独立首帧，除必要返修不批量多候选；H3先1个代表镜头，接受后其余串行；TTS按实际分段。未获得价格/耗时测量，不填写虚构人民币预算。配音参考声线和音乐来源生产前登记；未确认音乐可不使用配乐。现有案例脚本须适配新镜头、路径与文案，不复用旧声音/时码。所有模型、合成、视频抽帧在220；SSH失败立刻报告，不切本地或219。

## 批准与验收

原图授权仅支持本期设计探索，不等同于已批准候选人物和全分镜版本。当前未批准角色；下一步确认角色后完成全部实际竖屏首帧与编号图文网页，统一确认该版本后才TTS/H3/合成。不会在完成三镜后额外加批准关卡。技术通过、视觉抽检、语义审核和完整听审分别记录。

本期源码、prompt、来源、QA与hash保留项目内；媒体不入Git。最终交付MP4、封面、SRT、时间线、发布文案、来源、QA和SHA256。输入图公开复用权利尚未独立核验，第三方公开视频仅借鉴结构，不下载或复制素材、声音、人物。

## 完整分镜文案草案

'''+body)
(P/'PUBLISHING_DRAFT.md').write_text('''# 发布文案候选 v1（未发布）

封面：孕1—12周变化\n副标题：宝宝在长大，妈妈也在努力

标题：肚子还没显出来，她已经经历了这么多｜孕1—12周变化

简介：从孕周怎么算，到宝宝每周在长什么，再到准爸爸能做的几件小事。这份孕早期变化表，送给准备迎接宝宝的你们。发育与症状因人而异，具体以产检评估为准。

话题候选：#孕早期 #怀孕1到12周 #孕期知识 #准爸爸 #母婴

评论引导：孕早期，你最希望家人理解哪件事？（不要求观众公开病历、检查结果。）

屏幕关注提示：关注，继续了解孕期变化。没有预先承诺尚未制作的下一期发布时间。

待成片审阅后确认封面措辞、话题及AI标识；不代用户发布，不承诺数据。
''')
print('shots',len(shots),'estimated_seconds',sum(s['estimated_seconds'] for s in shots),'narration_characters',sum(len(s['narration']) for s in shots))
