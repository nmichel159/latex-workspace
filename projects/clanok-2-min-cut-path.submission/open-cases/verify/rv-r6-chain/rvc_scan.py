"""Scan runs/*.jsonl (partial or complete) for records with errors; print per-file counts.
usage: python rvc_scan.py [pattern]"""
import glob
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
pat = sys.argv[1] if len(sys.argv) > 1 else "*.jsonl"
for f in sorted(glob.glob(os.path.join(HERE, "runs", pat))):
    st = Counter()
    errs = []
    with open(f, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("skip"):
                st["skip"] += 1
                continue
            st["rec"] += 1
            if r.get("answer") is True:
                st["yes"] += 1
            if r.get("answer") is False:
                st["no"] += 1
            if r.get("err"):
                errs.append((r.get("name"), r["err"][:3]))
            inf = r.get("info") or {}
            if inf.get("levels", 0) >= 2:
                st["levels>=2"] += 1
            st["paths"] += r.get("paths", 0) or 0
            if r.get("cert_graph"):
                st["cert_graph"] += 1
            if r.get("zz_only"):
                st["zz_only"] += 1
            st["maxbad"] = max(st["maxbad"], inf.get("bad", 0))
            st["maxA"] = max(st["maxA"], inf.get("Amax", 0))
    print(os.path.basename(f), dict(st), "errors:", len(errs))
    for e in errs[:10]:
        print("   ", e)
