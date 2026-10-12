# 早孕8个可能信号：奶油绘本科普版 — 前期方案 v1

状态：awaiting_confirmation。用户已同意风格方向；尚未确认本文件的角色、13镜及工具计划。没有启动本期素材生成、配音或视频制作。

## 定位与风格

受众是怀疑自己是否怀孕的成年人，同时覆盖备孕及无备孕计划者。标题《早孕可能出现的8个信号》，核心结论是症状不能确定或排除怀孕，按时验孕并知道何时就医。旁白像朋友安抚陪伴，不预设“恭喜”或生育意愿。

采用 `2d-storybook-cream-warm-daily-list-explainer@1`（奶油绘本科普），继承 `skills/2d-scenario-explainer/SKILL.md`。覆盖默认人物比例：圆脸、略大头的成人绘本形象，约五头身；非幼儿、非极端Q版。奶油白/浅粉/杏色，浅蓝平衡，柔和棕线与轻阴影。前作和新作独立保存，以同一旁白内容比较画风。

参考：用户当前抖音 @挪Zhong（孕中期）19秒《怀孕后的八个变化，看你中了几个？》。观察范围是UI播放和片头、气味敏感、腰酸的抽样画面，未完成全片听审或逐帧运动分析。原片一般视觉语言可参考；人物、构图重新设计。参考人物明显孕肚不适用本期早孕场景。本期采用H3小动作是我们的制作选择，不能据此推断参考片使用H3或真实角色动画。

## 原创角色与母版

暂称“小禾”，28岁成年女性，圆脸、自然五官、深棕锁骨长发、左侧米白小发夹；奶油开衫、浅陶粉长裤、米色拖鞋，未显怀、普通体型。避免婴幼儿化、夸张孕肚、暴露衣着、真实皮肤或3D塑料感。

母版一张：单人站立三分之四视角，全身，中性奶油背景，无文字无额外道具。设定表一张：正面/侧面/背面及疑惑、疲倦、恶心、平静表情，仅审核用。每镜图片编辑只输入已批准单人母版，不将多人设定表送入H3。先生成母版和设定表供用户批准母版，再生成01/03/11三张代表首帧供审阅，之后才批量制作；样张批准不代表允许改变既定事实。

## 规格、版式、声音

9:16，1080×1920、24fps，约80秒；下表总时长80秒只是剪辑目标，锁定以实际旁白为准，不机械加速。每镜一个主要动作，固定机位或轻推拉。H3基础素材预计576×1024，最终上采样不等于原生1080p。

黄字深棕描边短标题，控制在顶部安全区以下；字幕底部安全区以上、最多两行。所有汉字、序号、日历日期、测试规则由Remotion后期添加，生成图片和H3不负责文字。第10—13镜的信息卡按旁白分步出现。避免原片式上下模糊补边，采用原生竖版构图。

推荐本版沿用前作IndexTTS2旁白做内部风格对照，先核对实际音轨是否与本稿逐句一致；一致则复用并记录哈希，不重做配音。参考声线的公开使用权尚未验证，因此本版默认内部审阅；正式发布前需要授权声线并重新对齐时间。背景音乐选前作自制无歌词音乐，先检查源文件和记录，缺失则无BGM，不自动使用Music3或第三方音乐。不模仿参考作者声音。

## 完整逐镜设计

所有首帧均待生成，下述不是已有素材路径。图片路线统一为OpenLux GPT Image 2基于单人母版编辑；视频路线统一为220的MiniMax H3图生视频；文字/信息卡用Remotion合成。图像prompt由统一前缀加逐镜场景组成；H3只接受对应单镜首帧。

### 统一图片前缀

原创2D绘本插画，竖屏9:16，奶油白浅粉杏色配浅蓝，柔和棕色描边，平涂和少量柔和阴影。沿用已批准母版的同一位28岁成年女性：圆脸、自然成人五官、深棕锁骨长发、左侧小米白发夹、奶油开衫、浅陶粉长裤、米色拖鞋；站立约五头身、未显怀。保持成人身份和自然体型。关键主体避开顶部12%、底部18%、左右8%，不带文字水印，不出现胎儿、婴儿、明显孕肚或验孕阳性暗示。

### 01 开场 · 约8秒

- **旁白**：月经还没来，身体又有点不一样？先别急着猜答案。早孕可能有这些变化，但每个人都不一样。
- **首帧与构图**：客厅中景，主角坐在沙发上看无字日历，右侧预留标题区。
- **动作 / 运镜**：从日历抬眼，轻轻放松肩膀；缓慢推近。
- **后期文字**：身体有点不一样？
- **图片prompt**：统一前缀 +「客厅中景，主角坐在沙发上看无字日历，右侧预留标题区。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 从日历抬眼，轻轻放松肩膀。Camera: 缓慢推近。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_01_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 02 月经推迟 · 约5秒

