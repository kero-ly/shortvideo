# V2：角色母版 → 每镜首帧 → H3 → 剪辑

本版按用户指定链路重新制作。旧版仅作内容和配音参考，不以程序人物动画冒充 H3 输出。当前状态：OpenLux 已生成母版、设定表和 13 张参考图；13 镜 H3 已出片并抽帧审核，合成与技术验收已完成，内部审阅成片见 PRODUCTION.md。精确生成记录见 review/h3-clips.json，当前交付状态见 PRODUCTION.md。

## 已执行的自动生图路径

用户更新的 OpenLux skill 支持本地参考图编辑。本次全部镜头均上传同一张 `references/character/openlux_character_master_v1.png` 进行编辑；不上传公共图床。镜头文件为 `references/shots/openlux_shot_01_v1.png` 至 `openlux_shot_13_v1.png`；设定表为 `references/character/openlux_character_sheet_v1.png`。实际请求、返回尺寸、SHA256 和评审见 `review/`。

母版实际 1024×1536，设定表 1536×1024。镜头 01 实际 941×1672，其余 1024×1536；保留原图，未声称均为精确 9:16。H3 按 576×1024 生成，后期输出 1080×1920；最终输出分辨率不等于 H3 原生细节分辨率。

`generate_openlux_batch.py` 仅显式选择镜头调用付费图片接口，无自动重试；`run_h3_batch.py` 串行提交本集镜头；`review_h3.py` 检查原片并抽五帧；`compose_h3.py` 合成预览；`finalize_h3.py` 正式渲染与 QA。`prepare_prompts.py` 是初始提示词模板生成器，已有人工修订后不要直接重跑覆盖。现行输入以 shots.json 和 prompts 下文件为准。

## 迭代方式

修改主题或镜头前先检查 `shots.json` 和 `SHOT_LIST.md`。重做图片时使用新的版本文件名，仍以同一角色母版编辑；通过参考图审核后再重做对应 H3 镜头。不要覆盖已有原图或失败版本。镜头 10 当前使用 `prompts/shot_10_h3_v3.txt`；其他镜头使用各自 `shot_XX_h3.txt`。现有 15 张图均已完成，无需再次手工生成。

## 文件与职责

- `prompts/00_*.txt`：人物母版和设定表的 GPT-image2 提示词。
- `prompts/shot_XX_image.txt`：每镜独立、可直接复制的 GPT-image2 完整提示词。
- `prompts/shot_XX_h3.txt`：H3 动作、镜头及稳定性要求；第 10 镜实际采用 `shot_10_h3_v3.txt`，历史失败版本保留。
- `shots.json`：镜头目的、画面构图、参考图路径、H3 提示词与时长目标。
- `references/character/`：OpenLux 生成的人物资产。
- `references/shots/`：OpenLux 编辑生成的单镜首帧。
- `runs/h3-pregnancy-*/`（工厂根目录）：H3 原片及任务审计文件；由 `review/h3-clips.json` 索引。
- `review/`：后续参考图审核、首中尾抽帧、失败原因和选择记录。

## 生成与剪辑约定

优先 FL2VA 首帧图生视频。母版用于生成一致的首帧；H3 每次输入单镜首帧，不输入九宫格。先完成 01 号镜头的 5–8 秒试跑再批量，不把多个人物视图作为一张视频画面。

H3 提示词只安排一个主要动作和一种轻微运镜，不要求同一短片发生多个地点切换。保存 seed、模型/工作流、输入图 SHA256、原始 prompt、实际帧数和生成日志。模型具体可用分辨率、长度约束以服务器工作流实测为准，shots.json 的秒数是剪辑目标而非已验证 API 参数。

镜头 10–13 同样生成 H3 人物情境底片，清单、验孕时间线和医疗提示由 Remotion 叠加，避免模型画错医学文字。旁白统一后期配音，不要求人物口型，不使用 H3 自动生成的语音。最终以配音定剪辑长度；较长信息镜头可延长结尾静帧供阅读，不默认将短片大幅慢放。

必须检查：人物身份/衣着一致、成人观感、肢体与道具稳定、画面确实完成指定动作、无误导阳性结果、无遮挡关键图文。参考图不合格先修图；H3 动作不合格仅重做该镜。最终交付 MP4、封面、SRT、分镜、图片/视频提示词、来源与 QA。

## 已验证的服务状态

220 本机 `http://127.0.0.1:8199` ComfyUI 已实际生成本集 13 镜；客户端为 `capabilities/video-generation/h3_comfy.py`。大部分使用 Turbo 8 steps，第 10 镜返修采用 baseline 20 steps。恢复网络后查询原任务，未重复提交。共享模型与服务不修改；生成、剪辑和渲染均在 220 执行，本地仅创作、归档和预览。
