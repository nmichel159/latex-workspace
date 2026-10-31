"""Referee rv-r7-desc: totals quoted in the report.  Run from runs/."""
import ast
import glob
import re

s = open("saved.txt", encoding="utf-8", errors="replace").read()
print("saved paths", sum(int(x) for x in re.findall(r"\n\s+paths (\d+)", s)))
print("saved files", sum(int(x) for x in re.findall(r"\n\s+files (\d+)", s)))
for f in ("random-11.txt", "random-12.txt"):
    t = open(f, encoding="utf-8", errors="replace").read()
    print(f, re.findall(r"(?m)^(yes|no|paths) (\d+)", t))
acc = rej = 0
atk_a = atk_r = 0
for f in [x for x in glob.glob("planted-*.txt") if "summary" not in x]:
    for ln in open(f, encoding="utf-8", errors="replace"):
        if ln.startswith("accepted moves"):
            d = ast.literal_eval(ln.split(" moves ", 1)[1])
            acc += sum(d.values())
            atk_a += d.get("attack", 0)
        elif ln.startswith("rejected moves"):
            d = ast.literal_eval(ln.split(" moves ", 1)[1])
            rej += sum(d.values())
            atk_r += d.get("attack", 0)
print("accepted", acc, "rejected", rej, "attack accepted", atk_a, "attack rejected", atk_r)
tot = {}
for f in [x for x in glob.glob("planted-*.txt") if "summary" not in x]:
    for ln in open(f, encoding="utf-8", errors="replace"):
        m = re.match(r"(.*) (\d+)$", ln.rstrip("\n"))
        if m and not ln.startswith(("max", "C_1 max", "R_1 max", "base ")):
            tot[m.group(1)] = tot.get(m.group(1), 0) + int(m.group(2))
for k in sorted(tot):
    print(k, tot[k])
print("empty ce:", len(glob.glob("../ce/*")))
print("all logs clean:", all("FAILURES: none" in open(f, encoding="utf-8", errors="replace").read() for f in glob.glob("*.txt")
                             if f not in ("planted-summary.txt", "rand-test.txt", "mut-5.txt", "cross-check.txt", "fam.txt") and not f.startswith("t-")))
