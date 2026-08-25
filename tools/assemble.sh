#!/usr/bin/env bash
# assemble.sh — concat the chained clips, master, extract every frame, sample the seam.
#
# A bash port of the skill's assemble.sh: this container has no zsh and no xxd.
# The logic is unchanged where it matters:
#   * clips 2+ drop their first frame, which is a duplicate of the previous
#     clip's last frame (that frame was literally the start pin)
#   * -fps_mode vfr on the master; CFR padding creates frozen scrub zones
#   * EVERY frame is extracted at the film's native rate — decimating to a round
#     number is what turns a 24fps film into a slideshow under the playhead
#
# Extraction width is 1280 because the source clips are 720p (1286x716). Asking
# for 1440 here would upscale and buy nothing; the engine caps DPR at 1.0 so the
# canvas is close to a 1:1 match on a normal desktop.
set -euo pipefail
export PATH="$HOME/bin:$PATH"

CLIPDIR=${1:?usage: assemble.sh <clip-dir> <frames-out-dir>}
FRAMES=${2:?usage: assemble.sh <clip-dir> <frames-out-dir>}
MASTER="$CLIPDIR/master.mp4"
WIDTH=${WIDTH:-1280}

mapfile -t CLIPS < <(ls "$CLIPDIR"/[0-9][0-9]-*.mp4 2>/dev/null | sort)
[ "${#CLIPS[@]}" -ge 2 ] || { echo "need >=2 clips in $CLIPDIR, found ${#CLIPS[@]}"; exit 1; }
echo "assembling ${#CLIPS[@]} clips"

INPUTS=(); FILTER=""; CONCAT=""
for i in "${!CLIPS[@]}"; do
  INPUTS+=(-i "${CLIPS[$i]}")
  if [ "$i" -eq 0 ]; then
    FILTER+="[${i}:v]setpts=PTS-STARTPTS[v${i}];"
  else
    FILTER+="[${i}:v]select='gte(n\\,1)',setpts=PTS-STARTPTS[v${i}];"
  fi
  CONCAT+="[v${i}]"
done
FILTER+="${CONCAT}concat=n=${#CLIPS[@]}:v=1:a=0[out]"

ffmpeg -y -v error "${INPUTS[@]}" -filter_complex "$FILTER" -map "[out]" \
  -fps_mode vfr -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p "$MASTER"
echo "master: $(ffprobe -v error -select_streams v -show_entries stream=width,height,nb_frames -of csv=p=0 "$MASTER")"

mkdir -p "$FRAMES"; rm -f "$FRAMES"/f_*.jpg
HEAD_TRIM=${HEAD_TRIM:-0}
if [ "$HEAD_TRIM" != "0" ]; then
  echo "trimming ${HEAD_TRIM}s from the head"
  ffmpeg -v error -y -ss "$HEAD_TRIM" -i "$MASTER" -vf "scale=${WIDTH}:-2" \
    -fps_mode passthrough -q:v 6 "$FRAMES/f_%04d.jpg"
else
  ffmpeg -v error -y -i "$MASTER" -vf "scale=${WIDTH}:-2" \
    -fps_mode passthrough -q:v 6 "$FRAMES/f_%04d.jpg"
fi

COUNT=$(ls "$FRAMES"/f_*.jpg 2>/dev/null | wc -l | tr -d ' ')
[ "$COUNT" -gt 0 ] || { echo "FAILED — no frames extracted"; exit 1; }
LAST=$(ls "$FRAMES"/f_*.jpg | sort | tail -1)
echo "frames: $COUNT at ${WIDTH}w, $(du -sh "$FRAMES" | cut -f1)"

# Seam colour: average of the final frame's bottom 12%. The after-film section
# starts at exactly this hex so the handoff has no visible line.
SEAM=$(ffmpeg -v error -i "$LAST" -vf "crop=iw:ih*0.12:0:ih*0.88,scale=1:1" \
        -frames:v 1 -f rawvideo -pix_fmt rgb24 - \
        | python3 -c "import sys;d=sys.stdin.buffer.read();print('%02X%02X%02X'%(d[0],d[1],d[2]))")
echo "FRAME_COUNT=$COUNT"
echo "SEAM=#$SEAM"
