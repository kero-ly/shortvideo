# Shortvideo Factory

独立生产目录：`/home/ly/shortvideo`（220）。原工程只作为选择性复用来源。

本地创作目录：`/Users/ly/Desktop/project/shortvideo`。两端共享 Git 历史及源文件结构；环境和大文件单独管理。原仓库完整保留在同级 `shortvideo-reference-original`。

- [目录与同步规则](docs/workspace-layout.md)
- [当前早孕视频案例](projects/early_pregnancy_signs_01/README.md)
- [当前 H3 V2 图片生成与归档说明](projects/early_pregnancy_signs_01/h3_v2/README.md)

## 快速验证
```bash
cd /home/ly/shortvideo
uv run python pipeline/doctor.py
uv run python pipeline/smoke.py --gpu 0
```
运行前查看 GPU 占用，选择空闲卡。`--gpu` 是物理卡号；脚本不会停止其他任务。
每次 smoke 创建唯一 runs/smoke-*/，重新生成中文旁白、渲染 Remotion 动画、FFmpeg 合成、解码和 QA。失败保留日志并返回非零；不以已有音频或静音冒充成功。

- skills：未来面向主题的端到端风格入口，尚未安装正式风格 skill。
- styles：风格参数、镜头模板与例片。
- capabilities：通用工具适配（当前实现 narration 与 QA）。
- renderers：画面引擎，当前可执行 Remotion 冒烟片。
- pipeline：编排与环境检查；目前是基础验证，不是完整批量调度器。
- schemas/configs：数据约定、主机与资源位置；不保存凭据。
- projects：每期输入内容；runs：中间产物；deliveries：通过 QA 的成片。
- library：共用素材与来源记录；deploy：安装维护；docs：流程与验收证据。

共享模型仅引用，输出和缓存写本目录。219 服务需从219本机调用或另建SSH隧道；此处没有配置跨服务器凭据。

Python uses uv: orchestration via uv sync / uv run; TTS environment via uv venv. TTS borrows explicitly configured external dependency directories read-only. configs/tts-observed-packages.json is an observed snapshot, NOT a portable lockfile. A separate fully isolated TTS lock remains future work.
