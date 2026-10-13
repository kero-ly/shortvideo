#!/usr/bin/env bash
set -euo pipefail
root=/home/ly/shortvideo
ed="$root/projects/heart_circulation_mechanism_04"
run="$ed/runs/20261013-heart-v8"
src="$root/renderers/remotion/src/heart-v8-20261013"
mkdir -p "$run" "$src"
cp "$ed/scripts/Heart-v8.jsx" "$ed/scripts/math.mjs" "$src/"
cp "$ed/deliveries/20261013-heart-v7/props.json" "$run/props.json"
cd "$root/renderers/remotion"
if [[ "${1:-samples}" == samples ]]; then
 for frame in 200 240 280 410 460 489; do
  node_modules/.bin/remotion still "$src/Heart-v8.jsx" HeartCirculation "$run/frame-$frame.png" --props="$run/props.json" --frame="$frame" --scale=0.5
 done
else
 node_modules/.bin/remotion render "$src/Heart-v8.jsx" HeartCirculation "$run/visual.mp4" --props="$run/props.json" --codec=h264 --concurrency=3
 bash "$ed/scripts/finalize-v8.sh"
fi
