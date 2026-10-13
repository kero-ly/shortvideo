#!/usr/bin/env bash
set -euo pipefail
ed=/home/ly/shortvideo/projects/heart_circulation_mechanism_04
v="$ed/runs/20261013-heart-v5"
ffmpeg -y -v warning -i "$v/visual.mp4" -i "$ed/deliveries/20261013-heart-v4/heart-circulation.mp4" -map 0:v -map 1:a -vf 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p' -c:v libx264 -crf 18 -preset medium -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a copy -t 22.733333 -movflags +faststart "$v/heart-circulation.mp4"
