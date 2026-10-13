#!/bin/sh
# background adversarial hunts (agent DC-algorithm)
cd "$(dirname "$0")/.."
for s in 11 12 13 14; do
  python hunt_pc.py sw $s 6000 runs/hunt-sw-$s.jsonl > runs/hunt-sw-$s.log 2>&1 &
done
for s in 21 22 23 24; do
  python hunt_pc.py zz $s 6000 runs/hunt-zz-$s.jsonl > runs/hunt-zz-$s.log 2>&1 &
done
wait
