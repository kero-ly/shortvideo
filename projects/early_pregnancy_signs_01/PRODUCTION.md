# 早孕可能出现的 8 个信号 · 第一版制作记录

## 本集实现

- 主生产位置：220，`/home/ly/shortvideo/projects/early_pregnancy_signs_01`。
- 本地目录保存创作稿、镜头代码和交付副本。原仓库仅作为参考，不调用其大型 Root.tsx 或其他作者的影片素材。
- `episode.json`：本集锁定文案和 13 个场景；实际时长按旁白生成，79.583 秒。
- `EarlyPregnancy.jsx`：原创矢量角色、生活情境、表情/动作、信息卡和封面。使用工厂已装的 Remotion。
- `produce.py`：通过 uv 启动，选择空闲 GPU、调用工厂 IndexTTS2 适配器、拼接旁白、编译时间线、渲染低清片。
- `align_captions.py`：将 Whisper-small 逐字时间对齐锁定文案，保留医学用语原文；不将 ASR 误识别直接写进字幕。
- `finalize.py`：生成轻量原创伴奏、混音、1080p 渲染、封面、逐镜抽帧、技术 QA 与交付目录。

## 素材与来源

| 资源 | 来源 / 实际使用情况 |
|---|---|
| 角色、背景、道具、卡片 | 本集原创 SVG / React 代码绘制，无参考作者画面拷贝 |
| Atlas | 通过指定 skill 调用；接口返回 HTTP 402 `insufficient balance`，未生成或使用 Atlas 图片 |
| 旁白 | 220 已配置的 IndexTTS2；参考为工厂既有 `teacher_reference_24k.wav`，emotion_alpha=0.45；未克隆淼爸或诗诗的声音；既有参考录音的授权未在本轮单独审计 |
| 音乐 | `finalize.py` 本次程序合成的原创轻柔音型，无第三方录音采样 |
| 字体 | 服务器 Noto Sans CJK SC，Noto 字体采用 SIL Open Font License |
| 医学事实 | NHS 下列页面；本轮重新读取核对 |

医学来源：

1. https://www.nhs.uk/pregnancy/trying-for-a-baby/signs-and-symptoms-that-might-mean-youre-pregnant/
2. https://www.nhs.uk/pregnancy/trying-for-a-baby/doing-a-pregnancy-test/

八个信号对应来源中的月经推迟、疲倦、乳房敏感、恶心、嗅觉敏感、尿频、食物偏好变化和情绪变化；非诊断评分。验孕时机和复测建议对应第二页；第一页面同时提示腹痛、盆腔痛、阴道出血等情况需要求助。

## 验证与边界

技术检查由 `qa.json` 记录：分辨率、帧率、总帧数、H.264/yuv420p、AAC、48kHz 双声道、时长、完整解码、黑帧、响度和字幕时序。

Whisper-small 自动回听核对字符相似度为 97.7%。差异为“歇/些”“经前/金钱”“频繁/平凡”“验孕/艳运”“猜/彩”等识别结果，详见 `speech-review.json`。同音词识别差异不等同于确认配音读错；未声称进行真人逐句听审。字幕依据锁定文本，时间根据 ASR 校准。

这是可播放的第一版成片，用于进一步评价画风、声音和节奏；尚未发布到抖音。采用轻量矢量情境动画，不是 Atlas 插画或逐帧角色表演。工厂尚未将本集封装成安装版风格 skill。

## 下次复用

可以复用人物组件、场景、安全区、字幕对齐、混音与 QA；新主题必须重新审核文案和设计适合的情境，不能仅替换标题。后续风格 skill 应将此处实际跑通的流程串起来，并把内容资料、角色风格版本和工具配置分开。
