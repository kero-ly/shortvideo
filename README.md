# Shortvideo Factory · 短视频生产工厂

输入主题与可选风格，先看角色与完整分镜图文，再生成视频、对齐声音字幕、审阅和交付。当前验证过暖色手绘、奶油绘本两种人物情境科普案例；这是技能规范＋配置＋工具适配器，尚非自动批量调度器。

## 从哪里开始

给agent：“读取AGENTS.md和skills/video-production/SKILL.md，用奶油绘本科普做【主题】，面向【受众】，重点讲【观点】。”也可以只给主题，由agent推荐适合的风格与制作方法。明确指定工具、风格或范围优先；上一期风格不自动成为默认。

选择顺序：用户显式要求 → 本期批准配置 → 用户指定栏目的默认配置 → 内容推荐。方案记录配置ID、版本、hash、覆盖项、工具实测状态和批准依据。批准后锁定resolved配置，后续全局更新不修改旧片。

## 一期一个目录

所有一期的内容与生产产物收在projects/<episode-id>/：

```text
projects/<episode-id>/
  brief.json / PREPRODUCTION.md    内容与前期方案（按现有项目实际格式）
  production-plan.json             方法、风格、工具、版本与确认
  scripts/                        本期适配脚本
  storyboard/                     新期分镜、中文文案、prompt、参考索引
  references/                     新期角色、场景、参考帧（媒体不入Git）
  timeline/                       配音时长与字幕
  review/                         批准记录、QA、来源和媒体hash
  runs/<unique-job-id>/            任务日志、中间媒体和失败记录
  deliveries/<unique-delivery-id>/ 成片、封面、SRT、网页、QA与manifest
  OUTPUTS.md                      本期产物导航
```

已有案例的h3_v2、generated等子目录保留，避免破坏来源记录。两期根目录runs/deliveries中的既有产物已迁入各自项目；旧路径保留软链接，使旧脚本、hash清单和已打开网页继续可用。根runs只用于环境检查、全局smoke、迁移备份等非单期任务。新期直接写项目内目录，不继续依赖旧路径。

旧版HTML可能使用相对根路径，历史审阅页从OUTPUTS.md里的兼容URL打开；新网页需按项目位置生成正确链接。归档/备份项目时包含项目实际目录；不要只复制根目录兼容软链接。服务器保留较完整的中间产物，本地可能仅有审阅与交付副本。

当前项目：
- [第一期：暖色手绘](projects/early_pregnancy_signs_01/OUTPUTS.md)
- [第二期：奶油绘本](projects/early_pregnancy_signs_storybook_02/OUTPUTS.md)

## 技能与配置分层

| 位置 | 职责 |
|---|---|
| skills/video-production | 统一入口：选择、确认、阶段与交付组织 |
| skills/character-scenario | 人物母版、完整场景首帧、动作/运镜与视频生成方法 |
| skills/2d-mechanism-explainer | 二维器官/机制动画；心脏循环SVG/Remotion样片已在220有限实测，非通用骨骼/解剖引擎，风格待用户接受 |
| skills/caption-alignment | 字幕融合、真实声音对齐、混音与带声审阅 |
| skills/science-narration、procedural-music-mix | 科普表现型配音、程序配乐与可闻混音；可独立选择，有案例代码和QA |
| skills/video-qa | 技术、视觉、内容、完整听审分别验收 |
| styles/registry.json、presets/ | 别名检索、风格组合与兼容方法 |
| styles/visual、layouts、audio | 画风、字幕外观、声音表现规范 |
| formats/ | 清单、情境解释等内容结构 |
| series/ | 用户明确选定栏目的默认配置，example不是启用配置 |
| capabilities/、renderers/ | 模型服务适配器与实际渲染实现 |
| schemas/、configs/ | 数据约定与环境资源配置 |
| library/ | 现有来源归属记录；素材库建设暂缓 |

旧skills/2d-scenario-explainer是兼容转向；旧styles/2d-handdrawn是历史快照，新配置以registry/presets为准。仓库skill通过AGENTS.md发现，未自动安装进个人skill列表。详细入口见[skills/README.md](skills/README.md)。

独立可选项在registry.selectable_components，可说“科普表现型配音＋轻快程序配乐＋SVG机制动画”，也可只选其中一项。当前为案例实测、待逐期验证与听审，非自动加载器或全局默认。混合视频按镜头选择方法，复用/升级规则见[制作方法复用指南](docs/production-method-reuse.md)。

## 制作与审阅流程

