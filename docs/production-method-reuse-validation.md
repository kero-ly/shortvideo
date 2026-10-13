# 制作方法沉淀验证 · 2026-10-13

范围：科普配音、程序配乐/混音技能；SVG案例导航升级到v10；独立可选组件与混合镜头约定。没有生成新媒体、安装个人skill或把效果标记为用户批准。

## 独立场景检查

测试任务：“新肾脏科普：表现型配音、可闻配乐、SVG机制＋AI开场＋候选3D”，只读路由，不生产。

- 基线：总入口能找到器官方法，但引用停在早期Heart.jsx/QA.md；v6情绪配音、v9混音、v10引导组件不可从标准入口直接发现。共享TTS与案例向量TTS不同，原音频配置为陪伴/低音量。
- 配音回测：代码/配置匹配；补充每次声线来源范围检查及制作授权边界，manifest只证明运行参数。
- 混音回测：生成器、v9滤镜、源文件和hash规则吻合；补充只有时序不变才复制AAC，避免音画错位。
- SVG/组合回测：可发现源码和QA；明确新结构验证、候选3D、片段接口和无全局默认。
- 集成发现schema强制preset对象。先验证新示例仅在selection.preset=null处失败，再修改schema；5个当前计划与示例全部通过，包括旧preset对象和新null形式。
- 最终独立检查：无本轮范围内的实质遗留问题。

## 静态验证

skill-creator quick_validate：science-narration、procedural-music-mix、2d-mechanism-explainer、video-production通过。registry组件id/version、skill、实现/证据文件及Markdown引用检查通过；git diff --check通过。

执行行为证据来自已交付心脏v6/v9/v10，本轮文档检查不代表新的TTS或渲染测试。听审、跨主题效果及用户最终接受范围仍逐期记录。
