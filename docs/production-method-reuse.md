# 制作方法选择、组合与升级

## 当前可选项

| 用户说法 | 配置/方法 | 实现与证据 | 当前边界 |
|---|---|---|---|
| 科普表现型配音 | science-expressive / science-narration | 心脏tts-v6.py，v6-tts-manifest.json | 支持逐句情绪；不是所有共享TTS都支持，听审pending |
| 轻快程序配乐、音乐能听见 | procedural-science-mix / procedural-music-mix | music-v6.py、remix-v9.py、v9-qa.json | 参数是案例起点；新源需重新混音/试听 |
| SVG机制动画 | svg-mechanism-guidance / 2d-mechanism-explainer | Heart-v10.jsx、math.mjs、v10-QA.md | 路径、箭头、局部形变、聚焦和放大；非任意器官/复杂绑定引擎 |

registry中的selectable_components是代理可读选项，独立于整片presets；没有全局默认，不会自动改变已批准片子。用户授权整理不等于认可全部样例效果。暂不抽象通用API：先借助源码导航在新期有限适配，第二个不同主题验证后再决定稳定接口，避免把心脏专有结构固化。

## 复杂视频按镜头组合

总工作流仍是video-production。每镜记录method、source/hash、实际工具及状态、时长、动作起止、人物/颜色/空间连续性。AI情境开场可走character-scenario，精确流向镜头走SVG；3D/实拍先提出实际工具与验证计划，当前不登记空壳skill。

片段交接记录以下信息（放本期production-plan的shots与review；不是新增自动调度协议）：

- 源视频路径/hash、原生尺寸/fps、可用时长、入出点、是否含音频。
- 目标画布/fps、缩放裁切、字幕安全区；统一编码时明确色彩范围，避免把full-range误当limited。
- 最后/第一帧的主体、位置、方向、颜色语义，连续推近须指明共用锚点；可普通切镜时不强造连续性。
- 配音的真实audioStart/duration、保留/静音源片声音、音乐跨镜方式；统一旁白与字幕阶段完成，不每段各混一遍导致跳音量。
- 静帧、运动关键点、短片接缝检查与失败时只重做受影响阶段。

参考选择：新肾脏科普可先用AI生活情境，再用重画的SVG肾脏结构解释流动，统一配音/音乐/字幕。心脏路径、事实、时码不能沿用；准确复杂空间结构若需3D，验证可用工具后再进入生产。

## 从本期经验升级为共享方法

1. 本期反馈先保留revision、来源/hash、参数、用户原话、QA和A/B例子。
2. 用户授权沉淀时提取方法和可选配置，链接实际代码与证据。configured、reachable、smoke-tested、case-tested和production-approved分别记录，不能跳级。
3. 新主题只做少量代表验证，核对适用条件/失败点。用户接受范围记到本期；成为系列默认需用户明确选择，不因上次成功自动继承。
4. 共享配置改动递增version，旧计划保留resolved快照/hash；失败可回退到上一版本。重复适配显示稳定需求时再抽出通用工具模块并实际测试。

本次仅整理可选方法和案例导航；媒体仍留本期，素材库、自动调度器和个人全局skill安装均未建设。
