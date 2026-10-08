# Rehearsal notes: port of clanok-1-min-cut-path to elsarticle (sandbox)

Sandbox: `tmp/rehearsal/ws/`. Doc = `knowledge/writing/template-porting.md` (TP) / skill `port-latex-template` (SK).

## 0. Reading (fresh session)
- Read CLAUDE.md (in context), SK, TP (all), latex-conventions §1, 1.1, 2-4, DAM venue card, packager header, project README.
- DAM card: no hard page limit. "Note" <= 10 pages, "Contribution" > 10 pages. So `-MaxPages` has nothing to take from the card.
  Article is 23 pages = Contribution. Card says "Editorial Manager: all files in one folder" -> `-Flat`.

## 1. Sandbox
- Built per instructions. `templates/new-aiaa/` holds main.tex, new-aiaa.bst, new-aiaa.cls, references.bib.
- `templates/elsarticle/` holds only `elsarticle.cls`.

## 2. Baseline (sandbox copies of the scripts)
- build-project: exit 0, 23 pages, Letter, no undefined/overfull/multiply defined, blg `warning$ -- 0`.
  pdffonts: all Type 1 embedded. PDF Title empty.
- package-project (default): Verdict PASS, 23 pages, 9 findings (1 layout `\setstretch`, 8 comment).

## 3. Port (TP §1 steps 1-9)
Step 1 (unpack pristine): done by the sandbox set-up; TP says record origin URL + `\ProvidesClass` in `templates/README.md` (not in sandbox; no templates/README.md copied).
Step 2 snapshot: built (23 pp), main.tex -> archives/removed-from-projects/clanok-1-min-cut-path/main-before-port-2026-10-08.tex.
Step 3: elsarticle.cls copied (SHA-256 equal); new-aiaa.cls/.bst moved to archive. `elsarticle` needs only packages in MiKTeX
  (fontenc, graphicx, natbib, geometry, expl3, xparse, etoolbox). `kpsewhich elsarticle.cls` finds nothing in MiKTeX (class only from the template folder).
  DOC GAP: the step-3 grep recipe `grep -E "RequirePackage|LoadClass"` also hits `\IfFileExists{...}` guarded loads (xparse, etoolbox, txfonts, endfloat) - fine, but PowerShell has no grep (workspace is PowerShell; docs show bash grep).
Step 4 wrapper: written from structure of Elsevier sample (not available) -> `\documentclass[preprint,12pt]{elsarticle}`, frontmatter, etc.
Step 5 front matter: title, author+`\ead`, `\affiliation[upjs]{organization,city,country}` (street/postcode NOT in author.md -> owner must supply),
  abstract in frontmatter, keywords + `\MSC[2020]` (placeholders; article has none).
Step 6 preamble: first build with the old preamble UNCHANGED built (exit 0, 30 pp) but with defects the docs did not predict:
  (a) `\paragraph{Title.}` prints "Title.." : elsarticle appends a period to every `\paragraph` title (class l.1068-1070).  NOT IN TP.
  (b) `\begin{enumerate}[label=(\alph*)]` prints "label=(a)" literally: elsarticle redefines enumerate/itemize (class l.1109-1138) and
      takes the optional arg as a label PATTERN; the old class loaded enumitem. Fix: `\usepackage{enumitem}` in preamble/packages.tex. NOT IN TP.
      Silent (no warning, no error): found only by reading pdftotext. TP §3 has a row for "forbids packages" but none for "old class loaded a package the sections use".
  (c) Font warnings `T1/lmr/bx/sc` (bold small caps in problem title) and `T1/lmr/m/scit` (italic small caps in theorem statements): lmodern has no such shapes.
      TP §3 row says "check \textsc in bold for font warnings" but gives no fix; latex-guide §2 gives only the bx/sc fix. scit needs `ssub*lmr/m/scsl`.
  (d) Overfull boxes (10) because 12pt A4-width... text block 390pt: 3 problem tables `p{0.12\linewidth}` (label "Question:" overflows 11.6pt, visible: label touches text),
      4 figures `width=145mm` (> 137mm line), 2 displays (88pt, 63pt), 1 item line (1.6pt). Fixed: tabular p{0.18}/p{0.75} (as in 02-fundamentals), width=\linewidth,
      multline*/gather* for the two displays, microtype (old class loaded microtype; lost with the class) for the 1.6pt line.
      TP §5 says "reword; never shrink fonts or margins"; it does not say that layout-only edits of sections/ (column fractions, figure width in mm, display splitting) are the expected fix.
  (e) Removed from the old wrapper: `inputenc`, `\let\openbox/\Bbbk\relax` (newtxmath no longer loaded), `\AtBeginEnvironment{algorithmic}{\setstretch{1}}` (class has single spacing in preprint; this also removes the [layout] finding).
  (f) Paper size: class `\ExecuteOptions{a4paper,...}` is run BEFORE `\DeclareOption*` (class l.111-112), so `a4paper` is silently dropped; probe (tmp/rehearsal/probe): preprint,12pt -> \paperwidth 614.295pt (Letter), textwidth 390pt; with explicit a4paper -> 597.5pt, textheight 592 vs 548.5.
      TP says nothing. Owner decision whether to pass `a4paper` (the sample does not).
  (g) grfext.sty missing in this MiKTeX: a bare elsarticle document with NO other package after the class fails ("File grfext.sty not found") because `\@curroptions` stays non-empty
      (the latex-guide §3 note 1 describes it for cleveref). The project build is not affected since later `\usepackage` lines reset it. Probe artifact; documented? latex-guide §3 yes, TP no.
  (h) hyperref: elsarticle does not load it; loaded in wrapper `[hidelinks]` as in article-modular. Side effect: class passes `\useelstitle`/`\useauthors` -> PDF Title/Author metadata filled (old PDF had empty). Good.
  (i) natbib: `\PassOptionsToPackage{sort&compress}{natbib}` before \documentclass keeps the old `sort&compress`; elsarticle's `\biboptions` writes `.spl` read at the NEXT run (class l.1240-1248) - avoided.
