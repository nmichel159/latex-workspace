"""HYB (plain, refined) on Y^d_k, Y'^d_k for one k and given parameter sets (Proposition D (iv)).
usage: python hyb_runs.py K kd,ks,s,B [kd,ks,s,B ...] [refined]
"""
import json
import sys
import time

from fam import yfam
from glib import hyb


def main():
    k = int(sys.argv[1])
    refined = sys.argv[-1] == "refined"
    plist = [tuple(int(x) for x in a.split(",")) for a in sys.argv[2:] if a != "refined"]
    for contact in (False, True):
        for dvar in ("plain", "back"):
            G, info = yfam(k, contact, dvar)
            name = ("Y'" if contact else "Y") + "^d" + ("(back)" if dvar == "back" else "") + "_%d" % k
            for p in plist:
                t0 = time.time()
                r = hyb(G, *p, refined=refined)
                pred = "reject" if (p[0] + p[1] + p[2] < k and p[3] < k) else "-"
                print(json.dumps({"inst": name, "params": p, "refined": refined, "accepts": r,
                                  "Prop D (iv) predicts": pred, "sec": round(time.time() - t0, 1)}), flush=True)


if __name__ == "__main__":
    main()
