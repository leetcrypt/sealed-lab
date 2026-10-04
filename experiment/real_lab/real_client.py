"""Real capture client (ingress observer), multi-arm. Opens N connections to the sink and
replays a distinct random burst pattern per connection, logging the ingress byte-count series
+ real connect latency. Own-fleet only. Stdlib (minimal SOCKS5 for Tor).

usage:
  real_client.py direct <host> <port>                    <N> <SEED> <out.json>
  real_client.py socks  <proxyH> <proxyP> <onion> <port> <N> <SEED> <out.json>
(SOR uses `direct` to a local ssh -L forwarded port.)"""
from __future__ import annotations
import json, random, socket, sys, time
from pathlib import Path

T_BINS, BIN_S = 48, 0.05
mode = sys.argv[1]
if mode == "direct":
    HOST, PORT = sys.argv[2], int(sys.argv[3]); rest = sys.argv[4:]
elif mode == "socks":
    PH, PP, DH, DP = sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5]); rest = sys.argv[6:]
else:
    sys.exit("bad mode")
N, SEED, OUT = int(rest[0]), int(rest[1]), Path(rest[2])

def make_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(90)
    if mode == "direct":
        s.connect((HOST, PORT))
    else:
        s.connect((PH, PP))
        s.sendall(b"\x05\x01\x00")
        if s.recv(2) != b"\x05\x00": raise RuntimeError("socks handshake")
        req = b"\x05\x01\x00\x03" + bytes([len(DH)]) + DH.encode() + DP.to_bytes(2, "big")
        s.sendall(req)
        resp = s.recv(10)
        if len(resp) < 2 or resp[1] != 0x00: raise RuntimeError(f"socks connect rep={resp[1] if len(resp)>1 else '?'}")
    return s

def pattern(r):
    b = []
    for _ in range(r.randint(3, 7)):
        start = r.randint(0, T_BINS - 1); size = int(r.uniform(1, 5) * 400)
        for k in range(r.randint(1, 4)):
            if start + k < T_BINS: b.append((start + k, int(size * r.uniform(0.5, 1.5))))
    return sorted(b)

def series(events, t0):
    s = [0.0] * T_BINS
    for (t, nb) in events:
        bb = int((t - t0) / BIN_S)
        if 0 <= bb < T_BINS: s[bb] += nb
    return s

ingress, lat, good = {}, [], []
for cid in range(N):
    bursts = pattern(random.Random(SEED * 1000 + cid))
    t_c = time.time()
    try:
        s = make_conn()
    except Exception as e:
        print(f"conn {cid} failed: {e}", flush=True); continue
    lat.append(time.time() - t_c)
    s.sendall(cid.to_bytes(4, "big"))
    t0 = time.time(); ev = []; tot = 0
    for (b, nb) in bursts:
        tgt = t0 + b * BIN_S; now = time.time()
        if tgt > now: time.sleep(tgt - now)
        s.sendall(b"x" * nb); ev.append((time.time(), nb)); tot += nb
    s.close()
    good.append(tot / max(1e-6, time.time() - t0)); ingress[cid] = series(ev, t0)

OUT.write_text(json.dumps({"ingress": ingress, "latency_s": lat, "goodput_Bps": good}))
m = lambda xs: sorted(xs)[len(xs)//2] if xs else 0
print(f"sent {len(ingress)}/{N}; median connect latency {m(lat)*1000:.0f} ms", flush=True)
