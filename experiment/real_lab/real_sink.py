"""Real capture sink (egress observer). Accepts N sequential connections; for each, records
a per-bin byte-count series from real arrival timestamps. Own-fleet only. Stdlib.
usage: real_sink.py <port> <N> <out.json>"""
from __future__ import annotations
import json, socket, sys, time
from pathlib import Path

PORT, N = int(sys.argv[1]), int(sys.argv[2])
out = Path(sys.argv[3])
T_BINS, BIN_S = 48, 0.05

def recvn(c, n):
    buf = b""
    while len(buf) < n:
        chunk = c.recv(n - len(buf))
        if not chunk: break
        buf += chunk
    return buf

def series_from(events, t0):
    s = [0.0] * T_BINS
    for (t, nb) in events:
        b = int((t - t0) / BIN_S)
        if 0 <= b < T_BINS: s[b] += nb
    return s

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", PORT)); srv.listen(8)
print(f"sink listening on {PORT}, expecting {N}", flush=True)
egress = {}
for _ in range(N):
    c, _ = srv.accept()
    cid = int.from_bytes(recvn(c, 4), "big")
    t0 = time.time(); events = []
    while True:
        chunk = c.recv(65536)
        if not chunk: break
        events.append((time.time(), len(chunk)))
    egress[cid] = series_from(events, t0)
    c.close()
out.write_text(json.dumps(egress))
print(f"wrote {len(egress)} egress series", flush=True)
