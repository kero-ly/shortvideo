# 工厂目录和同步约定

本地 `/Users/ly/Desktop/project/shortvideo` 与 220 `/home/ly/shortvideo` 使用同一个 Git 历史和目录结构。服务器负责模型与生产渲染，本地负责创作、审阅与交付预览。运行环境不跨操作系统复制。

| 目录 | 用途 |
|---|---|
| projects/<episode-id>/ | 每期文案、分镜、生成提示词、时间线、素材清单及版本 |
| skills/ | 经案例验证后沉淀的端到端风格入口，目前尚未正式封装 |
| styles/ | 可复用风格规范及模板 |
| capabilities/ | 配音、图片、视频、音乐、QA 等共用工具适配 |
| renderers/ | Remotion / Blender / Godot 引擎和入口 |
| pipeline/ | 环境检查、任务编排及资源锁 |
| configs/ | 主机和资源配置；resources.json 当前为 220 配置，不代表本地可运行模型 |
| schemas/ | 输入输出约定 |
| library/ | 共用素材的来源、授权和索引 |
| runs/ | 唯一任务目录、中间产物和日志；不入 Git |
| deliveries/ | 成片及随附文件；不入 Git |
| docs/、tests/、deploy/ | 文档、检查、部署维护 |

## 原工程

原仓库完整保存在同级目录 `/Users/ly/Desktop/project/shortvideo-reference-original`，包含原 `.git`、上游 remote 和本轮之前的文件。原上游 https://github.com/deviceagent/shortvideo.git，迁移前 HEAD 为 `020a2f4f`。旧母婴目录保留备份，后续只修改新工厂 projects 下的副本。ASR 模型缓存转移到新工厂 `.cache/asr-model-cache`。

不把上游原仓库嵌套进新工厂 Git，也不向它推送工厂变更。选择性复用时保留许可及来源记录。

## Git 与大文件

追踪：脚本、lockfile、文案、分镜、图片提示词、H3 提示词、结构化案例、媒体 SHA256 清单、轻量 QA 记录。生成图片/视频/音频、模型、缓存、node_modules 和机器虚拟环境不入普通 Git。当前未部署 Git LFS；本地和 220 保留媒体副本。媒体清单未登记前，不应声称素材已完整归档。

本地 origin 指向 `ly@8.92.9.220:/home/ly/shortvideo`（SSH 工作仓库，不是 GitHub）。不要直接推送服务器当前检出的分支。同步步骤：检查两端状态 → 本地提交 → push 到唯一 `sync/<commit>` 分支 → 服务器干净时 `git merge --ff-only sync/<commit>` → 比较 HEAD。服务器若有未提交工作，先备份并审核合并，不用 reset --hard 或 rsync --delete 覆盖。

图片等资源另行 scp/rsync 同名相对路径，不复制 `.git`、虚拟环境和模型缓存。文件写入后记录尺寸和哈希；源图会由后续 H3 任务按清单引用。Git 同步不等于媒体已同步。

## 当前案例

`projects/early_pregnancy_signs_01/`：第一条早孕主题。`h3_v2/` 是当前制作版本，等待人工生成参考图。角色素材放 `h3_v2/references/character/`，分镜首帧放 `h3_v2/references/shots/`。旧 Remotion 矢量版作为 v1 记录保留，成片在 `deliveries/early-pregnancy-20261013-010143-e9a8/`。
