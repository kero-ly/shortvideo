# 工厂工具链状态（2026-10-12）

主目录：220 /home/ly/shortvideo，独立Git仓库。新增文件、缓存、输出均在该目录。配置不含密码。

基础链路已通过：中文文本 → IndexTTS2新旁白 → 实际音频时长 → Remotion动画/字幕 → FFmpeg合成 → 全量解码与QA → deliveries。
测试片：6秒，540×960，24FPS，144帧，48kHz双声道。已人工查看抽帧，中文和主体显示正常；未做ASR逐字或听感验收。不是正式风格样片。

Python使用uv：主环境由pyproject.toml和uv.lock管理，语音环境由uv venv创建。语音借用resources.json中三个外部依赖目录，只读复用；tts-observed-packages.json记录包版本，但不是可迁移的语音lock。共享环境升级可能影响运行，正式生产需固定独立语音依赖。测试音色后续按参考选择。

Remotion/React已固定版本，package-lock.json已生成，Headless Shell已安装。工厂GPU任务有互斥锁，并检查空闲显存；不干预其他用户任务。

可选能力：H3 220本地8199(0.30.0)、H3 219本地8193/8195(0.31.0)、Music3 219本地8207已完成API检查，未生成验收。跨服务器执行/隧道尚未接入。Blender 220为4.0.2、219为5.1.2；Godot仅219已检测到4.7.1；FreeCAD仅219已检测到。均未通过本工厂建模/渲染验收。

操作：进入/home/ly/shortvideo，运行bash deploy/setup-python.sh；uv run python pipeline/doctor.py；uv run python -m unittest discover -s tests -v；选择空闲GPU后运行uv run python pipeline/smoke.py --gpu 0。

正式风格skills、批量调度、阶段缓存与断点恢复、内容事实审核和发布尚未实现。目录和端到端风格流程约定已备好，等待用户参考素材。
