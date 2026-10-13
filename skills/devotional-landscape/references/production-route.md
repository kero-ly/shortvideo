# 实测生产路线（method v2）

案例证据：projects/buddha_blessing_05/review/qa-video-v1.json、delivery-manifest-v1.json、lineage-video-v1.json。仅内部审阅案例，不是所有主题都稳定或声音已获公开授权。

复用该期 scripts/h3_episode.py 时改episode解析，job目录唯一，记录prompt_id后恢复而非重复提交。H3首帧15秒请求362帧，原生576×1024/24fps；只去掉最后2帧得到15秒，不循环、冻结或降速。生成尺寸与图像宽高比需实测，源图948×1659采用Lanczos等比cover中心裁切。

第一次只有首帧的生成使主体放大约50%，被拒绝。scripts/h3-static-end-v2.json把末帧也接同一master，storyboard/h3-prompt-v2.txt锁定机位，解决明显相机漂移。此方法仍产生较大云层与遮光变化，不能仅凭两端相同判中段合格；逐秒接触表和完整播放分别检查。

scripts/produce_audio.py分短语TTS，align_and_mix.py用实际WAV时长和faster-whisper词时间，禁止按字数均分。该例六段ASR全匹配，语音尾后0.934秒；原创五声音阶轻钟声与持续音，响度约-16.3LUFS、峰值-1.45dBTP。默认teacher参考来源仅内部测试，公开使用前替换已授权声音或取得具体授权证据。ASR/响度通过不代表实际听审通过。

scripts/render_and_qa.py在220用ffmpeg/libass合成，输出1080×1920为原生画面放大，不是原生1080模型生成。白字黑边、幸福粉色重点实际渲染已检验。全解码、360帧、无黑场及AAC48k立体声检测通过。QA/来源/manifest更新后重算hash，复制文本证据到review；媒体留episode，shared registry按实际dirty状态选择部署。
