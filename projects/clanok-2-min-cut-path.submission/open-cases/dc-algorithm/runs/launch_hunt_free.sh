#!/bin/sh
# control hunts without P2 (agent DC-algorithm)
cd "$(dirname "$0")/.."
for s in 31 32; do
  python hunt_pc.py swfree $s 6000 runs/hunt-swfree-$s.jsonl > runs/hunt-swfree-$s.log 2>&1 &
done
for s in 41 42; do
  python hunt_pc.py zzfree $s 6000 runs/hunt-zzfree-$s.jsonl > runs/hunt-zzfree-$s.log 2>&1 &
done
wait
