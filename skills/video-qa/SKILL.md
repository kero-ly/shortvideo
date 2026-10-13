---
name: video-qa
description: Use when verifying generated clips or composed videos, assessing audio and caption completeness, or preparing final video delivery with QA and media manifests.
---
# 视频QA与交付

读取本期production-plan、批准版本、时间线与实际媒体。QA输出分开记录，不用单一passed暗示全部验收。

| 类别 | 检查与证据 |
|---|---|
| 技术 | 完整解码、宽高/帧率/帧数/时长、音轨长度、黑帧、响度/峰值；保存ffprobe与日志 |
| 字幕/声音 | 文案覆盖、词级时间来源hash、cue/镜头边界、旁白不截断、尾部留白；语义映射人工审校与自动覆盖分开 |
| 视觉抽样 | 每镜首中尾和动作关键点，角色/肢体/物品、乱码、标题首尾可见、最长字幕、手机及平台安全区；异常扩大检查 |
| 内容 | 本主题事实与适用条件、来源、角色/声线/音乐授权范围；不沿用其他主题结论 |
| 完整播放与实际听审 | 是否完成、审阅者、问题、结论；未执行明确pending，抽帧与自动检测不能替代 |

默认平台目标H.264/yuv420p、AAC48k双声道，响度-19至-13LUFS、真峰值≤-1dBTP；用户/平台要求优先。结尾完整语音后默认≥0.6秒。检查当前声轨对应当前时间线，不能只核对总时长。

生成原片只有审核接受才进入合成；技术失败修受影响阶段。任何缺项标明，不将未完成的听审写为通过。可交付技术通过但待听审的内部审阅版；发布范围与素材授权未核实时如实标注，不代用户发布。

交付到deliveries/<unique-run>/：MP4、封面、SRT、props/时间线、来源/镜头索引、QA、manifest（文件SHA256）。标明原生生成分辨率及合成输出分辨率。220渲染/抽帧，下载本地逐文件验hash并确认网页视频加载。媒体不入Git，源码/提示词/清单入Git按docs/workspace-layout.md同步；两端脏文件先检查备份。

目前可参考两期案例QA脚本，但新期须适配镜头数、时间、路径和断言。没有通用QA执行器时逐项调用工具，不把本skill说成已自动执行。
