#!/usr/bin/env bash
set -euo pipefail
root=/home/ly/shortvideo
ed="$root/projects/heart_circulation_mechanism_04"
v1="$ed/runs/20261013-heart-v1"
v2="$ed/runs/20261013-heart-v4"
mkdir -p "$v2" "$root/renderers/remotion/src/heart-sample-20261013"
cp "$ed/scripts/Heart.jsx" "$ed/scripts/math.mjs" "$root/renderers/remotion/src/heart-sample-20261013/"
cd "$root"
uv run python -c 'import json;from pathlib import Path;p=Path("projects/heart_circulation_mechanism_04/runs");d=json.loads((p/"20261013-heart-v1/props.json").read_text());d["revision"]=4;(p/"20261013-heart-v4/props.json").write_text(json.dumps(d,ensure_ascii=False,indent=2))'
cd "$root/renderers/remotion"
for pair in '01 70' '02 210' '03 338' '04 455' '05 605'; do
 read -r shot frame <<< "$pair"
 node_modules/.bin/remotion still src/heart-sample-20261013/Heart.jsx HeartCirculation "$v2/shot$shot.png" --props="$v2/props.json" --frame="$frame" --scale=0.5
 done
node_modules/.bin/remotion render src/heart-sample-20261013/Heart.jsx HeartCirculation "$v2/visual.mp4" --props="$v2/props.json" --codec=h264 --concurrency=3
ffmpeg -y -v warning -i "$v2/visual.mp4" -i "$v1/narration.wav" -map 0:v -map 1:a -c:v copy -af 'loudnorm=I=-16:TP=-1.5:LRA=11,apad' -c:a aac -ar 48000 -ac 2 -t 22.733333 -movflags +faststart "$v2/heart-circulation.mp4"
ffmpeg -y -v warning -i "$v1/visual.mp4" -i "$v1/narration.wav" -map 0:v -map 1:a -c:v copy -af 'loudnorm=I=-16:TP=-1.5:LRA=11,apad' -c:a aac -ar 48000 -ac 2 -t 22.733333 -movflags +faststart "$v1/preview.mp4"
