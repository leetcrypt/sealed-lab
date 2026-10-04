#!/usr/bin/env bash
# clean SOR: trillsec(client) -> grok-bot -> laptop(sink). Stable cloud relay, no mobile confound.
set -uo pipefail
R=${1:-10}; START=${2:-1}; LPORT=48950; SINKPORT=48902; N=20   # START>1 appends (fresh seeds)
OUT=output/anon-baserate/real-data/runs-sor.jsonl; [ "$START" -eq 1 ] && : > "$OUT"
for r in $(seq "$START" $((START+R-1))); do
  SEED=$((20261003+r))
  ssh -o ConnectTimeout=10 laptop "nohup python3 /tmp/real_sink.py $SINKPORT $N /tmp/eg-sorg-$r.json >/tmp/sink-sorg.log 2>&1 &" >/dev/null 2>&1
  sleep 1
  python3 experiment/real_lab/real_client.py direct 127.0.0.1 $LPORT $N $SEED /tmp/in-sorg-$r.json >/dev/null 2>&1
  sleep 1
  scp -q laptop:/tmp/eg-sorg-$r.json /tmp/eg-sorg-$r.json 2>/dev/null
  python3 experiment/real_lab/score_run.py /tmp/in-sorg-$r.json /tmp/eg-sorg-$r.json sor "$r" >> "$OUT"
  echo "[sor-grok] run $r: $(tail -1 "$OUT")"
done
echo "[sor-grok] done: $(wc -l < "$OUT") runs"
