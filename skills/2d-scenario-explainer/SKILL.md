---
name: 2d-scenario-explainer
description: Use when planning or producing 2D character scenario explainers, including hand-drawn animation and cream storybook illustration presets, with consistent adult cartoon characters acting out everyday situations, reassuring narration and readable explanatory cards, including maternal health and everyday science topics.
---

# 2D 手绘动画 · 暖色明亮低饱和 · 生活情境科普

用原创 2D 人物演生活情境，以像朋友一样的旁白解释主题，再给出清晰的行动建议。适用于成年观众的母婴、健康和生活科普；具体受众按本期 brief 决定。不要仿制参考作者的角色、声音、标识。

从本 skill 所在目录向上两级找到工厂根目录。先读根目录 `AGENTS.md`、`docs/workspace-layout.md`、`configs/resources.json`。工作流细节见 [references/workflow.md](references/workflow.md)；准备前期方案时读 [references/preproduction.md](references/preproduction.md)。

## 风格检索与输入

本 skill 是“2D 人物情境科普”的制作方法，当前默认预设为 `2d-handdrawn-warm-light-muted-daily-explainer`。命名与分类见根目录 `styles/README.md`，默认预设见 `styles/2d-handdrawn/warm-light-muted-daily-explainer.json`。前期方案记录 preset ID、版本、各风格维度与本期覆盖项；“温柔陪伴”归入语气，“母婴”归入主题，工具归入实现路线。用户修改色调或语气时明确记录覆盖项，不必复制整套 skill。换成实拍、3D 或纯剪辑形式时重新选择制作路线，不自动宣称本 skill 已支持。

## 输入与风格

用户通常只提供主题、核心观点、受众、必须准确的事实和参考。已有信息直接复用，只询问影响内容设计的缺项；工具由你提出并解释，用户指定工具优先。

- 视觉：以选定风格预设为准；奶油绘本预设可用略大头的成人卡通，默认预设用成人比例的 2D 手绘卡通、克制表情、柔和轮廓、低饱和配色、温暖日常场景。默认奶油白 / 鼠尾草绿 / 浅木色，可按主题调整。
- 内容：生活中的疑问 → 情境化解释 → 限制与误区 → 可执行的下一步。时长和镜头数量随内容决定，不套用固定 13 镜。
- 声音：温和陪伴、自然停顿、不制造焦虑；旁白独立于角色口型。声线来源和使用范围必须记录。
- 画面：每镜一个主要动作和一种轻微运镜；角色保持一致，生活道具少而清晰。抽象事实、数字、医学文字用后期信息卡表达。
- 版式：默认竖屏，标题、字幕、信息卡留安全区；避免挡脸和关键动作。发布平台安全区要单独检查。

## 先展示角色，再确认整期制作

用户提出制作主题并给出风格方向后，先完成 brief、角色设计和完整前期方案草稿，直接制作有限角色样张：默认一张单人母版、一张角度/表情设定表。使用已选图片工具；已有授权无需再次询问是否生成角色。样张是供讨论的候选，不是已批准资产。默认不扩展为多角色、多套风格或大量候选。

展示实际图片及尺寸，说明角色设计、完整旁白、逐镜画面/动作/运镜/文字/时长、工具模型路线、素材和难点，与用户一起确认。图片可在本地调用已选API生成；视频仍在220执行。角色母版与设定表只用于前期视觉讨论，不能自动授权分镜首帧批量生成、配音、H3、建模、剪辑或渲染。

将设计和批准范围写入 `projects/<episode>/PREPRODUCTION.md`。状态区分角色探索已授权、样张待审、整期已批准；用户看完图明确确认角色及本期方案后进入制作。不把一般“继续”视为对尚未展示方案的确认。用户明确指定其他审批顺序或限定样张范围时优先遵从。已有确认覆盖当前版本时不重复询问。

样张有明显技术瑕疵可最多自行返修两次；改变风格、身份或设计方向先展示问题讨论。制作中角色、分镜含义、关键事实或工具路线有实质变更，呈现修改方案再确认；技术参数的小幅修正可自行处理并记录。

## 执行与交付

前期先完成角色母版与设定表并展示；角色及完整方案确认后按依赖执行：代表镜头参考图审核 → 全部分镜参考图 → 单镜视频试跑 → 逐镜生成与审核 → 旁白时间线与合成样片 → 成片 QA → 交付。配音可与参考图阶段独立执行，但剪辑长度以真实旁白为准。调用和失败恢复按 workflow reference。

视频生成、建模、剪辑、渲染及视频抽帧在 220 执行；本地可编写方案、调用已选图片 API、归档与预览。服务器连接异常立即通知用户并停下依赖服务器的工作，禁止擅自转成本地视频生产或 219。恢复后查询原任务，避免重复提交。

验收同时覆盖人物/肢体/道具、动作含义、事实、字幕、同步、声音和技术参数。明确区分抽帧检查、完整人工观看、实际听审、自动技术 QA，未做的不能声称做过。旁白使用权未确认时只交内部审阅版。

交付视频、封面、SRT、分镜与 prompt 索引、来源、版本和 QA、SHA256 manifest。案例图片/视频/音频（含封面与审核缩略图）只保留磁盘和媒体备份，不进入 Git。Git 追踪源代码、文案、prompt、参数、来源及 QA 文本、媒体哈希；按根目录同步规则操作。

## 已有案例与复用边界

`projects/early_pregnancy_signs_01/h3_v2/` 已验证 OpenLux GPT Image 2 → MiniMax H3 → Remotion → FFmpeg 的内部审阅链路；查看 `PRODUCTION.md`、`SHOT_LIST.md` 和 `review/h3-clips.json` 获取真实记录。可复用适配器和版式，不复用早孕事实、旧旁白、角色或医学卡片去套无关主题。

该例 `compose_h3.py` / `finalize_h3.py` 仍硬编码本期 13 镜、旧声轨和医学内容，不能直接用于新主题。新期先建立自己的 episode 数据与合成入口或明确参数化；本 skill 是可执行指导，不是已经完成的通用批量调度器。
