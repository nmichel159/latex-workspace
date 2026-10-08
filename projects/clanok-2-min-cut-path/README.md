# Article 2 - Min Cut-Path (empty so far)

## Intent

| | |
|---|---|
| Type | journal article – placeholder, no sources yet |
| Content source | **master's thesis *Min Cut-Path* (2025)** – the author's decision of 2026-10-07 |
| Main file | – (`main.tex` once created) |
| PDF | – |
| Origin | empty folder `clanok_2 min cut-path`, renamed according to the convention on 2026-10-07 |

## Status

Empty; waiting for the LaTeX source of the master's thesis.

### Needed before starting

1. **LaTeX source of the master's thesis.** The repository has only the PDF and the extracted text
   (`knowledge/sources/diplomova-praca-2025-min-cut-path.*`). If the source exists (Overleaf, disk), put the zip into `inbox/` –
   formulas, algorithms and figures can then be taken over exactly. Without it the text is transcribed from the PDF.
2. **Scope and title.** Article 1 already used from the thesis: diameter 2, cut at most 2, random graphs (approximation scheme).
   Left unused (see [knowledge/research/min-cut-path.md](../../knowledge/research/min-cut-path.md), Section 4):
   - ch. 2: tree-cut, 2-approximation, global minimum, partial path / partial cut property;
   - ch. 3.3: class *diam or cut 2*, general square graph decomposition, polynomial and linear algorithm;
   - ch. 4.5: almost polynomial average-case algorithm (Path-Cut);
   - ch. 5: symmetric case `c = d = cp`, Filter-BFS, Local-Cut, nearly k-regular graphs.

   The CV lists two working titles: *Polynomial-Time Solutions for Island Structures in the Min Cut-Path Problem* and
   *Random Graph Models for the Min Cut-Path Problem*.
3. **Template.** Start from `templates/article-modular/` (default for new articles, venue-neutral; see `templates/README.md`);
   the target journal is decided later and the manuscript is then ported (`knowledge/writing/template-porting.md`).
   Originally planned: `templates/new-aiaa/` (same as article 1).

## Build

```powershell
.\scripts\build-project.ps1 -Project clanok-2-min-cut-path
```

Only once `main.tex` exists here. From then on the folder follows its template and stays sendable
([latex-conventions.md](../../knowledge/writing/latex-conventions.md) §1.1): the static check after each structural
change, the full run (without `-CheckOnly`) before anything is sent.

```powershell
.\scripts\package-project.ps1 -Project clanok-2-min-cut-path -CheckOnly
```

## Known problems

Watch out when reusing text from the master's thesis. The list of errors found in the thesis is in
[knowledge/research/min-cut-path.md](../../knowledge/research/min-cut-path.md), Section 5a
(concentration of degrees, `α > 1`, bibliography, "NP-hardness is open"). Adapt the text to an article following
[knowledge/writing/academic-style.md](../../knowledge/writing/academic-style.md): sections instead of chapters, `Lemma`/`Theorem`,
notation `\cp`, `\CP`, cite article 1 for NP-completeness.
