---
name: procedural-music-mix
description: Use when an explainer needs original background music, voice-aware ducking, or louder music without obscuring speech.
---

# 配乐与混音

版本1。按[video-production](../video-production/SKILL.md)的现有授权执行。保留独立旁白与音乐，音量修订建立新版本，不重做未受影响画面。

## 选择与实现

可选配置：[轻快程序配乐与可闻混音](../../styles/audio/procedural-science-mix.json)。音乐生成参考[心脏music-v6.py](../../projects/heart_circulation_mechanism_04/scripts/music-v6.py)，为原创104 BPM、C大调拨弦/低音/轻打击乐，非Music3生成；混音参考[remix-v9.py](../../projects/heart_circulation_mechanism_04/scripts/remix-v9.py)。两者是固定项目脚本，不是通用CLI，复制适配到新episode的唯一run后才在220运行。

v9旁白gain 1.25、音乐gain 1.20、sidechain threshold 0.08、ratio 2、attack 12ms、release 240ms只是案例起点。新旁白/配乐的初始响度与频谱不同，不能用固定增益保证听感。用户选择其他音乐/生成工具优先；确认当前工具状态与来源使用范围，不能将案例原创身份套给外部素材。

## 操作和验收

1. 保存源文件hash、音乐来源/授权、生成器/seed、BPM、时长和淡入淡出。依据实际视频时长生成/编排，避免循环接缝。
2. 先校准旁白清晰度，再提高音乐；音乐仍听不见时同时查看过强的侧链压低，避免只无限提高gain。保留A/B片段，在口播与停顿处试听。
3. 侧链后混合、整体响度归一化，记录完整滤镜。参考目标-16 LUFS、真峰值≤-1.5 dBTP；以[video-qa](../video-qa/SKILL.md)及用户平台要求验收最终编码声轨。归一化改变总音量，不保证音乐相对可闻度。
4. 只改混音时保留视频流，验证video packet hash一致；只改画面且时长、镜头和音频时序不变时才复制已选AAC并验证audio packet hash一致。若画面改动带来时序变化，必须从已接受的旁白和音乐源重新对齐/混音。不能拿旧mix覆盖用户更新过的版本。
5. 依[caption-alignment](../caption-alignment/SKILL.md)核对旁白位置/字幕、音轨长度与末尾≥0.6秒；保存narration/music/mix、music-source、QA与manifest。

[v9 QA](../../projects/heart_circulation_mechanism_04/review/v9-qa.json)证明实际混音、响度与完整解码；听感仍待用户审阅，浏览器播放和技术检查不替代听审。
