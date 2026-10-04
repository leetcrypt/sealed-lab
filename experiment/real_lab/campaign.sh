#!/usr/bin/env bash
# campaign.sh <arm> <R> <sinkport> [N] [START]  — R real capture runs for one arm -> runs-<arm>.jsonl
# START>1 APPENDS runs START..START+R-1 (fresh seeds) instead of truncating.
set -uo pipefail
[ -f experiment/real_lab/fleet.env ] && . experiment/real_lab/fleet.env
ARM=$1; R=$2; PORT=$3; N=${4:-20}; START=${5:-1}
OUT=output/anon-baserate/real-data/runs-$ARM.jsonl; [ "$START" -eq 1 ] && : > "$OUT"
ONION=$(cat /tmp/tor-sink/hs/hostname 2>/dev/null)
for r in $(seq "$START" $((START+R-1))); do
  python3 experiment/real_lab/real_sink.py "$PORT" "$N" /tmp/eg-$ARM-$r.json >/tmp/sink-$ARM.log 2>&1 &
  SINK=$!; sleep 1
  SEED=$((20261003+r))
  case $ARM in
    wg)  ssh -o ConnectTimeout=10 laptop "python3 /tmp/real_client.py direct "$TRILLSEC_TS_IP" $PORT $N $SEED /tmp/in-$ARM-$r.json" >/dev/null 2>&1 ;;
    tor) ssh -o ConnectTimeout=10 laptop "timeout 180 python3 /tmp/real_client.py socks 127.0.0.1 9055 $ONION $PORT $N $SEED /tmp/in-$ARM-$r.json" >/dev/null 2>&1 ;;
    sor) ssh -o ConnectTimeout=10 laptop "timeout 180 python3 /tmp/real_client.py direct 127.0.0.1 48950 $N $SEED /tmp/in-$ARM-$r.json" >/dev/null 2>&1 ;;
  esac
  wait $SINK 2>/dev/null
  scp -q laptop:/tmp/in-$ARM-$r.json /tmp/in-$ARM-$r.json 2>/dev/null
  python3 experiment/real_lab/score_run.py /tmp/in-$ARM-$r.json /tmp/eg-$ARM-$r.json "$ARM" "$r" >> "$OUT"
  echo "[$ARM] run $r done: $(tail -1 "$OUT")"
done
echo "[$ARM] CAMPAIGN COMPLETE ($R runs)"