- **旁白**：第一，月经推迟。尤其平时周期比较规律时，值得留意。
- **首帧与构图**：餐桌中景，主角看桌上无字日历；后期叠加预计经期标记。
- **动作 / 运镜**：用一根手指指向日历，稍作停顿；固定。
- **后期文字**：01 月经推迟
- **图片prompt**：统一前缀 +「餐桌中景，主角看桌上无字日历；后期叠加预计经期标记。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 用一根手指指向日历，稍作停顿。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_02_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 03 容易疲倦 · 约5秒

- **旁白**：第二，容易累。平常做完不费力的事，也想坐下来歇一歇。
- **首帧与构图**：沙发中景，主角已经坐稳，身旁放叠好的毛巾。
- **动作 / 运镜**：抱住靠垫，轻轻打一个哈欠；固定。
- **后期文字**：02 比平时更容易累
- **图片prompt**：统一前缀 +「沙发中景，主角已经坐稳，身旁放叠好的毛巾。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 抱住靠垫，轻轻打一个哈欠。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_03_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 04 乳房敏感 · 约4.5秒

- **旁白**：第三，乳房胀痛或变得敏感。不过，经前也可能这样。
- **首帧与构图**：卧室上半身中景，衣着完整，主角手已搭在开衫前襟，镜头不聚焦胸部。
- **动作 / 运镜**：轻调开衫前襟，微皱眉后停住；固定。
- **后期文字**：03 乳房胀痛或敏感｜经前也可能出现
- **图片prompt**：统一前缀 +「卧室上半身中景，衣着完整，主角手已搭在开衫前襟，镜头不聚焦胸部。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 轻调开衫前襟，微皱眉后停住。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_04_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 05 恶心 · 约4秒

- **旁白**：第四，恶心。它不一定只在早晨出现。
- **首帧与构图**：厨房中景，人物身前留空，桌上只有水杯。
- **动作 / 运镜**：轻掩嘴并停顿，不呕吐、不弯腰剧烈晃动；固定。
- **后期文字**：04 恶心｜不只在早晨
- **图片prompt**：统一前缀 +「厨房中景，人物身前留空，桌上只有水杯。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 轻掩嘴并停顿，不呕吐、不弯腰剧烈晃动。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_05_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 06 气味敏感 · 约4.5秒

- **旁白**：第五，对气味更敏感。熟悉的味道，突然觉得受不了。
- **首帧与构图**：餐桌中景，一碗热汤在左前景，人物居中；不画鼻子比喻或文字气泡。
- **动作 / 运镜**：微转头避开热汤，另一只手保持静止；固定。
- **后期文字**：05 对气味更敏感
- **图片prompt**：统一前缀 +「餐桌中景，一碗热汤在左前景，人物居中；不画鼻子比喻或文字气泡。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 微转头避开热汤，另一只手保持静止。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_06_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 07 尿频 · 约4.5秒

- **旁白**：第六，上厕所比平时频繁，尤其是小便次数增多。
- **首帧与构图**：走廊中景，人物在洗手间门外侧身站立，门关闭。
- **动作 / 运镜**：朝门方向走一小步后停下；不打开门；固定。
- **后期文字**：06 小便次数增多
- **图片prompt**：统一前缀 +「走廊中景，人物在洗手间门外侧身站立，门关闭。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 朝门方向走一小步后停下；不打开门。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_07_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 08 口味变化 · 约4.5秒

- **旁白**：第七，口味变了。以前爱吃的食物，现在可能不想碰。
- **首帧与构图**：餐桌中景，人物面前一盘简单食物，双手清楚可见。
- **动作 / 运镜**：将餐盘轻推远一点，轻摇头；固定。
- **后期文字**：07 口味变化
- **图片prompt**：统一前缀 +「餐桌中景，人物面前一盘简单食物，双手清楚可见。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 将餐盘轻推远一点，轻摇头。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_08_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 09 情绪起伏 · 约5秒

- **旁白**：第八，情绪起伏比平时明显，也可能只是众多变化之一。
- **首帧与构图**：客厅中景，手机屏幕朝下放在旁边，人物轻皱眉。
- **动作 / 运镜**：呼出一口气，眉头逐渐放松；轻推近。
- **后期文字**：08 情绪起伏
- **图片prompt**：统一前缀 +「客厅中景，手机屏幕朝下放在旁边，人物轻皱眉。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 呼出一口气，眉头逐渐放松。Camera: 轻推近。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_09_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 10 症状不能确诊 · 约9.5秒

