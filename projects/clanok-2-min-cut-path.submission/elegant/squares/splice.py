"""Build a trial copy of main.tex with the proposed Sections 3 and 4, in a scratch folder given as argv[1].

Usage: splice.py TARGET [--only4 | --only3]
Reads projects/clanok-2-min-cut-path/main.tex, never writes to it. Lines are found by labels, not by numbers.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'clanok-2-min-cut-path'))
target = sys.argv[1]
only4 = '--only4' in sys.argv
only3 = '--only3' in sys.argv
os.makedirs(target, exist_ok=True)
for f in os.listdir(ROOT):
    if os.path.isfile(os.path.join(ROOT, f)) and f != 'main.tex':
        shutil.copy(os.path.join(ROOT, f), target)

src = open(os.path.join(ROOT, 'main.tex'), encoding='utf8').read()
sec4 = open(os.path.join(HERE, 'sec4-new.tex'), encoding='utf8').read()
sec3 = open(os.path.join(HERE, 'sec3-new.tex'), encoding='utf8').read()


def between(s, a, b):
    i = s.index(a)
    j = s.index(b, i)
    return i, j


# Section 3
if not only4:
    i, j = between(src, '\\section{NP-Completeness on Graphs of Diameter Three}', '\\section{Pairs with Cut-Value at Most Two}')
    src = src[:i] + sec3 + src[j:]

if only3:
    open(os.path.join(target, 'main.tex'), 'w', encoding='utf8').write(src)
    raise SystemExit

# Section 4
i, j = between(src, '\\section{Pairs with Cut-Value at Most Two}', '\\section{From Pairs at Distance Two to a Zigzag Problem}')
src = src[:i] + sec4 + src[j:]

# minimum sides and lem:zz-sides move from Section 5 to Section 2
a = 'A \\emph{minimum side} is a set $A \\subseteq V$ with $u \\in A$, $v \\notin A$ and $|\\delta(A)| = c$.\n'
b = 'By \\cref{lem:minimum-cuts}, the minimum $u$--$v$ cuts are exactly the sets $\\delta(A)$ for the minimum sides $A$.\n'
assert a in src and b in src
src = src.replace(a, '').replace(b, '')
i = src.index('\\begin{lemma}[Minimum sides]')
j = src.index('\\end{proof}', i) + len('\\end{proof}\n')
lem = src[i:j]
src = src[:i] + src[j:].lstrip('\n')
lem = lem.replace('$|\\delta(A)| = c$', '$|\\delta(A)| = c$')
new2 = ('Let $c = c(u, v)$.\n'
        'A \\emph{minimum side} is a set $A \\subseteq V$ with $u \\in A$, $v \\notin A$ and $|\\delta(A)| = c$.\n'
        'By \\cref{lem:minimum-cuts}, the minimum $u$--$v$ cuts are exactly the sets $\\delta(A)$ for the minimum sides $A$.\n\n'
        + lem + '\n')
key = 'The inequality $|\\delta(A \\cap B)| + |\\delta(A \\cup B)| \\leq |\\delta(A)| + |\\delta(B)|$ is the submodularity of the cut function.\n\n'
assert key in src
src = src.replace(key, new2)

# references from other sections
repl = [
    ('The minimum $u$--$v$ cuts divide the graph into a chain of subgraphs, the squares (\\cref{thm:structure}).\n',
     'The strong components of the residual digraph of a flow of value two form a chain of subgraphs, the layers and among them the squares (\\cref{lem:layers}).\n'),
    ('some square contains a path from an entering to a leaving terminal that lies on a shortest $u$--$v$ path and separates the other two terminals',
     'some square contains a path from an entering to a leaving edge that lies on a shortest $u$--$v$ path and separates the ends of the other two edges'),
    ('For $c(u, v) = 2$, consecutive squares are joined by two general paths, and a $u$--$v$ path $R$ follows exactly one of them.\n',
     'For $c(u, v) = 2$, the minimum $u$--$v$ cuts that come from the layers have two edges each, and a $u$--$v$ path $R$ contains exactly one of them.\n'),
    ('the part of $R$ in the square separates the two terminals at the edges of the square that $R$ does not use',
     'the part of $R$ in the square separates the ends of the two edges of the square that $R$ does not use'),
    ('For a pair with $c(u, v) = 2$, the square decomposition of \\cref{sec:structure} is an explicit form of these representations.\n',
     'For a pair with $c(u, v) = 2$, the layers of \\cref{sec:layers} are the vertices of this acyclic digraph.\n'),
    ('We prove its properties directly, because \\cref{sec:separating,sec:algorithm} use the terminals of the squares and distances inside the squares, which a contraction does not keep.\n',
     'We keep the graphs inside the layers, because \\cref{sec:separating,sec:algorithm} use the ends of the edges between layers and distances inside the layers, which a contraction does not keep.\n'),
    ('Here the decomposition is defined by the union of all minimum $u$--$v$ cuts, and every statement on it has a complete proof.\n',
     'Here the squares are obtained from the strong components of a residual digraph, and every statement on them has a complete proof.\n'),
    ('the linear running time that includes the computation of the decomposition',
     'the linear running time that includes the computation of the squares'),
    ('\\Cref{sec:structure,sec:separating,sec:algorithm} treat the first kind.',
     '\\Cref{sec:layers,sec:separating,sec:algorithm} treat the first kind.'),
]
for x, y in repl:
    assert x in src, x
    src = src.replace(x, y)

open(os.path.join(target, 'main.tex'), 'w', encoding='utf8').write(src)
print('written', os.path.join(target, 'main.tex'))
