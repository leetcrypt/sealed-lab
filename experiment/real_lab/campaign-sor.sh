#!/usr/bin/env bash
# best-effort SOR: fresh per-run 2-hop tunnel (phone relay), skip runs that fail to tunnel
set -uo pipefail
R=${1:-6}; PORT=48901; N=20
OUT=output/anon-baserate/real-data/runs-sor.jsonl; : > "$OUT"
for r in $(seq 1 "$R"); do
  SEED=$((20261003+r))
  # fresh tunnel for this run
  ssh -o ConnectTimeout=12 laptop 'pkill -f "NL 48950" 2>/dev/null; sleep 1; for rel in tril fp6 tab7; do timeout 22 ssh -o ExitOnForwardFailure=yes -o ConnectTimeout=10 -J $rel -fNL 48950:127.0.0.1:48901 trillsec 2>/dev/null && { sleep 2; ss -ltn|grep -q 48950 && exit 0; }; done; exit 1' >/dev/null 2>&1
  if ! ssh -o ConnectTimeout=8 laptop 'ss -ltn 2>/dev/null | grep -q 48950' >/dev/null 2>&1; then
    echo "[sor] run $r: no tunnel, skip"; continue; fi
  python3 experiment/real_lab/real_sink.py "$PORT" "$N" /tmp/eg-sor-$r.json >/tmp/sink-sor.log 2>&1 &
  SINK=$!; sleep 1
  ssh -o ConnectTimeout=10 laptop "timeout 160 python3 /tmp/real_client.py direct 127.0.0.1 48950 $N $SEED /tmp/in-sor-$r.json" >/dev/null 2>&1
  wait $SINK 2>/dev/null
  scp -q laptop:/tmp/in-sor-$r.json /tmp/in-sor-$r.json 2>/dev/null
  python3 experiment/real_lab/score_run.py /tmp/in-sor-$r.json /tmp/eg-sor-$r.json sor "$r" >> "$OUT"
  echo "[sor] run $r: $(tail -1 "$OUT")"
done
echo "[sor] done: $(wc -l < "$OUT") runs captured"
