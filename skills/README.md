# 视频制作技能入口

用户只需主题和可选风格，代理首先读取 [video-production](video-production/SKILL.md)。它选择方法与风格组合，记录本期计划和确认版本；不是自动模型调度器。

| 层级 | 入口 | 职责 |
|---|---|---|
| 总工作流 | video-production | 主题、选择、阶段、审阅、交付组织 |
| 制作方法 | character-scenario | 角色、场景、完整首帧、动作、H3路线 |
| 方法案例与参考 | [2d-mechanism-explainer](2d-mechanism-explainer/SKILL.md) | 器官/机制分层与运动分镜；心脏循环的血流、轮廓、简单拟人和运镜已有限实测，复杂绑定未验证 |
| 共用能力 | caption-alignment | 字幕融合、声音完整性、对齐与样片 |
| 共用能力 | [science-narration](science-narration/SKILL.md) | 科普表现型配音，逐段情绪和实际时长；对应可选audio配置 |
| 共用能力 | [procedural-music-mix](procedural-music-mix/SKILL.md) | 原创程序配乐、侧链、音乐可闻度修订；对应可选audio配置 |
| 共用能力 | video-qa | 技术、视觉、内容、听审和交付证据 |
| 旧入口 | 2d-scenario-explainer | 转到上述规范，兼容历史案例 |

风格从styles/registry.json检索：“暖色手绘科普”和“奶油绘本科普”共用人物情境方法。styles/presets引用visual、layouts、audio以及formats；series/example.json只是栏目配置模板，没有全局默认风格。

请求示例：“做睡眠主题，用奶油绘本科普，面向成年人。”只给主题时按内容推荐，先通过实际角色样张与完整分镜网页讨论，不要求用户指定工具。

当前工具适配器在capabilities/；图像服务读用户指定的个人skill。尚未实现的3D/实拍方法不注册为空壳skill。更多颜色组合新增preset，新的制作步骤新增方法，换服务新增适配器，换主题新建项目。

仓库skills通过AGENTS.md发现；未安装到个人技能目录，不保证在客户端个人列表显示。

独立声音/视觉选项见styles/registry.json的selectable_components：可只选科普配音、只选配乐，或只选SVG机制动画，不隐式打包心脏整片风格。它们有真实案例实现，但目前需要代理按技能适配代码，JSON不会自动驱动渲染。混合镜头与逐步升级规则见[制作方法复用指南](../docs/production-method-reuse.md)。

祈福景观入口：[devotional-landscape](devotional-landscape/SKILL.md)，对应“佛祖保佑 / 金色云海祈福”。method v3已有单期H3、配音与字幕技术实测及v11整片用户接受；见references/production-route.md，仍不是通用production-ready。
