# 视频制作技能入口

用户只需主题和可选风格，代理首先读取 [video-production](video-production/SKILL.md)。它选择方法与风格组合，记录本期计划和确认版本；不是自动模型调度器。

| 层级 | 入口 | 职责 |
|---|---|---|
| 总工作流 | video-production | 主题、选择、阶段、审阅、交付组织 |
| 制作方法 | character-scenario | 角色、场景、完整首帧、动作、H3路线 |
| 共用能力 | caption-alignment | 字幕融合、声音完整性、对齐与样片 |
| 共用能力 | video-qa | 技术、视觉、内容、听审和交付证据 |
| 旧入口 | 2d-scenario-explainer | 转到上述规范，兼容历史案例 |

风格从styles/registry.json检索：“暖色手绘科普”和“奶油绘本科普”共用人物情境方法。styles/presets引用visual、layouts、audio以及formats；series/example.json只是栏目配置模板，没有全局默认风格。

请求示例：“做睡眠主题，用奶油绘本科普，面向成年人。”只给主题时按内容推荐，先通过实际角色样张与完整分镜网页讨论，不要求用户指定工具。

当前工具适配器在capabilities/；图像服务读用户指定的个人skill。尚未实现的3D/实拍方法不注册为空壳skill。更多颜色组合新增preset，新的制作步骤新增方法，换服务新增适配器，换主题新建项目。

仓库skills通过AGENTS.md发现；未安装到个人技能目录，不保证在客户端个人列表显示。
