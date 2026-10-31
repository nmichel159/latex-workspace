"""Proposition CF (iv) (r5-core §3.3): Z_k, Z^B_k are solved by CDESC with one centre and no flip.
usage: python test_cf_z.py KMAX"""
import json
import sys
from fam import zfam
from glib import cdesc, p2_violations, shortest_len, brute

for k in range(2, int(sys.argv[1]) + 1):
    for block in (False, True):
        for contact in (False, True):
            G, info = zfam(k, contact, block)
            rec = {"k": k, "block": block, "contact": contact, "m": G.m, "N": G.N, "p2_viol": len(p2_violations(G)),
                   "shortest": shortest_len(G)}
            if G.m <= 12:
                rec["nsol"] = len(brute(G))
            r0 = cdesc(G, 1, 0, want=True)
            rec["cdesc(1,0)"] = r0[0]
            if r0[0]:
                rec["kind_centre"] = (r0[1][0], len(r0[1][1]))
            print(json.dumps(rec), flush=True)
