# Figures of article 2

TikZ sources of the figures of `projects/clanok-2-min-cut-path/main.tex` (not sent). Each `<name>.tex` is a
standalone document (class `standalone`, text font Computer Modern, T1 encoding as in the article) that builds
`<name>.pdf`; the PDF lies directly in `projects/clanok-2-min-cut-path/`.

**AI declaration.** The drawings were written as TikZ code by an AI assistant from the figures of the master's
thesis and from the specification of the article (`SPEC.md`, Sections 4 and 5). The author must declare this at
submission (`knowledge/writing/submission.md`, §1.3).

## Figures

All figures are drawn at their final size: include them at natural size (the text block of `sn-jnl` is 131 mm
wide, the labels are 10 pt like the text, the captions 9 pt), never with `width=`.

| File | Shows | Proposed caption (one line) | Label | Size (mm) | Include |
|---|---|---|---|---|---|
| `graph-classes` | the class $\mathcal{DC}_2$ with the graphs of diameter at most two and the cactus graphs overlapping in $C_4$; the counterexamples (a), (b) lie outside both | `The class $\mathcal{DC}_2$ and the graphs (a) and (b) of \cref{fig:counterexamples}, for which $\mathrm{cp}=c+d-1$ fails.` | `fig:graph-classes` | 117.0 x 69.0 | `\includegraphics{graph-classes}` |
| `counterexamples` | the two six-vertex graphs of the research map, minimum cut-path $u$-$a$-$b$-$v$ in red | `Two graphs in $\mathcal{DC}_2$ with $\mathrm{cp}(u,v)=3$ and $c(u,v)+d(u,v)-1=4$; the red path is a minimum cut-path.` | `fig:counterexamples` | 96.8 x 61.6 | `\includegraphics{counterexamples}` |
| `square-decomposition` | schematic of $S_1,P_{1,1},P_{1,2},S_2,\dots,S_k$; $P_{1,1}$ is one edge of $F$, $P_{1,2}$ has two links | `The square decomposition of $(G,u,v)$: squares (boxes), links (ellipses), edges of $F$ (dashed arrows, tail to head).` | `fig:square-decomposition` | 118.5 x 33.0 | `\includegraphics{square-decomposition}` |
| `decomposition-example` | counterexample (a) with $F=\{ua,us,sb,ta,tv,vb\}$ oriented, squares $S_1=\{u\}$, $S_2=\{a,b\}$, $S_3=\{v\}$, links $\{s\}$, $\{t\}$ | `The decomposition of \cref{fig:counterexamples}(a): the squares $S_1,S_2,S_3$ and the links $\{s\}$ and $\{t\}$.` | `fig:decomposition-example` | 89.5 x 38.8 | `\includegraphics{decomposition-example}` |
| `square-terminals` | a square $S_i$ with terminals $x,\alpha,y,\beta$ and a path $x$-$w$-$y$ of a $u$-$v$ path $R$; (a) $\alpha,\beta$ separated in $S_i\setminus R$, (b) joined by one more edge | `A square $S_i$ and the path $x$-$w$-$y$ of a $u$-$v$ path: in (a) $\alpha$ and $\beta$ are separated, in (b) they are not.` | `fig:square-terminals` | 119.0 x 45.8 | `\includegraphics{square-terminals}` |
| `padding` | the gadget of Theorem on hardness (S12): $u'$ joined to $u$ by two paths of length two through $s_1,s_2$; the four new edges are edges of $F$ | `The graph $G$ with the new vertex $u'$ and the four new edges of $F(u',v)$.` | `fig:padding` | 84.3 x 29.0 | `\includegraphics{padding}` |
| `transformations` (optional) | Transformations A, B, C of the thesis (Figures 3.9-3.11): a pseudo-square with terminals $a,b,c,d$ and a cut $\{e_1,e_2\}$, before and after | `Transformations A, B, C of a pseudo-square along a cut $\{e_1,e_2\}$ with two, one and no edge inside it.` | `fig:transformations` | 112.3 x 101.9 | `\includegraphics{transformations}` |
| `worked-example` | the graph $G_1$ (vertices $u,v,1,\dots,8$) and its square decomposition: $F$ = all edges except $12,13,23,67$ oriented tail to head, squares $S_1=\{u\}$, $S_2=\{1,2,3\}$, $S_3=\{6,7\}$, $S_4=\{v\}$, links $\{4\}$, $\{5\}$, $\{8\}$; no path highlighted | `The graph $G_1$ of \cref{ex:worked-example} and its square decomposition.` (the example number comes from `\cref`; use the real label of the example) | `fig:worked-example` | 116.5 x 37.4 | `\includegraphics{worked-example}` |
| `hardness-construction` | the 25-vertex graph of the reduction from satisfiability for $\varphi=(x_1\vee\neg x_2)\wedge x_2$: cliques $K^u$, $K^v$ (clique edges not drawn), rungs $u_iv_i$, occurrence vertices $o_{1,1},o_{1,2},o_{2,1}$ (ringed) with their edges to the anchors (thin gray, six edges), synchronization edge $o_{1,2}o_{2,1}$ (dotted), red path $u_0,v_0,o_{1,1},v_1,o_{2,1},v_2$ in the minimum cut of $x_1=x_2=\mathrm{true}$, dashed curve = side $A_\tau$ | `The graph of the reduction for $\varphi=(x_1\vee\neg x_2)\wedge x_2$; the red path lies in the minimum cut of the assignment $x_1=x_2=\text{true}$.` | `fig:hardness-construction` | 115.9 x 56.5 | `\includegraphics{hardness-construction}` |

`transformations` is needed only if the article keeps the transformation algorithm of the thesis; the plan in
`SPEC.md` computes $F$ and the pieces directly (S11) and does not use it.

## Conventions of all drawings

- Vertices are small black discs; terminals and the vertices $u$, $v$ are slightly larger.
- Edges of $F$ are dashed blue arrows (tail to head); edges of $G$ outside $F$ are thin black; the path of a
  cut-path (or the part of the $u$-$v$ path $R$ inside a square) is thick red.
- Pieces are light gray: squares are rounded boxes labelled $S_i$ (also in `transformations`, where the
  pseudo-square is the box), links are small darker ellipses; darker gray blobs inside a box are parts of it.
- Colors are the blue (31,102,178) and red (200,40,40) of the figures of article 1 and differ in gray scale by
  dashing and thickness as well: dashed thin (edges of $F$), dashed thick (cut edges in `transformations`),
  solid thin (other edges), solid thick (red path).
- No titles and no captions inside the figures; panel labels (a), (b), (c) lie under the panels.

## Rebuild

From PowerShell, in the workspace root (never run `pdflatex` without `--miktex-disable-installer`):

```powershell
Set-Location tmp\clanok-2-figures
foreach ($n in 'graph-classes','counterexamples','square-decomposition','decomposition-example','square-terminals','padding','transformations','worked-example','hardness-construction') {
  Copy-Item "..\..\projects\clanok-2-min-cut-path.submission\figures\$n.tex" .
  pdflatex -interaction=nonstopmode -halt-on-error --miktex-disable-installer "$n.tex"
  Copy-Item "$n.pdf" ..\..\projects\clanok-2-min-cut-path\ -Force
}
```

TikZ libraries used: `arrows.meta`, `shapes.geometric` (both in the MiKTeX installation; nothing was installed).
Every source sets `\pdfinfoomitdate`, `\pdftrailerid` and `\pdfsuppressptexinfo` as the figures of article 1 do,
so the PDFs carry no date, no ID and no TeX banner.

## Checks (2026-10-12)

- `pdffonts`: every font in every PDF is Type 1 and embedded (CMMI10, CMMI7, CMR10, CMR7, CMSY10, CMSY7 and
  SFRM1000 of cm-super for T1 text); no Type 3 font.
- `pdfinfo`: Creator `TeX`, Producer `MiKTeX pdfTeX-1.40.28`, no title, author, dates or XMP; a byte scan finds no
  user name, path, tool name or `.tex` string.
- Every figure was rendered at 150 dpi and inspected: no overlapping labels, no label on an edge, nothing clipped.

## Differences from the brief and from the thesis

- Vertices are black discs (brief), not the white-ringed vertices of article 1; fonts are Computer Modern, not STIX.
- `graph-classes`: the formula $\mathrm{cp}=c+d-1$ stands once in each inner class (the left and the right part);
  (a) and (b) are plain points, the failure of the formula is stated in the caption only.
- `square-decomposition`: the squares show only their terminals (inside the box next to the border); the chain
  between $S_2$ and $S_k$ is indicated by two dashed stubs on each side and $\cdots$. The first square shows
  $u=a_1=b_1$, the last one $v=c_k=d_k$.
- `square-terminals`: the thesis has no such figure. The layout follows from the criterion S7, not from a guess:
  if $x$ and $\alpha$ lay in one part and $y$ and $\beta$ in the other, the two red edges would be a minimum
  $u$-$v$ cut inside a piece, which is impossible. Therefore part A holds $\alpha$, $x$ and $y$, part B holds
  $w$ and $\beta$, and both red edges join A to B (the path dips into B). In (b) the extra edge is $\alpha\beta$.
- `transformations`: the thesis draws each transformation as before and after on its own page; here the three are
  stacked (before on the left, after on the right). In (c) the thesis labels the edges before the transformation
  $e_2$ (upper right) and $e_1$ (lower left) but after it $e_1$ (upper) and $e_2$ (lower); the drawing here keeps
  $e_2$ on the upper and $e_1$ on the lower path in both states, because the edges do not move. In (b) the
  unnamed vertex at the tail of $e_1$ becomes the terminal $c'$, as in the thesis (labels $a'',b''$ in (a), $c'$ in
  (b)).
- Thesis Figures 3.3 (counterexamples), 3.4-3.6 (general path, square graph, general square graph), 3.7 (example
  decomposition), 3.9-3.11 (transformations) are replaced by `counterexamples`, `square-decomposition`,
  `decomposition-example` and `transformations`. Figure 3.8 (the coarser decomposition of the same graph, remark
  S14) and Figure 3.12 (reason why a shortest path has at most two edges in a square) are not redrawn.

## Open points for the author

- `padding`: the four new edges are edges of $F(u',v)$ for every $G$ with $c_G(u,v)\ge 2$, but $G$ is a single
  square only if $c_G(u,v)\ge 3$; for $c_G(u,v)=2$ the minimum cuts of $G$ belong to $F$ as well and $G$ splits
  further. The caption and the sentence in S12 ("the whole of $G$ is one square") should state the hypothesis.
- `decomposition-example`: the terminals of $S_2$ coincide in pairs ($a_2=c_2=a$, $b_2=d_2=b$), as in the thesis
  Figure 3.7; the figure shows the vertices only.
