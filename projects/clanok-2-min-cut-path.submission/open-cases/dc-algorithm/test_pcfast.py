"""Cross-check pcfast.pc_answer against zz.pc_numpy and the exact answer on random instances (with and without P2).
Usage: python test_pcfast.py SEED COUNT"""
import sys
import random
import time
sys.setrecursionlimit(100000)
import zz
import pcfast

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
st = {}
t_old = t_new = 0.0
for it in range(count):
    n = rng.randint(5, 14)
    p2 = rng.random() < 0.5
    z = zz.random_zz(rng, n, rng.choice([0.1, 0.2, 0.3]), rng.choice([0.1, 0.2, 0.3]), p2=p2)
    ex = zz.exact_dfs(z)[0]
    t = time.time()
    a = zz.pc_numpy(z)
    t_old += time.time() - t
    t = time.time()
    b = pcfast.pc_answer(z)
    t_new += time.time() - t
    key = (p2, ex, a, b)
    st[key] = st.get(key, 0) + 1
    if a != b:
        print("MISMATCH", it, n, z.R)
print("(P2, exact, pc_numpy, pcfast):", st)
print("time pc_numpy %.1fs pcfast %.1fs" % (t_old, t_new))
