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
