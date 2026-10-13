"""cp(u,v) as an integer program (CBC through pulp); a third, independent computation of cp.

Variables: y_x (side; y_u = 1, y_v = 0), z_e >= |y_a - y_b| (covers the cut delta({y = 1})),
p_ab, p_ba (a unit u-v flow; its support contains a u-v path), s_e >= z_e, s_e >= p_ab, s_e >= p_ba.
Minimise sum s_e. A feasible solution gives an edge set {s = 1} containing a u-v cut and a u-v path; a cut-path S
gives a feasible solution of value |S| (path P in S, cut C in S, y = component of u in G - C). So the optimum is cp.
"""

import sys

# Keep pulp away from an installed Gurobi: with gurobipy blocked, pulp never opens a Gurobi environment (which writes
# gurobi.log into the working directory). Only CBC is used below.
if "gurobipy" not in sys.modules:
    sys.modules["gurobipy"] = None

import pulp  # noqa: E402


def cp_ilp(g, u, v, time_limit=None, upper=None):
    prob = pulp.LpProblem("cp", pulp.LpMinimize)
    y = {x: pulp.LpVariable("y%d" % x, cat="Binary") for x in range(g.n)}
    z, s, pf, pb = {}, {}, {}, {}
    for e, (a, b) in enumerate(g.edges):
        z[e] = pulp.LpVariable("z%d" % e, lowBound=0, upBound=1)
        s[e] = pulp.LpVariable("s%d" % e, cat="Binary")
        pf[e] = pulp.LpVariable("pf%d" % e, cat="Binary")
        pb[e] = pulp.LpVariable("pb%d" % e, cat="Binary")
    prob += pulp.lpSum(s.values())
    prob += y[u] == 1
    prob += y[v] == 0
    for e, (a, b) in enumerate(g.edges):
        prob += z[e] >= y[a] - y[b]
        prob += z[e] >= y[b] - y[a]
        prob += s[e] >= z[e]
        prob += s[e] >= pf[e]
        prob += s[e] >= pb[e]
    for x in range(g.n):
        out_ = pulp.lpSum(pf[e] for y_, e in g.adj[x] if g.edges[e][0] == x) + \
            pulp.lpSum(pb[e] for y_, e in g.adj[x] if g.edges[e][1] == x)
        in_ = pulp.lpSum(pb[e] for y_, e in g.adj[x] if g.edges[e][0] == x) + \
            pulp.lpSum(pf[e] for y_, e in g.adj[x] if g.edges[e][1] == x)
        rhs = 1 if x == u else (-1 if x == v else 0)
        prob += out_ - in_ == rhs
    if upper is not None:
        prob += pulp.lpSum(s.values()) <= upper
    solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=time_limit, threads=1)
    status = prob.solve(solver)
    st = pulp.LpStatus[status]
    if st != "Optimal":
        return None, st
    return int(round(pulp.value(prob.objective))), st
