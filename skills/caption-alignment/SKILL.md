---
name: caption-alignment
description: Use when aligning narration and subtitles, merging duplicate screen text, repairing clipped speech, mixing background music or revising caption layouts in videos.
---
# 字幕、声音与审阅

执行时读取references/captions-and-review.md。输入为锁定旁白文案、真实旁白/混音音频及hash、镜头时间线、屏幕文字与选定layout；缺真实音频时只可做排版草案，不能声称同步。

输出：语义映射表、含shot_id/source_indices/start/end/text/context的cue、SRT、对齐来源hash、声音来源与时长/尾部检查、可逐句播放的审阅网页。

上下融合需登记每条旧文字去向并保留事实条件，不能只删除上层或机械拼接。主题已在口播出现时省略重复标签；全片主标题独立于逐镜口播。未口播补充事实明确标示。

以词级实际时间定位；哈希一致且片段位置不变才能复用对齐。不得按字数均分；改变配音、剪裁或顺序后重对齐受影响段。完整覆盖旁白，尾句实际结束后默认至少0.6秒，混音不能截断语音。背景音乐记录来源、音量和淡入淡出，实际听审清晰度。

排版参数来自所选layout；用实际手机尺度检查长句、描边和遮挡，静帧之后还要完整带声样片。自动对齐检查与实际听审分别记录；语义正确性需要审校，不因cue格式通过而自动成立。技术QA调用../video-qa/SKILL.md。
