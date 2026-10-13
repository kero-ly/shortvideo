---
name: video-production
description: Use when a user provides a video topic, asks to produce an episode, select a style or production route, or continue an existing video project in this repository.
---
# 视频制作统一入口

根目录是本文件向上两级。读AGENTS.md、docs/workflow.md、configs/resources.json；定位已有episode，避免将修订误当新片。用户只需主题和可选风格，不要求其指定工具。

## 选择与版本

读取styles/registry.json。选择优先级：用户显式要求 > 用户已批准的本期配置 > 用户指定系列的默认值 > 根据内容提出的推荐。上一期选择不是永久默认。风格未定时推荐少量适用方向并解释；可在已授权的角色探索中展示差异，不擅自批量生产。准确表达空间/机械结构而现有方法不支持时提出新方法方案，不把人物动画硬套过去。

preset引用visual、layout、audio、format和compatible_methods；制作方法不等于画风。允许逐镜混合方法，但仅执行已实现且本期批准的方法；候选3D/实拍路线不视为可用skill。工具明确指定优先，实际可用性、预算和原生尺寸独立检查；无合适工具则报告阻塞，不静默替换供应商或服务器。

用schemas/production-plan.schema.json和本skill的references/production-plan.example.json建立本期production-plan.json：记录每个配置的ID/version/path/SHA256、选择依据与覆盖项，方法和工具版本、实测状态、审批证据及逐镜路由。读取时合并preset默认值与本期overrides；合并结果在审阅页展示。批准后锁定resolved配置，registry更新不修改已批准项目；修改受影响项另建revision，不篡改历史批准。

## 阶段与调用

1. brief：主题、受众、核心观点、事实来源、时长/画幅、预算与已有素材。缺事实标待核实，不凭症状下诊断。
2. 前期：调用选定方法skill。人物情境读../character-scenario/SKILL.md；先角色实际样张确认，再完整分镜图文网页确认。其他方法按其真实存在的指引执行，不能假设都需要角色母版。
3. 生产：确认图文与工具计划后才TTS、视频生成、建模、合成。素材与任务保留ID/hash；真实音频驱动时间线。方法可调用capabilities脚本和用户指定图像skill，调用前读其当前说明。
4. 合成：读../caption-alignment/SKILL.md；字幕融合、配乐与真实旁白同步。静帧排版检查后提供完整带声低清样片和逐镜网页。明确要求直接完整渲染时按授权执行，不新增审批。
5. 正式输出：用户认可样片或明确要求完成后，按批准props、声音与样式版本在220渲染；读../video-qa/SKILL.md完成分层检查与交付。

只修改字幕/样式时定位批准版本，重做受影响合成与QA，不重跑已接受的角色/H3/TTS。用户要求回退时用版本记录确定目标；不清楚才问。连接异常立即报告，恢复后查原任务避免重复提交。

工具脚本、JSON规范与skill并非自动调度器。使用前核对案例脚本中的旧主题、时码、镜头数和run路径。状态只能根据实际产物推进，不能凭文件存在标记批准/完成。

项目归档：每期任务写projects/<episode-id>/runs/，交付写同项目deliveries/，导航写OUTPUTS.md；Git跟踪的QA/manifest摘要放review/。根runs/deliveries软链接仅兼容历史记录，新任务先适配案例脚本输出路径。素材库暂缓建设。
