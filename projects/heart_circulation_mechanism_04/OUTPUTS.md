# 本期输出

- 最新路径引导版：`deliveries/20261013-heart-v8/index.html`；第二、三镜加入起点圈选、金色路径、沿血流方向箭头、终点提示。声轨逐包复用 v7，时间线不变。
- v8 源码：`scripts/Heart-v8.jsx`；渲染：`bash scripts/render-v8.sh samples` 后 `bash scripts/render-v8.sh full`（仅在220）；打包：项目根执行 `uv run python projects/heart_circulation_mechanism_04/scripts/package-v8.py`。版本证据：`review/production-plan-v8.json`、`review/v8-manifest.json`、`review/v8-QA.md`。
- 当前审阅（人声略降、音乐略升）：`deliveries/20261013-heart-v7/index.html`（完整混音视频、v6对照和五镜分镜）。
- 视频：`deliveries/20261013-heart-v7/heart-circulation.mp4`，1080×1920 / 30fps / 28.067秒；`review/v7-manifest.json`记录23项交付文件SHA256。
- 上一版配音与配乐：`deliveries/20261013-heart-v6/index.html`，保留纯配音、单独配乐和v5对照。
- 上一版全屏排版：`deliveries/20261013-heart-v5/index.html`，保留原配音、无背景乐，22.733秒。
- 220工程根：`/home/ly/shortvideo/projects/heart_circulation_mechanism_04`。
- 本地工程根：`/Users/ly/Desktop/project/shortvideo/projects/heart_circulation_mechanism_04`。
- v6逐镜旁白源：`runs/20261013-heart-v6/audio/`，220保存；v7复用同一旁白、配乐和视频画面，只重混并重新封装。两端交付文件SHA256逐项验证。
- 原创源图为`scripts/Heart.jsx`内SVG；没有复用抖音图像/音乐。
- 历史v1/v2/v3/v4保留，未替换已哈希的历史交付。
- 技术/视觉与播放检查、实际听审分开记录，见`review/v7-QA.md`（本版）、`review/v6-QA.md`和`review/QA.md`（历史）。
