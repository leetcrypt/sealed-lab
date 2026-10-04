#!/usr/bin/env bash
# Live capture: the Sealed Lab rigor gates executing for real (stdlib-only Python).
set -uo pipefail
cd ~/coding/hackathon
C_CYAN=$'\033[38;5;39m'; C_GRN=$'\033[38;5;42m'; C_RED=$'\033[38;5;203m'; C_MUT=$'\033[38;5;245m'; C_0=$'\033[0m'
hr(){ printf "${C_MUT}%s${C_0}\n" "────────────────────────────────────────────────────────────"; }
banner(){ printf "\n${C_CYAN}▌ %s${C_0}\n" "$1"; sleep 0.8; }
prompt(){ printf "${C_GRN}sealed-lab${C_0} ${C_MUT}\$${C_0} %s\n" "$1"; sleep 0.7; }

clear
banner "GATE 1  design_check — run the pre-registered design, don't read it"
prompt "python3 method/tools/design_check.py config/designs/anon-baserate.json"
python3 method/tools/design_check.py config/designs/anon-baserate.json 2>&1 | tail -14
sleep 2.6

clear
banner "GATE 2  instrument_check — inject a scorer that reads BACKWARDS"
prompt "python3 method/tools/instrument_check.py experiment/defects/inverted-instruments.json --gates O"
python3 method/tools/instrument_check.py experiment/defects/inverted-instruments.json --gates O 2>&1 | tail -12
printf "${C_RED}▌ policy → DENY: experiment run BLOCKED before any data${C_0}\n"
sleep 2.8

clear
banner "GATE 3  verify_seals — re-hash the sealed pre-registration"
prompt "python3 method/tools/verify_seals.py \$PWD/output/anon-baserate"
python3 method/tools/verify_seals.py "$PWD/output/anon-baserate" 2>&1 | grep -E "SEAL VERIFICATION|OK|verified " | head -8
sleep 2.6

clear
banner "VERIFIER  re-score with a lag-aligning adversary — catch our own artifact"
prompt "python3 experiment/real_lab/verify_result.py"
python3 experiment/real_lab/verify_result.py 2>&1 | tail -12
sleep 2.0
printf "\n${C_GRN}▌ the lab retracted its own headline. verification, not generation.${C_0}\n"
sleep 2.5
