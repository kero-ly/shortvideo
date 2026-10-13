#!/usr/bin/env bash
set -euo pipefail

episode=/home/ly/shortvideo/projects/heart_circulation_mechanism_04
previous="$episode/deliveries/20261013-heart-v6"
run="$episode/runs/20261013-heart-v7"
delivery="$episode/deliveries/20261013-heart-v7"

if [[ -e "$run/mix.wav" || -e "$delivery/manifest.json" ]]; then
  echo 'v7 output already exists; refusing to overwrite it' >&2
  exit 1
fi
mkdir -p "$run"

ffmpeg -y -v warning -i "$previous/narration.wav" -i "$previous/music-original.wav" \
  -filter_complex '[0:a]aresample=48000,volume=1.25,asplit=2[voice][side];[1:a]volume=0.60[music];[music][side]sidechaincompress=threshold=0.025:ratio=5:attack=12:release=240[duck];[voice][duck]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=8:linear=false,aresample=48000[mix]' \
  -map '[mix]' -ac 2 "$run/mix.wav"

ffmpeg -y -v warning -i "$previous/heart-circulation.mp4" -i "$run/mix.wav" \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -shortest -movflags +faststart "$run/heart-circulation.mp4"
