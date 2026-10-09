# Preserving revision of article 1 (2026-10-09): shared brief for all editors

Workspace root: `/home/user/latex-workspace`. Working folder (this file's folder):
`projects/clanok-1-min-cut-path.submission/revision-2026-10-09/` (called `R/` below).

The manuscript `projects/clanok-1-min-cut-path/main.tex` was split into fragments in `R/`:
`frag-0-preamble.tex`, `frag-A-front-1-2.tex` (title page, abstract, Sections 1-2), `frag-B-3.tex` (Section 3),
`frag-C-4-5.tex` (Sections 4-5), `frag-D-6-7.tex` (Sections 6-7, acknowledgments), `frag-Z-end.tex`.
The untouched original is also at `archives/removed-from-projects/clanok-1-min-cut-path/main-before-preserving-revision-2026-10-09.tex`.
Each editor owns exactly one fragment (edits it in place) plus its own `R/changes-<X>.md` and `R/issues-<X>.md`.
Do not edit any other file except where your task names it.

## 1. The owner's two instructions (both apply)

1. *First request:* make the NP-completeness proof (Section 3) clearer and easier to navigate (it is a wall of
   text, the reader gets lost); improve the whole article, find errors; no extremely long paragraphs; no wording
   typical of AI-generated text; add sources where they matter, Discrete Applied Mathematics papers especially welcome.
2. *Second request (overrides the first where they conflict):* act as a careful mathematical editor, not a
   summarizer. **Preserve all mathematical content.** In particular:
   - Never delete a definition, lemma, theorem, remark, corollary, proof, proof step, algorithm, auxiliary
     procedure (`BuildChain`, `Thread`, `Calibrate`), figure, citation or technical explanation. Never replace an
     argument by a shorter summary. Never turn a formal `definition`/`lemma`/`theorem` environment into prose.
   - Do not change hypotheses, quantifiers, claims, notation, algorithm steps or the logical structure silently.
     Do not add new mathematical claims.
   - Allowed: English, punctuation, clarity, transitions; reordering *within* a section when the logic is kept;
     making implicit steps explicit; putting an argument that is already in the text into a `proof`; splitting a
     long proof into lemmas whose proofs carry every original step; consistent notation where it does not change
     meaning; cross-references; better formatting of cases.
   - A possible mathematical error, a gap, or anything you think should be deleted or restated: **do not fix it in
     the text**; write it to `R/issues-<X>.md` with the exact place, why, and a precise proposed correction
     (ready-to-paste LaTeX when practical). Exception: a gap you close by adding a justification sentence that makes
     an already-claimed step explicit (no new claim) may be applied; log it in `changes-<X>.md` as "made explicit".
   - The text must not get substantially shorter. The original builds to 15 pages; the revision should be about the
     same or slightly longer. Do not optimize for fewer words.
   - Owner's rule in `knowledge/writing/academic-style.md` §11 says the same; read it.

## 2. Style (read before writing)

Read `knowledge/writing/academic-style.md` (all) and `knowledge/writing/math-writing.md` (all). Key points:
- One sentence per source line. Sentences about 15-25 words, split above 40. Paragraphs short (at most about
  5-6 sentences); one point per paragraph.
- No text about the text ("We now show", "It remains to", "In this section", "We are now ready"), no
  recaps, no praise, no "crucial/notably/leverage/underscore/delve/pivotal/robust/seamless", no "not only ...
  but also", no rhythmic triads, at most one dash parenthesis per paragraph, no "Formally:" after a paraphrase.
  Plain, specific mathematical English. Allowed: "Recall that", "Conversely,", "In particular,", "Suppose that".
- American spelling; authorial "we"; present tense; `\emph{}` only at a term's first definition.
- Figure captions stay one line.
- Use the macros `\cp`, `\CP`, `\diam`, `\OPT`, `\MinCutPath`, `\SSP`, `\ThreeSAT`.
- `Theorem~\ref{...}` style references (no cleveref). Keep every existing `\label` unchanged.
- No comment in the `.tex` may name this workspace, its paths (`knowledge/`, `scripts/`, `R/`, ...), a Markdown
  file, an AI tool, "TODO", or "verify". Keep comments to what a co-author needs, or none.
- Do not write `TODO(verify)` into the `.tex`; put doubts into `issues-<X>.md`.

## 3. Shared decisions (all editors keep these so the fragments fit together)

- Global setting stays as in Section 2: graphs undirected and finite; `n = |V|`, `m = |E|` (Section 3 overrides
  with variables/clauses, as it says). Whether to add "simple" is an issue to report (editor A), not to apply.
- Section 3 will contain these new labels (editor B creates them; others may cite them):
  `lem:chain-paths` (shortest paths are exactly the chain paths), `lem:synchronization` (a chain path hits all
  synchronization threads iff it is consistent), `lem:clause-threads` (a consistent chain path hits all clause
  threads iff its assignment satisfies the formula), `lem:separating` (the consistent chain path of a satisfying
  assignment is separating), `sec:reduction-construction` (the subsection with the construction / Algorithm 1),
  `sec:reduction-correctness` (the subsection with the lemmas and the proof of Theorem 3.5).
- Existing labels everywhere stay: `def:cut-path`, `def:cut-paths`, `def:cp-value`, `lem:basic-bounds`,
  `def:approximation-scheme`, `sec:ssp`, `def:chain-link`, `def:chain`, `def:thread`, `def:threading`,
  `thm:ssp-np-complete`, `alg:reduction`, `sec:ssp-to-mcp`, `thm:mcp-np-complete`, `def:diameter`,
  `lem:cut-decomposition`, `lem:empty-i-or-l`, `lem:odd-intersection`, `thm:diameter-two`, `rem:algorithm`,
  `thm:cut-two`, `thm:random-diameter-two`, `thm:random-diameter`, `thm:random-connectivity`, `lem:degree-bounds`,
  `lem:connectivity-bounds`, `thm:approximation-scheme`, all `fig:` and `sec:` labels.
- "With high probability" (w.h.p.) may be defined once at the start of Section 6 as "with probability tending to
  one as n tends to infinity" and used in prose; the displayed limit statements of theorems stay.
- Probability is written `\mathbb{P}(\,\cdot\,)` (round brackets) everywhere. Inline fractions in running text use
  the solidus (`p = \alpha \log n / n`, `1/\alpha`); displayed `e^{x}` becomes `\exp(x)` (DAM style; log it).
- Citations: only keys present in `knowledge/bibliography/references.bib` with a `VERIFIED` status line, and only
  for claims backed by the reading notes in `knowledge/literature/`. A key not yet in
  `projects/clanok-1-min-cut-path/references.bib` is listed in your `changes-<X>.md` under "bib keys to add"; the
  integrator copies the entries. No theorem/page numbers in `\cite[...]` unless the note verifies them for the
  printed version.

## 4. Process (usage limits interrupt runs: save as you go)

- First action: append "started" to `R/progress-<X>.md`. Then work section by section (or proof by proof); after
  finishing each unit, save the fragment and append one line to `R/progress-<X>.md` saying what is done.
- If `R/progress-<X>.md` already lists done units when you start, you were interrupted: continue from there, do
  not redo.
- Inventory before editing: list every environment (definition/lemma/theorem/remark/proof/algorithm/figure/problem
  box/list of cases) of your fragment with its label in `R/inventory-<X>.md`. At the end, confirm against it that
  everything is still present (and say where each item is now).
- Compile check: build the integrated document yourself to catch LaTeX errors in your fragment:
  `cd R && cat frag-0-preamble.tex frag-A-front-1-2.tex frag-B-3.tex frag-C-4-5.tex frag-D-6-7.tex frag-Z-end.tex > /tmp/<X>-test/main.tex`
  then copy `projects/clanok-1-min-cut-path/*` except `main.tex` into `/tmp/<X>-test/` and run
  `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` there (other editors may be mid-edit; if their
  fragment breaks the build, substitute the original fragment from the archived original for the check).
- `R/changes-<X>.md`: what changed and where, grouped as Language / Exposition / Made explicit / Formatting /
  Citations; each item one line.
- `R/issues-<X>.md`: numbered; each item tagged [M] possible mathematical error or gap, [C] change that would alter
  a claim, [D] proposed deletion or substantial restructuring, [S] other suggestion; with place, reason and the
  exact proposed text.
- Finish with a short report (under 200 words) as your final message.
