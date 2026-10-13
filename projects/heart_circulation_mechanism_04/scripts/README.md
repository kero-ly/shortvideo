# 案例脚本与重现

所有渲染/合成/抽帧只在220。本目录是本期案例，尚非通用调度器。历史job ID和成片时间已固化，禁止直接覆盖重跑；新作先分配唯一run/delivery并适配所有路径、文字和测量时长。

1. `math.test.mjs`验证弧长采样、环路连续与帧确定性。
2. `produce.py`读取resources，GPU0空闲检查后在工厂锁内调用IndexTTS2；实际逐句WAV生成props和完整旁白。新任务先重新检查GPU。现有manifest触发防覆盖。
3. `Heart-v1.jsx`、`Heart-v2.jsx`、`Heart-v3.jsx`保留历史源；`Heart.jsx`为v4。
4. `render-v4.sh`复制本期源到Remotion暂存入口，在220输出全部中间参考帧和1080p视频。
5. `finalize-v4.sh`转换bt709 limited/yuv420p并合入旁白；不能跳过此步直接发布Remotion原始色彩标记。
6. `package-v4.py`在220解码、抽帧、响度检查，生成审阅HTML、SRT和SHA256。实际视觉/播放/听审另记QA。
7. 只为本地播放启动HTTP静态服务不属于本地视频渲染。

旁白按每句源WAV实测容器时长定位；没有假造逐字时间。素材库与全局风格注册均未扩展。


v5排版修订：`Heart-v4.jsx`锁定旧版源，当前`Heart.jsx`为v5；执行`render-v5.sh`→`finalize-v5.sh`→`package-v5.py`。v5直接拷贝v4 AAC声音流，另建唯一run。

## v6 audio revision

Visual layout and locked text remain v5. produce-v6.py queues on the factory GPU lock and verifies GPU6 memory before IndexTTS2 work. tts-v6.py is an episode-scoped adapter copy with happy/surprised/calm vectors. WAV durations drive new props, without tempo acceleration.

Orchestration uses uv run on 220. music-v6.py uses the configured TTS Python for NumPy. align-v6.py uses the existing tested faster-whisper 1.2.1 environment /home/ly/.cache/uv/archive-v0/EHM1RV4AF41ciiYBgIu3A/bin/python. This cache is not a portable lockfile. FFmpeg decodes 16k float PCM into an ndarray to avoid an incompatible PyAV keyword.

Then run render-v6.sh, finalize-v6.sh and uv run python .../package-v6.py. music-v6.py is original procedural 104 BPM C-major pluck/bass/light percussion, with no external recordings; voice-driven music ducking, 0.7s fade-in/1.2s fade-out and -16LUFS/-1.5dBTP targets. Fixed v6 paths belong to this revision; future runs need new IDs and must preserve this delivery.