- **旁白**：但请记住，有几条都不能直接说明怀孕，没有这些反应也不能排除。最可靠的下一步，是按说明做一次验孕。
- **首帧与构图**：人物安静坐在画面左下，右上留出信息卡区域；不出现宝宝或验孕结果。
- **动作 / 运镜**：看向前方，轻点头一次；固定。
- **后期文字**：有症状≠确定怀孕｜没症状≠排除怀孕
- **图片prompt**：统一前缀 +「人物安静坐在画面左下，右上留出信息卡区域；不出现宝宝或验孕结果。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 看向前方，轻点头一次。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_10_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 11 何时验孕 · 约9秒

- **旁白**：通常从月经推迟的第一天开始测。如果不知道月经什么时候来，就在上次无保护性行为至少二十一天后测。
- **首帧与构图**：桌旁人物放在左下，桌上无品牌的封闭验孕包装及说明书，右侧大面积留空。
- **动作 / 运镜**：轻指向桌上说明书后保持；固定。
- **后期文字**：月经推迟第一天起｜日期不清：上次无保护性行为至少21天后
- **图片prompt**：统一前缀 +「桌旁人物放在左下，桌上无品牌的封闭验孕包装及说明书，右侧大面积留空。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 轻指向桌上说明书后保持。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_11_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 12 阴性后如何做 · 约8秒

- **旁白**：测得太早是阴性，月经又没来？过几天再测一次。第二次仍是阴性、月经还没来，可以咨询医生。
- **首帧与构图**：人物在餐桌前看手机背面，左侧留白用于后期步骤卡。
- **动作 / 运镜**：拿起手机到舒适阅读位置后停住；固定。
- **后期文字**：过几天复测 → 仍阴性且月经没来：咨询医生
- **图片prompt**：统一前缀 +「人物在餐桌前看手机背面，左侧留白用于后期步骤卡。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 拿起手机到舒适阅读位置后停住。Camera: 固定。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_12_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

### 13 就医与陪伴 · 约8.5秒

- **旁白**：要是出现明显腹痛或阴道出血，请及时就医。先确认，再决定下一步，不用一个人靠猜。
- **首帧与构图**：客厅人物坐稳，旁边放水杯；无腹痛表演、无流血画面；上方预留提醒卡。
- **动作 / 运镜**：肩膀自然放松，平静看向前方；轻微拉远。
- **后期文字**：明显腹痛或阴道出血：及时就医｜先确认，再决定下一步
- **图片prompt**：统一前缀 +「客厅人物坐稳，旁边放水杯；无腹痛表演、无流血画面；上方预留提醒卡。」
- **H3 prompt**：Preserve the exact same adult character, outfit, warm cream storybook illustration and soft brown outlines of the reference. One continuous shot. Action: 肩膀自然放松，平静看向前方。Camera: 轻微拉远。 Gentle small movement, stable face and hands, stable background and props. No cuts, no lip-sync, no new people, no new objects, no written text, no photorealism, no 3D rendering, no pregnancy-belly growth.
- **计划首帧**：`references/shots/shot_13_v1.png`（待生成）；完整prompt见 `shots.plan.json`。

## 工具、资源、预算与执行顺序

1. 用户确认本方案v1的角色、旁白、逐镜内容及工具路线，记录确认依据。
2. 复核下列医学来源、220连接/GPU余量/H3服务、OpenLux连通性；读取图片skill最新编辑接口。只读共用模型，不停止他人任务；服务器异常立即报告，禁止本地视频生产或改用219。
3. OpenLux GPT Image 2：1张角色母版、1张设定表；母版获得用户批准后生成01/03/11首帧样张。用户审阅三张首帧后完成共13张首帧。计划15张图片，单图失败最多额外重试2次，总计最多45次图片请求；超过预算前讨论。付费接口的当前单价未核实，若出现新的付费步骤或需充值则先给出金额。
4. 220 MiniMax H3，经现有ComfyUI适配器执行。沿用前作int8主模型、Qwen文本编码器和H3 VAE，先查真实工作流参数；首试第03镜疲倦，测试人物一致性、小动作和暖彩保真，再生成其余12镜。预计13次基础视频任务，每镜最多2次修复重试，最多39次；不同时占用多张卡。不承诺未经测量的运行耗时。
5. 镜头长度以旁白为准：普通镜单段H3素材，长信息镜保留稳定人物段并由后期信息卡推进；尾部必要时稳定末帧延续，不强行循环角色动作。若冻结尾帧显著影响观感，先提出拆镜或增加素材的修订。
6. 核对前作实际旁白与本稿，登记来源路径/SHA256后复用；需要新TTS时在220用uv管理Python。H3原音不用作成片旁白。封面直接用审核过的首帧加后期标题，不额外生成角色。
7. Remotion沿用工厂渲染环境，建立本期独立props/入口，不能直接执行硬编码旧13镜资产和声轨的compose_h3.py。FFmpeg用于抽帧、转码、混音和检查。所有视频生成、合成、抽帧、渲染在220；本地仅方案、图片API、媒体归档和预览。
8. 先出540×960低清样片，经用户确认再1080×1920终渲染；交付MP4、封面、SRT、逐镜prompt索引、来源/授权说明、QA和SHA256清单。

