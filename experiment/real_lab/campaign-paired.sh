#!/usr/bin/env bash
# PAIRED Tor+SOR: same SEED per run -> identical latent patterns through both transports,
# so runs are truly paired (removes deviation D-real-1). Uses the FROZEN paired decision rule.
set -uo pipefail
R=${1:-15}; N=20
ONION=$(cat /tmp/tor-sink/hs/hostname)
OUT=output/anon-baserate/real-data/paired.jsonl; : > "$OUT"
for r in $(seq 1 "$R"); do
  SEED=$((30000+r))
  # Tor arm: laptop client -> onion -> trillsec sink
  python3 experiment/real_lab/real_sink.py 48900 $N /tmp/eg-ptor-$r.json >/tmp/s1.log 2>&1 & S1=$!
  sleep 1
  ssh -o ConnectTimeout=10 laptop "timeout 180 python3 /tmp/real_client.py socks 127.0.0.1 9055 $ONION 48900 $N $SEED /tmp/in-ptor-$r.json" >/dev/null 2>&1
  wait $S1 2>/dev/null
  scp -q laptop:/tmp/in-ptor-$r.json /tmp/in-ptor-$r.json 2>/dev/null
  TOR=$(python3 experiment/real_lab/score_run.py /tmp/in-ptor-$r.json /tmp/eg-ptor-$r.json tor $r)
  # SOR arm: trillsec client -> grok -> laptop sink (SAME SEED = same patterns)
  ssh -o ConnectTimeout=10 laptop "nohup python3 /tmp/real_sink.py 48902 $N /tmp/eg-psor-$r.json >/tmp/s2.log 2>&1 &" >/dev/null 2>&1
  sleep 1
  python3 experiment/real_lab/real_client.py direct 127.0.0.1 48950 $N $SEED /tmp/in-psor-$r.json >/dev/null 2>&1
  sleep 1
  scp -q laptop:/tmp/eg-psor-$r.json /tmp/eg-psor-$r.json 2>/dev/null
  SOR=$(python3 experiment/real_lab/score_run.py /tmp/in-psor-$r.json /tmp/eg-psor-$r.json sor $r)
  python3 -c "import json; t=json.loads('''$TOR'''); s=json.loads('''$SOR'''); print(json.dumps({'run':$r,'tor_tpr':t.get('tpr'),'sor_tpr':s.get('tpr'),'gap':(t.get('tpr',0)-s.get('tpr',0)) if 'tpr' in t and 'tpr' in s else None,'tor_auc':t.get('auc'),'sor_auc':s.get('auc')}))" >> "$OUT" 2>/dev/null
  echo "[paired] run $r: $(tail -1 "$OUT")"
done
echo "[paired] done: $(wc -l < "$OUT") runs"
