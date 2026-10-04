# Phone SSH-relay reliability (Termux) — why it's flaky and how to fix it

The phone relays dropped SSH port-forwards within seconds. For tonight's study we routed SOR
through **grok-bot (cloud VM)** instead, which is stable and also removes the mobile-buffering
confound. These fixes make the phones usable as relays for future runs.

## Root causes
1. **Android Doze / battery optimization** kills Termux + its sshd when the screen is off or
   Termux is backgrounded — the #1 cause.
2. **Mobile/Wi-Fi NAT timeouts** drop idle forwarded connections.
3. **Termux sshd defaults** have no keepalive, so half-dead forwards linger then fail.
4. Slow phone CPU makes forward setup itself slow (ProxyJump through two phones = very slow).

## Fixes TO RUN ON THE PHONE (Termux)
```bash
# 1) CPU wakelock — THE big one. Keeps Termux alive under Doze. Run before any relay use:
termux-wake-lock
# (release later with: termux-wake-unlock)

# 2) sshd keepalive + forwarding — append to the Termux sshd config, then restart sshd:
cat >> $PREFIX/etc/ssh/sshd_config <<'CFG'
ClientAliveInterval 20
ClientAliveCountMax 6
TCPKeepAlive yes
AllowTcpForwarding yes
GatewayPorts yes
CFG
pkill sshd; sshd        # restart

# 3) persist across reboots/app-swipes: install the Termux:Boot app (F-Droid), then:
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-sshd.sh <<'B'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
sshd
B
chmod +x ~/.termux/boot/start-sshd.sh
```

## Fixes IN ANDROID SETTINGS (per phone)
- **Settings → Apps → Termux → Battery → Unrestricted** (and same for Termux:Boot).
- **Keep screen on while plugged in** (Developer options), and keep the phone plugged in during a run.
- **Wi-Fi → Advanced → keep Wi-Fi on during sleep: Always** (disable Wi-Fi sleep).
- Prefer **Wi-Fi over cellular** for sustained forwarding.

## Client-side (already applied on the laptop/trillsec)
`-o ServerAliveInterval=20 -o ExitOnForwardFailure=yes`; prefer ONE reliable relay over a
2-phone ProxyJump; reuse connections with `ControlMaster auto -o ControlPersist=60`.

## Bottom line
For the study we use **grok-bot** (stable). Phones become viable relays after
`termux-wake-lock` + Unrestricted battery + the sshd keepalive above.