这条工具链在前作已产出内部审阅片；新画风尚未验证。当前仅验证220 SSH和Git状态，不把历史成功当成本次H3/OpenLux健康检查。无需Blender/FreeCAD/Godot建模；改用建模需另议。

## 内容依据及待核查项

继承前作同题事实依据，但以下网页在本轮尚未重新访问，素材生成前及发布前要复核：

- NHS Signs and symptoms: https://www.nhs.uk/pregnancy/trying-for-a-baby/signs-and-symptoms-that-might-mean-youre-pregnant/
- NHS Doing a pregnancy test: https://www.nhs.uk/pregnancy/trying-for-a-baby/doing-a-pregnancy-test/
- NHS Symptoms needing help: https://www.nhs.uk/pregnancy/common-symptoms/pregnancy-symptoms-you-need-to-get-help-for/

每项是可能的变化，不是诊断标准或全部人都会出现的“典型组合”。不使用“中了三条基本怀孕”。不把出血、明显腹痛列为普通信号。早期阴性不能直接排除，复测与咨询建议保留。不生成带结果线的验孕棒，避免图像误导。

## 验收与失败处理

- 母版/首帧：成人身份明确、未显怀；发型服装线条配色一致，情境一眼可读，无多指、重复道具或文字乱码。
- 单镜视频：抽首中尾帧并完整播放检查，重点查手部、餐盘、门和人物脸是否变形；一个动作达意、镜头不漂移。两次修复仍失败就返回讨论，不悄悄换路线。
- 信息：8项编号完整；验孕时机与复测文字准确，21天明确关联上次无保护性行为；提醒足够停留时间。画面不暗示症状数量可确诊。
- 音画：字幕逐句对应，实际听审无错读、突兀切断和音乐压人声；参考声线权利未确认前仅内部审阅。
- 技术：ffprobe检查尺寸/fps/时长/编码/音轨，FFmpeg检查黑帧与峰值，核对字幕安全区；完整播放与实际听审、抽帧QA、自动QA分别记录完成情况，不互相冒充。
- Git只提交本方案、JSON、prompt、脚本、来源与哈希；所有图片音视频/封面/缩略图走独立媒体同步。原案例不覆盖。

## 待用户确认

确认本v1的原创角色、80秒13镜、完整旁白、黄色标题和OpenLux→H3→Remotion路线；默认先做内部审阅片，先审母版与三张代表首帧，再批量制作。确认后才进入制作；本文件没有代替用户记录批准。

制作可行性审阅：已完成只读builder check，已澄清母版批准先于三张代表首帧生成；未发现其余重要执行缺项。此审阅不等于用户批准。

## v1.1 审批流程更新（以此段覆盖v1旧审批顺序）

用户明确要求先做角色母版图和角色设计，再看图讨论。当前授权范围：OpenLux生成一张单人母版和一张设定表；不再要求生成角色前批准完整v1。随后展示实际图片，与本文13镜及工具路线一起确认；确认前不生成01/03/11或其他分镜图、TTS或视频。正文v1的旧审批顺序作为历史记录，不作为当前执行门槛。角色设计和旁白暂不变。当前状态：character_exploration_authorized，整期制作仍awaiting_confirmation。

角色探索结果：已生成 master_v2.png（1024×1536）及 sheet_v2.png（1536×1024），原始尺寸无调整。v1偏精细人物插画，保留但不推荐；v2简化五官、加粗棕线，作为待审候选。实际母版接近正面而非原提案三分之四角度；设定表侧面发夹位置仍需在锁定角色时校正，不能称为严格一致三视图。共4次图片请求，无H3/TTS/视频渲染。已做两张v2视觉检查；用户尚未批准。prompt及输入关系见character-manifest.json。
