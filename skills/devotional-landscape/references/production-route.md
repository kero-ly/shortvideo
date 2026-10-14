# 实测生产路线（method v2）

案例证据：projects/buddha_blessing_05/review/qa-video-v1.json、delivery-manifest-v1.json、lineage-video-v1.json。仅内部审阅案例，不是所有主题都稳定或声音已获公开授权。

复用该期 scripts/h3_episode.py 时改episode解析，job目录唯一，记录prompt_id后恢复而非重复提交。H3首帧15秒请求362帧，原生576×1024/24fps；只去掉最后2帧得到15秒，不循环、冻结或降速。生成尺寸与图像宽高比需实测，源图948×1659采用Lanczos等比cover中心裁切。

第一次只有首帧的生成使主体放大约50%，被拒绝。scripts/h3-static-end-v2.json把末帧也接同一master，storyboard/h3-prompt-v2.txt锁定机位，解决明显相机漂移。此方法仍产生较大云层与遮光变化，不能仅凭两端相同判中段合格；逐秒接触表和完整播放分别检查。

scripts/produce_audio.py分短语TTS，align_and_mix.py用实际WAV时长和faster-whisper词时间，禁止按字数均分。该例六段ASR全匹配，语音尾后0.934秒；原创五声音阶轻钟声与持续音，响度约-16.3LUFS、峰值-1.45dBTP。默认teacher参考来源仅内部测试，公开使用前替换已授权声音或取得具体授权证据。ASR/响度通过不代表实际听审通过。

scripts/render_and_qa.py在220用ffmpeg/libass合成，输出1080×1920为原生画面放大，不是原生1080模型生成。白字黑边、幸福粉色重点实际渲染已检验。全解码、360帧、无黑场及AAC48k立体声检测通过。QA/来源/manifest更新后重算hash，复制文本证据到review；媒体留episode，shared registry按实际dirty状态选择部署。

## v11可选组件与适配路线（method v3）

用户已明确将v11作为最终版：[整片验收](../../../projects/buddha_blessing_05/review/acceptance-v11.json)。这支持本案例画面、字体、声音接受，传播效果暂无数据；既有QA中的pending保留为验收前历史，不能据此覆盖新验收，也不改写历史媒体hash。

| 可独立选择的组件 | 实际参数与实现 | 证据/边界 |
|---|---|---|
| [庄严祈福配音](../../../styles/audio/sacred-spacious-blessing.json) | IndexTTS2，emotion_alpha=.45，实际参考条件合成；[produce_audio_v6.py](../../../projects/buddha_blessing_05/scripts/produce_audio_v6.py)需替换本期文案和路径 | [参考hash](../../../projects/buddha_blessing_05/review/v4-voice-reference.json)、[用户授权](../../../projects/buddha_blessing_05/review/voice-approval-v2.json)。早期-3半音EQ仅v2探索，不是v11必须滤镜；新期选源、验证授权范围、试听 |
| 连续环绕混音（上项组成，可只借处理方法） | [align_v11.py](../../../projects/buddha_blessing_05/scripts/align_v11.py)：完整旁白拼接后卷积；seed1105、IR1.1秒、预延迟25ms、指数衰减常数.19秒、wet=.14；暖持续音/稀疏钟声连续贯穿；侧链threshold=.035、ratio2、attack25ms、release600ms | [混音滤镜与来源](../../../projects/buddha_blessing_05/review/mix-evidence-v11.json)。旁白/音乐/reverb增益1.15/.95/1.15；目标-16LUFS，最终编码实测-15.86LUFS/-4.41dBTP，仅是适配起点 |
| [祈福大斜体字幕](../../../styles/layouts/blessing-large-italic.json) | [make_captions_v9.py](../../../projects/buddha_blessing_05/scripts/make_captions_v9.py)、[render_v11.py](../../../projects/buddha_blessing_05/scripts/render_v11.py)：libass/Noto Sans CJK SC，192字号、粗斜体、白色，第三句实际ASS颜色&H008FA3FF&，按BBGGRR解释为#FFA38F（历史revision标注#FF8FA3与编码不一致，复用以已接受实样为准）；上方Noto Serif CJK SC64，#F6D889 | 无矩形边框但保留14px字形描边；实际效果优先于早期“不要边框”的文字推断。不要把粉色版误降为128字号。新背景/长句需手机尺度检查，题字可换/关闭 |
| [金色云海主角画面](../../../styles/visual/golden-cloud-blessing-v2.json) | 大主体+后方固定光环，前景约6%，背景多层云卷动与金光扫动；[图像prompt](../../../projects/buddha_blessing_05/storyboard/image-prompt-v5.txt)、[运动prompt](../../../projects/buddha_blessing_05/storyboard/h3-prompt-v7.txt)，[h3_episode.py](../../../projects/buddha_blessing_05/scripts/h3_episode.py) | 脸手稳定，主体头顶完整，镜头≤2%；v7进一步主角放大1.08倍。这是prompt目标和单期结果，不是可精确控制的H3运动参数 |

### 起音与句间断层修复

“家”“一”异常与低能量起音被剪相关。本案例[prepare_audio_v11.py](../../../projects/buddha_blessing_05/scripts/prepare_audio_v11.py)从未剪起音源恢复，highpass60Hz+afftdn nr5/nf-45温和处理；仅剪经确认的100ms词后尾部，尾部8ms淡出。新源先比较原始/处理后的波形与实际听感，不按静音阈值自动裁掉轻辅音，也不机械沿用100ms。

本案例拼接起点.15秒，两处源片间隔.35/.55秒；这些是WAV之间的间隔，不等于识别词之间的实际停顿。全旁白总线做连续空间混响，连续音乐使用较缓侧链释放，解决每句尾声被截断、停顿突然无空间感的问题；不要为掩盖断层添加白噪声。改裁剪/重配/停顿后重做真实词对齐，保留至少.6秒完整语音尾部；对首词起音、接缝、末字逐一试听，ASR匹配不代表自然。

### 新期只借声音和字幕的例子

“山水祝福，用v11环绕配音和大斜体字幕，不要佛像”应选择上述audio+layout，保持preset=null，山水另选visual；题字、文案、粉色范围均为本期覆盖。复杂视频按镜头选AI景观、SVG机制或实际已验证工具，合成阶段共用真实旁白时间线、连续音乐/混响和字幕，交接字段见[制作方法复用指南](../../../docs/production-method-reuse.md)。

上述代码均为固定本期路径/14.375秒的案例实现，不能直接作为通用CLI执行。新期适配唯一run、真实时长、工具环境、素材hash与字体配置；保留未受影响素材，不重新生成已接受片段。共享配置只是可选配方，尚无自动运行时加载器。

复用检查还需适配TTS脚本固定GPU7/缓存、渲染默认teacher声源说明与旧approval路径；align_v11.py最终复制v9 ASS header，不能仅改--font-size期待生效。实际字体/颜色以合成后的ASS和渲染实样为准。v1组件文件和历史批准快照保持原路径；v2在独立文件中维护。
