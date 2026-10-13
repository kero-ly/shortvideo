---
name: science-narration
description: Use when Chinese science narration sounds flat or needs segment-level emphasis, emotional delivery and timing based on actual speech.
---

# 科普配音

版本1。先确定每句的信息重点、语速、停顿和情绪，再生成真实音频；声音风格与声线身份分别选择。仓库路径均相对根目录。

## 选择与执行

可选配置：[科普表现型声音](../../styles/audio/science-expressive.json)。当前实现是[心脏tts-v6.py](../../projects/heart_circulation_mechanism_04/scripts/tts-v6.py)，输入plan数组，每项为id、text、duration_ms、emotion_vector；配置emotion-alpha。该脚本参数化输入输出，可作为本期副本适配。不要直接运行历史produce-v6.py：它固定心脏文案、路径和任务目录。

共享capabilities/narration/indextts2.py使用参考音频情绪，目前不读取逐段emotion_vector，不能把配置JSON当作已接入共享适配器。读取案例produce-v6.py只用于了解依赖与调用，再按configs/resources.json、TTS运行环境和本期唯一run构造调用；模型工作前检查220 GPU，外部依赖只读。

1. 按[video-production](../video-production/SKILL.md)确认制作授权；完整图文生产批准或显式TTS授权才进入生成，角色/参考图授权不代替它。已有授权不重复询问。以锁定文案制作短句plan；向量顺序为happy, angry, sad, afraid, disgusted, melancholic, surprised, calm。案例用happy/surprised/calm组合，0.85是案例alpha，不是通用最优值。
2. 每次选择声线均核实来源和使用范围，包括已有配置的参考声音；路径或运行manifest不证明授权。挑有长句、术语和转折的代表句试听，按已有授权继续。
3. 保存原WAV、文本、向量、参考音频来源/hash、参数、实际时长和manifest。duration_ms只是计划槽，不能当作实测时长或机械变速依据。
4. 按实际WAV重新编译时间线，调用[caption-alignment](../caption-alignment/SKILL.md)进行真实音频对齐；仅音量修订且源音频位置不变时复用ASR，不重做TTS。

## 证据与验收

[v6运行与参数记录](../../projects/heart_circulation_mechanism_04/review/v6-tts-manifest.json)、[v10 QA](../../projects/heart_circulation_mechanism_04/review/v10-QA.md)证明案例运行与技术检查；它们不证明声音授权或完整听审。实际听审仍pending。交付独立旁白及带音乐片段，检查术语、重音、句尾完整性和语气；不要因情绪参数存在就宣称听感优秀。新主题保留已接受声音的对比版本，修改仅影响本期覆盖项。
