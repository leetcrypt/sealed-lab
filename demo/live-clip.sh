#!/usr/bin/env bash
set -uo pipefail
cd ~/coding/hackathon
C_CYAN=$'\033[38;5;39m'; C_GRN=$'\033[38;5;42m'; C_RED=$'\033[38;5;203m'; C_MUT=$'\033[38;5;245m'; C_0=$'\033[0m'
prompt(){ printf "${C_GRN}sealed-lab${C_0} ${C_MUT}\$${C_0} %s\n" "$1"; sleep 0.6; }
clear
case "${1:-pass}" in
  pass)
    prompt "python3 method/tools/design_check.py config/designs/anon-baserate.json"
    python3 method/tools/design_check.py config/designs/anon-baserate.json 2>&1 | tail -15 ;;
  deny)
    prompt "python3 method/tools/instrument_check.py defects/inverted-instruments.json --gates O"
    python3 method/tools/instrument_check.py experiment/defects/inverted-instruments.json --gates O 2>&1 | tail -13
    printf "${C_RED}▌ policy → DENY · experiment run BLOCKED before any data${C_0}\n" ;;
  retract)
    prompt "python3 experiment/real_lab/verify_result.py"
    python3 experiment/real_lab/verify_result.py 2>&1 | tail -13 ;;
esac
sleep 3.5
