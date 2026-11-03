# Presentations (Beamer)

Rules for talks. Section 2 records the author's style, read on 2026-11-02 from the three decks in
`projects/prezentacie/ukazky/` (`phd-1-semester` January 2026, `phd-2-semester` June 2026, `csgt-26`).

## 1. Where things live

All talks form one collection, `projects/prezentacie/`; layout and the index of talks: `projects/prezentacie.md`.

| What | Where |
|---|---|
| Samples from the author (reference only, never built or sent) | `projects/prezentacie/ukazky/` |
| Starting point | `templates/beamer-talk/` (`main.tex`, `references.bib`; kind `house`) |
| A talk | `projects/prezentacie/<category>/<group>/<talk>/`, category `predmety`, `konferencie`, `seminare` or `ostatne`; flat folder |
| PDF | `outputs/prezentacie/<category>/<group>/<talk>/main.pdf` |

New talk, from the workspace root:

```powershell
New-Item -ItemType Directory -Force projects\prezentacie\konferencie\csgt-2026
Copy-Item -Recurse templates\beamer-talk projects\prezentacie\konferencie\csgt-2026\min-cut-path
.\scripts\build-project.ps1 -Project prezentacie/konferencie/csgt-2026/min-cut-path
```

`-Project` takes the same path in `check-text.ps1`, `check-bib.ps1` and `package-project.ps1`. Then add a row to the
table of talks in `projects/prezentacie.md`; a talk gets no notes file and no row in `CLAUDE.md` or the root
`README.md`. The package check reports `Template: none (standard class beamer)`, as for any class from the TeX
distribution; its `ai-declaration` note does not apply to slides, and a `TODO` left on a slide is a `[trace]` FAIL
until it is filled in.

## 2. The author's style

The samples use theme `Madrid`. The template `beamer-talk` keeps their colors and structure in a richer look, written
in its `main.tex` without a theme (owner's request of 2026-11-02: a plain flat look was rejected):

- Class `beamer` with `t` (top-aligned frames), `aspectratio=43` (169 also works), Fira Sans with `newtxsf` math,
  pdfLaTeX, no overlays and no section pages.
- Blue RGB 0,85,150 with darker and brighter shades, red RGB 250,0,75. Each frame is a white card with a soft shadow on
  a pale blue page. Headline with all sections; frame title on a gradient bar lit from above, with a red slanted edge;
  footer of three slanted segments (author, title on red, `n/N`).
- The author's logo is part of the template: the point graph `D(n, m)` of the bachelor thesis, from `logo/logo.svg` in
  the repository `nmichel159/tricka`. `scripts/logo-to-pdf.py` writes the same vector path as `logo-white.pdf` and
  `logo-tint.pdf`, because pdfLaTeX cannot include SVG, and `logo-cover.pdf`, white with an opacity growing to the right
  shape by shape. On the covers `logo-cover.pdf`, as a texture in the title bar `logo-white.pdf`, pale in the corner of
  the card `logo-tint.pdf`.
- No TikZ fadings: some PDF viewers draw their soft masks wrongly, with a visible vertical edge (seen 2026-11-02). Soft
  edges use `\softedge`, overlapping strips of constant opacity.
- The university seal `logopfupjsf.jpg` is a circle in a square JPG, so it is always drawn by `\myseal`, which cuts it
  to the circle.
- `\titleframe` and `\closingframe`: gradient cover; title, author, `\supervisor`, institute, date, seal. Empty
  `\supervisor` drops its line.
- Frames: bold key followed by a value in itemize (`\textbf{Date:} ...`), photo or logo below or in a right column,
  status labels `\done{...}`, `\inprogress{...}`. Blocks with a title bar for definitions and theorems.
- Tables: columns `L{width}`, header `\rowcolor{myuniversity}` with `\head{...}`, row labels `\rowhead{...}`, alternating
  rows by themselves. Section names stay short, because all of them fit in the headline.
- Last two frames: references (`\scriptsize`) and `\closingframe{Thank you for your attention}`.
- References by BibTeX style `plain`, numbered items (`\setbeamertemplate{bibliography item}[text]`), because beamer's
  default icon is a PDF from the TeX tree, whose path stays in the PDF objects and fails the packager (`[trace]`).
- Harmless log message: `Token not allowed in a PDF string ... \translate` from the `\bibliography` inside a frame.

Structure of a PhD progress report (`phd-*-semester`), 17 to 23 frames: Contents; Study and Teaching Activities;
Supervision and Consulting; Conferences and Events, with a lighter frame of photos; Research; Future Plans. The
January 2026 report weighs research with definitions and algorithms, the June 2026 report activities. Conference talk
(`csgt-26`), 22 frames: one line of motivation, definitions with a figure, statement, construction in steps, result.

Length: one frame takes about a minute, so 20 minutes means about 18 frames; an algorithm in `\tiny`, as in the
samples, cannot be read in a talk and belongs in backup at most.

## 3. Writing slides

- Language: English unless the author asks for Slovak for a specific talk.
- A talk says what the article says: statements, notation and citations come from the project and the knowledge
  base (rules 4, 9, 10 of `CLAUDE.md`), never from memory. A simplified statement is marked as such.
- Words on a slide are not sentences to read: short phrases and formulas, not the article's paragraphs.
- A fact not yet known goes on the slide as `\fillin{...}`, printed in red with `TODO(verify)`.
- A sample's text is not a source: a citation is taken from the canonical `.bib`, not from the sample.

## 4. MiKTeX packages

Installed 2026-11-02 at the owner's request: `beamer`, `beamertheme-metropolis`, `pgfopts`, `appendixnumberbeamer`,
`fira`, `sansmathaccent`, `translator`; the template uses `fira` but no longer the theme `metropolis`. The other
packages of the template (`tcolorbox`, `newtxsf`, `colortbl`) were already present. The packages for the samples came
with the build of 2026-11-02 under `-enable-installer`.