Step 7 bibliography: `\bibliographystyle{plainnat}` (stand-in for elsarticle-num.bst; alphabetical + numbered = DAM wording). Plain `\cite` unchanged (numeric). 
Step 8/9 build: exit 0, 30 pages (23 -> 30; Letter, 12pt, one column, text width 390pt vs 6.5in/10pt before), 0 warnings, 0 overfull, blg warning$ 0.

## 4. Checks and package
- `-CheckOnly -Template elsarticle`: 0 findings, PASS (after port). check-bib: 0 findings.
- Package default: PASS, 30 pp, 8 [comment] findings (pre-existing end-of-line comments in preamble/); zip 22 files; `.bbl` included; no `.spl`.
- Package `-Flat`: PASS, 30 pp, 22 files in one dir; 9 [comment] (my own end-of-line comment in packages.tex, moved to a full-line comment afterwards -> 8).
  Both zips coexist; both write the same `...-20261008.pdf` (the later run overwrites the earlier one).
- Independent proof: `tar.exe -xf` flat zip -> fresh folder `tmp/rehearsal/flat-proof`, 3x `pdflatex -disable-installer -interaction=nonstopmode -halt-on-error main.tex`:
  exit 0/0/0, 30 pages, 0 `??`/`[?]`, no "Rerun"/undefined, PDF Title/Author filled. No BibTeX needed (`.bbl` in the zip).
- `-MaxPages 10` (DAM "Note" limit) on the 30-page port: finding `[pages] 30 pages, the limit is 10 (20 too many)` but **Verdict: PASS, exit 0, zip and PDF written**.
  TP §1 step 11 / SK step 6 say the packager "proves ... the page limit" and "done on Verdict: PASS" -> misleading. (DAM card: no page limit for a Contribution; "Note <= 10 pages" is a type.)
- Negative conformance: appended one comment line to `elsarticle.cls` in the project -> `[template-file] FAIL ... SHA-256 7FED1E30798E against 663BFD931C50`, `Verdict: FAIL (template-file)`, exit 1;
  restored from `templates/elsarticle/` -> `Findings: 0`, PASS.
- `[layout]` coverage probe (scratch project, CheckOnly): DETECTED geometry, titlesec, fancyhdr, setspace, \linespread, \baselinestretch, \setlength of \parindent/\textwidth/\topmargin/\parskip/\textheight,
  \addtolength textheight, \enlargethispage, \pagestyle, \vspace{-}. NOT detected: `\renewcommand{\section}`/heading redefinitions (incl. my `\els@aparagraph` shim), `\fontsize...\selectfont`,
  `\newgeometry`, `\pdfpagewidth=`, `\setlist{nosep}` (enumitem), `\onehalfspacing` (only the package line is flagged), `\def\maketitle`. `\usepackage{times}` -> [missing] (times.sty not installed).
  So TP §1 "package-project proves the first and the third point" overclaims for the third.
- Text comparison old vs new body (scratchpad norm3.py: pdftotext -layout, NFKC, page numbers/hyphens/whitespace stripped, numbering neutralized):
  letters 38175 -> 38293 (+118 = keywords+MSC line, e-mail footnote, 3 inner list labels (a)(b)(c)); 25 residual hunks, all of these classes:
  front matter (title block, keywords/MSC, `\ead` footnote printed at the page bottom), numbering style (Roman -> Arabic: sections "I." -> "1.", subsections "A." -> "3.1.", "Theorem III.5" -> "Theorem 3.5",
  "Fig. 1" -> "Figure 1:"), citation numbers (plainnat sorts alphabetically; new-aiaa by citation order) and the whole reference list style, list labels (old `\setlist` "1)" at all levels -> new "1." / inner "(a)"),
  math reading order in pdftotext (fractions, limits) and the two split displays, line breaks/hyphenation.
  sections/ source diff: only layout edits (3 tabular column specs x2 values, 4 figure widths, 2 displays); no word changed.
- Project README porting log not written in the sandbox copy (README is not part of the package).

## 5. Doc corrections made (real workspace: knowledge/writing/template-porting.md, .claude/skills/port-latex-template/SKILL.md)
TP: intro (second exception: layout-only edits; preamble also regains old-class packages); §1 conformance bullet (packager proves only point 1; what [layout] sees / misses; [pages] does not fail);
 step 3 (PowerShell form instead of grep); step 6 (list old class packages); step 9 (pdftotext old/new compare); step 11 (-MaxPages only when the card states a limit; PASS with [pages] is not done);
 §3 rows (natbib options via \PassOptionsToPackage; class without hyperref; old class packages used by sections; Latin Modern bx/sc + scit); §5 row (narrower text block layout-only edits);
 §6.2 elsarticle row; §6.3 elsarticle traps (\paragraph period, enumerate/enumitem, Letter paper, \affiliation data, plainnat stand-in/[template-bst], grfext); §7 log line.
SK: step 4 (old-class packages, layout-only edits allowed and logged), step 5 (pdftotext compare), step 6 (-MaxPages omitted without a card limit; [pages] does not fail; unseen overrides), comment line.
Tested [template-bst]: stand-in elsarticle-num.bst in sandbox template -> `[template-bst] \bibliographystyle{plainnat}: the template ships elsarticle-num.bst`, exit 0 (not a FAIL); removed again.
