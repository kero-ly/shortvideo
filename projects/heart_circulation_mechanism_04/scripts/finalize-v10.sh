#!/usr/bin/env bash
set -euo pipefail
ed=/home/ly/shortvideo/projects/heart_circulation_mechanism_04
run="$ed/runs/20261013-heart-v10"
ffmpeg -y -v warning -i "$run/visual.mp4" -i "$ed/deliveries/20261013-heart-v9/heart-circulation.mp4" -map 0:v:0 -map 1:a:0 -vf 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p' -c:v libx264 -crf 18 -preset medium -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a copy -movflags +faststart "$run/heart-circulation.mp4"
