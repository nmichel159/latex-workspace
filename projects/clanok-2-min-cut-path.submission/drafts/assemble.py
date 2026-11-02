#!/usr/bin/env python3
"""History, do not run: its paths are those of the former project clanok-3, and main.tex is the source.

Assemble projects/clanok-3-min-cut-path/main.tex from the drafts and prune references.bib.

Run once from any directory. The preamble comes from article 2's main.tex, which is the template's sample filled in.
After the first assembly, main.tex is the source; rerun only while the drafts are still the source.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUB = ROOT / "projects" / "clanok-3-min-cut-path.submission"
DRAFTS = SUB / "drafts"
PROJECT = ROOT / "projects" / "clanok-3-min-cut-path"
ARTICLE2 = ROOT / "projects" / "clanok-2-min-cut-path" / "main.tex"
CANON = ROOT / "knowledge" / "bibliography" / "references.bib"

TITLE = "Min Cut-Path: NP-Complete on Diameter Three, Polynomial for Distance or Cut-Value Two"

ABSTRACT = r"""A cut-path between two vertices $u$ and $v$ of a graph is a set of edges that contains both a $u$--$v$ path and a cut separating $u$ from $v$.
The \MinCutPath{} problem asks for a cut-path with the fewest edges.
Let $d(u,v)$ be the distance between $u$ and $v$, and let the cut-value $c(u,v)$ be the size of a minimum cut separating them.
We prove that \MinCutPath{} is NP-complete on graphs of diameter three, already for pairs with $d(u,v) = 2$.
We then prove that it is solvable in polynomial time on the graphs in which every two vertices are at distance at most two or have cut-value at most two, a class that contains the graphs of diameter two and the cactus graphs.
For a pair with cut-value two, the minimum cuts divide the graph into a chain of subgraphs, and a minimum cut-path has $d(u,v)$ edges if and only if one of these subgraphs contains a path that lies on a shortest $u$--$v$ path and separates two prescribed vertices of the subgraph, which gives a linear-time algorithm in the class.
The remaining pairs have $d(u,v) = 2$ and $c(u,v) \geq 3$, and there a minimum cut-path has $c(u,v)$ edges if and only if some minimum cut contains a $u$--$v$ path.
The minimum cuts are the down-sets of a preorder, and the condition on distances gives every two incomparable elements a common neighbor below both or above both.
We show that a bounded number of elements determines a down-set whose cut contains a given shortest solution, and enumeration of these descriptions decides the question."""

KEYWORDS = "Separating shortest path, Edge connectivity, Minimum cuts, Graph diameter, NP-completeness"

MACROS = r"""\newcommand{\PathInMinCut}{\textsc{Path in Min Cut}}%
\newcommand{\dn}{\mathord{\downarrow}}%
\newcommand{\upp}{\mathord{\uparrow}}%
\newcommand{\LMN}{\mathrm{LMN}}%
\newcommand{\UMN}{\mathrm{UMN}}%
\newcommand{\pos}{\mathrm{pos}}%
\newcommand{\nodeof}{\mathrm{node}}%
\newcommand{\pk}{\mathrm{pk}}%
\newcommand{\NE}{\mathrm{NE}}%
\newcommand{\NF}{\mathrm{NF}}%
\newcommand{\Pos}{\mathrm{Pos}}%
\newcommand{\win}{\mathrm{win}}%
\newcommand{\FR}{\mathrm{FR}}%
\newcommand{\ER}{\mathrm{ER}}%
\newcommand{\EP}{\mathrm{EP}}%
"""


def body(name: str) -> str:
    text = (DRAFTS / name).read_text(encoding="utf-8")
    lines = text.splitlines()
    if lines and lines[0].startswith("% MACROS:"):
        i = 1
        while i < len(lines) and lines[i].startswith("%"):
            i += 1
        lines = lines[i:]
    return "\n".join(lines).strip() + "\n"


def edit_drafts() -> dict:
    parts = {}
    parts["prelim"] = body("02-prelim.tex").replace(
        "% TODO(check): add a pointer to the sections that treat the second kind (pairs at distance two).",
        "\\Cref{sec:zz-zigzag,sec:pa-polynomial} treat the second kind.",
    )
    hard = body("03-diameter-three.tex")
    hard = re.sub(r"^% TODO\(check\):.*\n", "", hard, flags=re.M)
    hard = hard.replace(
        "For hardness, we reduce 3-SAT to \\PathInMinCut{}.",
        "For hardness, we reduce 3-SAT, which is NP-complete~\\cite{Cook1971Complexity,Karp1972Reducibility}, to \\PathInMinCut{}.",
    )
    parts["hard"] = hard
    parts["intro"] = body("01-intro.tex")
    parts["squares"] = body("04-squares.tex")
    parts["zigzag"] = body("05-zigzag.tex")
    parts["poly"] = body("06-polynomial.tex")
    parts["concl"] = body("07-conclusion.tex")
    return parts


def build_main(parts: dict) -> str:
    lines = ARTICLE2.read_text(encoding="utf-8").splitlines()
    doc = next(i for i, l in enumerate(lines) if l.startswith("\\begin{document}"))
    pre = "\n".join(lines[:doc])
    pre = pre.replace(
        "pdftitle={Min Cut-Path on Graphs with Distance or Cut-Value at Most Two}",
        "pdftitle={" + TITLE + "}",
    )
    anchor = "\\newcommand{\\SSP}{\\textsc{Separating Shortest Path}}%\n"
    assert anchor in pre
    pre = pre.replace(anchor, anchor + MACROS)
    a2 = "\n".join(lines[doc:])
    # Front matter of the sample, as article 2 fills it.
    m = re.search(r"^\\author\*.*?(?=%%==================================%%\n%% Sample for unstructured)", a2, flags=re.S | re.M)
    assert m
    author = m.group(0)
    sample_struct = re.search(r"%%================================%%\n%% Sample for structured abstract.*?(?=\\keywords)", a2, flags=re.S)
    assert sample_struct
    back = a2[a2.index("\\backmatter"):]
    out = [pre, "\\begin{document}", "", "\\title{" + TITLE + "}", "", author.rstrip(), ""]
    out += ["%%==================================%%", "%% Sample for unstructured abstract %%", "%%==================================%%", ""]
    out += ["\\abstract{" + ABSTRACT + "}", "", sample_struct.group(0).rstrip(), ""]
    out += ["\\keywords{" + KEYWORDS + "}", "", "%%\\pacs[JEL Classification]{D8, H51}", "", "%%\\pacs[MSC Classification]{35A01, 65L10, 65L12, 65L20, 65L70}", "", "\\maketitle", ""]
    for key in ("intro", "prelim", "hard", "squares", "zigzag", "poly", "concl"):
        out += [parts[key].rstrip(), ""]
    out.append(back.replace("on which this paper is based", "on which part of this paper is based"))
    return "\n".join(out) + "\n"


def entries(text: str) -> dict:
    res = {}
    for m in re.finditer(r"@\w+\{([^,\s]+),", text):
        i = m.end()
        depth = 1
        while depth and i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        res[m.group(1)] = text[m.start():i]
    return res


def prune_bib(main: str) -> list:
    cited = set()
    for m in re.finditer(r"\\cite\w*(?:\[[^\]]*\])*\{([^}]*)\}", main):
        cited |= {k.strip() for k in m.group(1).split(",")}
    project = entries((PROJECT / "references.bib").read_text(encoding="utf-8"))
    canon = entries(CANON.read_text(encoding="utf-8"))
    missing = []
    chosen = []
    for key in sorted(cited):
        if key in project:
            chosen.append(project[key])
        elif key in canon:
            chosen.append(canon[key])
        else:
            missing.append(key)
    (PROJECT / "references.bib").write_text("\n\n".join(chosen) + "\n", encoding="utf-8")
    return missing


def main_() -> None:
    parts = edit_drafts()
    main = build_main(parts)
    (PROJECT / "main.tex").write_text(main, encoding="utf-8")
    missing = prune_bib(main)
    print("main.tex lines:", main.count("\n"))
    print("missing citation keys:", missing)
    todo = [l for l in main.splitlines() if "TODO" in l]
    print("TODO lines:", len(todo))
    for l in todo:
        print(" ", l[:160])
    labels = set(re.findall(r"\\label\{([^}]+)\}", main))
    refs = set()
    for m in re.finditer(r"\\[cC]ref\{([^}]+)\}", main):
        refs |= {k.strip() for k in m.group(1).split(",")}
    print("undefined refs:", sorted(refs - labels))
    dup = [x for x in labels if len(re.findall(r"\\label\{" + re.escape(x) + r"\}", main)) > 1]
    print("duplicate labels:", dup)
    figs = set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", main))
    print("figures:", sorted(figs))


if __name__ == "__main__":
    main_()
