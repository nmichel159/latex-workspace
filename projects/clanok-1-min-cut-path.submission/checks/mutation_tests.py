"""Mutation tests for check_reduction.py: each broken construction must be caught by a check.

Run:  python mutation_tests.py
"""

import sys

import check_reduction as cr
from reduction import Reduction

FORMULA = [(1, 2, 3), (-1, 2, -3)]


class WrongSign(Reduction):
    """A 3-synchronization thread crosses its literal link with the wrong sign."""

    def _thread(self, kind, owner, spec):
        if kind == "sync3" and spec[0][1] == "+":
            spec = [spec[0], (spec[1][0], "+"), spec[2]]
        super()._thread(kind, owner, spec)


class PositiveClauses(Reduction):
    """Every clause thread crosses its literal links positively."""

    def _thread(self, kind, owner, spec):
        if kind == "clause":
            spec = [(idx, "+") for idx, _ in spec]
        super()._thread(kind, owner, spec)


class Reordered(Reduction):
    """3-synchronization threads visit I_i, T_i, L_{j,k} in this order (same crossing edges)."""

    def _thread(self, kind, owner, spec):
        if kind == "sync3":
            spec = [spec[0], spec[2], spec[1]]
        super()._thread(kind, owner, spec)


class NoSync2(Reduction):
    """No 2-synchronization threads."""

    def _thread(self, kind, owner, spec):
        if kind != "sync2":
            super()._thread(kind, owner, spec)


def separation(R):
    for signs in cr.check_hitting(R):
        cr.require(R.separates(R.chain_path(signs)), "the chain path of a satisfying assignment is not separating")


TESTS = [
    ("connecting paths of one edge (no second step of Calibrate): Lemma 3.5",
     lambda: cr.check_shortest_paths(Reduction(3, FORMULA, seed=1, lengthen=False))),
    ("wrong sign in a 3-synchronization thread: Lemma 3.6",
     lambda: cr.check_hitting(WrongSign(3, FORMULA, seed=1))),
    ("clause threads all positive: Lemma 3.7",
     lambda: cr.check_hitting(PositiveClauses(3, FORMULA, seed=1))),
    ("3-synchronization threads through I, T, L: Lemma 3.8",
     lambda: separation(Reordered(3, FORMULA, seed=1))),
    ("no 2-synchronization threads: Lemma 3.6",
     lambda: cr.check_hitting(NoSync2(3, FORMULA, seed=1))),
]

if __name__ == "__main__":
    missed = 0
    for name, test in TESTS:
        try:
            test()
            print("NOT DETECTED  %s" % name)
            missed += 1
        except cr.Failure as failure:
            print("detected      %s  (%s)" % (name, failure))
    sys.exit(1 if missed else 0)
