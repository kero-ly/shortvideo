#!/usr/bin/env bash
set -euo pipefail
root=/home/ly/shortvideo
ed="$root/projects/heart_circulation_mechanism_04"
v1="$ed/runs/20261013-heart-v1"
v2="$ed/runs/20261013-heart-v6"
mkdir -p "$v2" "$root/renderers/remotion/src/heart-v6-20261013"
cp "$ed/scripts/Heart.jsx" "$ed/scripts/math.mjs" "$root/renderers/remotion/src/heart-v6-20261013/"
cd "$root"
cd "$root/renderers/remotion"
for shot in 01 02 03 04 05; do
 frame=$(uv run python -c "import json; p=json.load(open('$v2/props.json'));s=p['shots'][int('$shot')-1];print(s['start']+s['frames']//2)")
 node_modules/.bin/remotion still src/heart-v6-20261013/Heart.jsx HeartCirculation "$v2/shot$shot.png" --props="$v2/props.json" --frame="$frame" --scale=0.5
 done
node_modules/.bin/remotion render src/heart-v6-20261013/Heart.jsx HeartCirculation "$v2/visual.mp4" --props="$v2/props.json" --codec=h264 --concurrency=3
