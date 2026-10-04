#!/usr/bin/env bash
# fleet-record — multi-angle recording helper for the Sealed Lab demo.
#
# What CAN be automated across the fleet (verified 2026-10-03):
#   - a synchronized CLAPPER (countdown + simultaneous beep on every device) so clips you
#     start by hand on different cameras line up in the editor.
#   - phone SCREEN recording (Android `screenrecord`) + phone AUDIO (`termux-microphone-record`).
# What CANNOT (Termux limitation): CAMERA video on phones (only `termux-camera-photo` stills).
#   -> face/room angles: start your phone's CAMERA APP by hand, then run `clapper` to sync.
#
# trillsec screen video: use OBS (installed) by hand, or the screen-capture skill for stills.
set -euo pipefail
DEVICES=(tril fp6 tab7)              # phones on the tailnet (ssh aliases)

beep_local(){ command -v paplay >/dev/null && paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || printf '\a'; }
beep_phone(){ ssh -o ConnectTimeout=6 "$1" 'termux-tts-speak "mark" 2>/dev/null || printf "\a"' 2>/dev/null & }

case "${1:-help}" in
  clapper)   # 3-2-1 then a simultaneous mark on all devices
    for n in 3 2 1; do echo "  $n..."; sleep 1; done
    echo "  >>> MARK <<<  (align all clips to this beep)"
    for d in "${DEVICES[@]}"; do beep_phone "$d"; done; beep_local; wait 2>/dev/null || true
    date +"sync mark: %Y-%m-%dT%H:%M:%S.%3N" ;;
  screenrec) # screenrec <device> <seconds> -> records that phone's SCREEN, pulls the mp4
    d="$2"; secs="${3:-30}"; f="/sdcard/fleet-rec-$(date +%s).mp4"
    echo "recording $d screen for ${secs}s -> $f"
    ssh "$d" "timeout $secs screenrecord --time-limit $secs '$f'; echo done"
    scp "$d:$f" "demo/footage/$(basename "$f")" && echo "pulled to demo/footage/" ;;
  audio)     # audio <device> <seconds> -> records phone mic (good for a scratch VO track)
    d="$2"; secs="${3:-120}"; f="/sdcard/fleet-audio-$(date +%s).m4a"
    ssh "$d" "termux-microphone-record -f '$f' -l $secs; sleep $((secs+1))"
    scp "$d:$f" "demo/footage/$(basename "$f")" && echo "pulled to demo/footage/" ;;
  *) sed -n '1,20p' "$0" ;;
esac
