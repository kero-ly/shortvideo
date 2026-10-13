# 风格组合注册表

唯一当前索引：registry.json。命名为“画面类型 · 色调 · 场景与表达”；主题与工具不属于画风。没有全局默认风格。

- 暖色手绘科普：2d-handdrawn-warm-light-muted-daily-explainer@1
- 奶油绘本科普：2d-storybook-cream-warm-daily-list-explainer@2

presets/组合visual/画面、layouts/排版、audio/声音和../formats/内容组织，兼容方法目前为character-scenario。用户覆盖项写入本期production-plan，不直接修改全局默认。修改已发布配置时递增version，保留Git历史；已批准项目锁定引用hash和resolved快照。

2d-handdrawn/旧JSON保留为历史兼容快照，新任务以registry和presets为准，不双重维护。两种风格均有内部审阅案例；奶油绘本技术QA通过，完整人工听审及声线公开使用权未核实。

JSON供代理读取并形成计划，尚未实现自动加载到Remotion或自动风格选择器。所有样式参数需在本期实际图像与手机尺度样片验证。

金色云海祈福：golden-cloud-buddha-blessing@1。写实佛像、金色体积云、海滩前景、白字黑边/粉色重点；当前configured_preproduction_only，未完成视频/声音/renderer验证。