1. 明确主题、受众、事实、风格、工具与成本；未知事实标明待核实。
2. 人物视频先生成有限角色母版和设定图，展示真实图片确认。其他方法按自身设计产物，不强制套角色流程。
3. 角色确认后完成全部分镜参考帧，包含背景、道具、动作起点与文字留白；网页逐镜展示中文旁白、屏幕文字、动作、运镜、时长和prompt。完整图文版本确认后才配音/H3/建模/合成。
4. 以真实音频时长建立时间线。上下文字需语义去重融合，不能只删一层；词级时间来自实际音频，复用需核对hash及位置。
5. 排版静帧检查后输出完整带声低清样片，核对连贯性；用户认可或明确要求完成后渲染正式尺寸。已授权步骤不重复请求批准。
6. 全片解码、尺寸/帧数/音轨/黑帧/响度检查；逐镜视觉和完整听审分别记录。尾句完整结束后默认至少0.6秒，技术通过不等于听审通过。
7. 交付MP4、封面、SRT、时间线、来源、QA和SHA256清单；下载后验证hash与网页加载。只改排版不重跑已接受H3/TTS。

## 如何扩展

| 新需求 | 改哪里 | 怎么验证 |
|---|---|---|
| 新画风/色调/比例 | visual＋preset | 角色和场景样图，手机尺度预览 |
| 字幕/标题外观 | layouts；需要新动效时同时改renderer | 长句/不同背景/安全区＋带声片段 |
| 新声线/音乐形态 | audio；具体音频留本期或未来素材库 | 试听、来源授权、混音清晰度 |
| 新叙事形式 | formats | 文案分镜和节奏样片 |
| 制作步骤明显不同 | 新方法skill | 代表镜头端到端验证，不建空壳入口 |
| 换模型/服务/工具优化 | capabilities＋相关skill | 输入输出、超时恢复、实际生成、成本与质量 |
| 常用组合/栏目习惯 | presets或series | 兼容性＋用户确认 |
| 新主题 | 新episode | 不复用旧事实/音轨/固定时码 |

先检索已有能力，再做有限样例；登记configured/reachable/smoke-tested/production-approved范围。样例成功不等于全部场景可用。扩展配置递增version，新项目解析组合，旧项目保持锁定版本。字幕逐字高亮等不只是JSON外观，需要词级时间与渲染组件共同支持。

仅本期调整写overrides；用户明确说“以后使用/加入风格”才沉淀共享默认。工具、风格和素材授权分别记录。素材库暂不搭建，先保留每期媒体、来源、hash和生成关系，积累案例后再建设。

## 环境、Git与归档

220主机/home/ly/shortvideo负责视频生成、合成、渲染和抽帧；本地/Users/ly/Desktop/project/shortvideo负责创作与预览。220故障立即告知，不转本地或219。Python用uv；共享/home/video只读，不停止共享任务。原仓库shortvideo-reference-original仅参考。

Git只追踪源代码、规范、prompt、来源、QA摘要和媒体hash；项目runs/deliveries及图片/音视频不入Git。需版本追踪的QA/manifest副本放review/。媒体单独传输，不把路径存在或HTTP成功说成生产可用。

同步：两端查状态 → 本地提交 → push到唯一sync分支 → 服务器干净或冲突文件备份后ff-only合并 → 对比HEAD。禁止覆盖脏文件、reset --hard、rsync --delete。媒体同步另做SHA256验证。迁移工具pipeline/archive_episode_outputs.py仅处理已知两期，默认dry-run，--apply移动并留旧路径软链接，不用于猜测新项目归属。

维护前读[AGENTS.md](AGENTS.md)、[目录同步约定](docs/workspace-layout.md)、[工作流](docs/workflow.md)。格式检查可用skill-creator的quick_validate；同时验证registry→preset→组件引用和项目Schema，再做有代表性的实际或只读场景验证。文档通过不等于模型/视频已通过生产验证。

新增前期路线：[金色云海祈福](styles/presets/golden-cloud-buddha-blessing.json) 与 [祈福景观方法](skills/devotional-landscape/SKILL.md)。已有15秒H3、分段配音、原创配乐与字幕实测，交付内部审阅版；听审和声线公开授权待确认，不是通用端到端就绪。案例：[佛光祈福图文 v1](projects/buddha_blessing_05/storyboard/v1.md)。

可复用的参考图动画修订经验见[孕周案例](skills/caption-alignment/references/pregnancy-revision-lessons.md)：数字配音规范、局部重配、字幕避让和音轨交付。候选母婴配置未成为系列默认；技术证据、完整听审和传播效果分别记录。
