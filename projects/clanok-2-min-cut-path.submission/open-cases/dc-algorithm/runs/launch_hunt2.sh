#!/bin/sh
# second round of adversarial PC hunts (agent DC-algorithm), larger instances, 90 minutes each
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
T=5400
for s in 51 52 53; do timeout $T python hunt2.py zz $s 1000000 runs/hunt2-zz-$s.jsonl 12 17 > runs/hunt2-zz-$s.log 2>&1 & done
timeout $T python hunt2.py zz 54 1000000 runs/hunt2-zz-54.jsonl 16 21 > runs/hunt2-zz-54.log 2>&1 &
for s in 61 62; do timeout $T python hunt2.py sw $s 1000000 runs/hunt2-sw-$s.jsonl > runs/hunt2-sw-$s.log 2>&1 & done
for s in 71 72; do timeout $T python hunt2.py rigid $s 1000000 runs/hunt2-rigid-$s.jsonl > runs/hunt2-rigid-$s.log 2>&1 & done
timeout $T python hunt2.py zzfree 81 1000000 runs/hunt2-zzfree-81.jsonl 12 17 > runs/hunt2-zzfree-81.log 2>&1 &
timeout $T python hunt2.py swfree 91 1000000 runs/hunt2-swfree-91.jsonl > runs/hunt2-swfree-91.log 2>&1 &
wait
