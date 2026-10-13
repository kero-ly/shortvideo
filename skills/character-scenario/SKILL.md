---
name: character-scenario
description: Use when producing character-driven scenario animation with consistent characters, complete scene reference frames and generated motion, including hand-drawn and cream storybook explainers.
---
# 人物情境动画制作方法

由video-production组织整期；本skill负责人物、场景、分镜与动作。风格由styles/registry.json中的预设选择，不默认为奶油绘本。前期读references/preproduction.md；模型执行读references/workflow.md；奶油绘本另读references/cream-storybook.md。

1. 用户给主题后，准备完整文案/分镜/工具计划草稿，并生成有限角色探索：单人母版一张和设定表一张。展示真实图片讨论角色；已授权探索不重复询问。候选图不代表批准。
2. 角色确认后，设计场景布局、家具、色板与关键物品；生成全部完整分镜首帧，包含人物、背景、物品、动作起点与文字留白。同一场景保持连续；母版是身份标准，不能用白底母版替代完整情境。参考图与动作prompt逐镜独立归档。
3. 网页按镜头编号展示实际参考帧、中文旁白/屏幕文字、预计时长、动作/运镜、图像与视频prompt、工具/模型路线；可放大图和折叠prompt，同时保留Markdown。授权全部首帧时完成全套，不增加三镜审批。
4. 用户明确批准完整图文包版本后，才配音、H3、建模、剪辑/渲染。角色批准不等于生产批准；实质改变角色、事实、镜头意图或工具路线须讨论。保持含义的技术返修最多两次，仍不合格展示问题。
5. 真实配音时长编排镜头，视频生成每镜一个主要动作与轻运镜。先选代表镜头试跑，必要时加最长信息镜头；内部技术试跑不增加用户审批。原片审核接受后才合成。

图片使用用户指定当前skill；案例路线为OpenLux GPT Image 2→220 H3→Remotion/FFmpeg，不能当作永久指定。提交前检查GPU/队列，不停止共享任务；220中断立即报告，不切本地或219。纯图文或准确结构内容可提出其他逐镜路线，但必须核实其实现与批准状态。

字幕/声音阶段调用../caption-alignment/SKILL.md；最终验收调用../video-qa/SKILL.md。新主题不继承旧事实、角色身份、旁白、时码或固定镜头数。模型原生音频默认不参与旁白科普，未经专门对齐不声称口型同步。
