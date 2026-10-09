# Next task: make article 1 ready for Discrete Applied Mathematics

Brief for the next session that works on `projects/clanok-1-min-cut-path/main.tex` ("Min Cut-Path Problem").
Written 2026-10-09 at the end of the preserving revision; state: 17 pages, builds clean, static package check PASS,
everything on `main`.

## 0. Read first (in this order)

1. `CLAUDE.md` (workspace rules: talk Slovak, write English, link the PDF after every change, never delete files).
2. `projects/clanok-1-min-cut-path.md` (notes; the top paragraph and "Change history" of 2026-10-09).
3. `projects/clanok-1-min-cut-path.submission/revision-2026-10-09/REPORT.md` (what changed, what is still open), then
   the `issues-*.md` files and `review-math.md` there; `referee-assessment.md` if it has content.
4. `knowledge/writing/academic-style.md` (all, especially §1.1 and §11), `knowledge/writing/math-writing.md`.
5. The whole `main.tex`, once, before any edit.

## 1. What the author wants (learned the hard way; do not relearn)

- **Preserve, do not compress.** Every definition, lemma, theorem, proof step, Algorithm 1 and figure stays unless
  the author approves a deletion. Formal definitions stay `definition` environments.
- **No new objects in proofs.** The author rejected an auxiliary multigraph and "Step 1-5" headings in Lemma 3.8.
  He wants proofs that follow the original logic, are complete, and are easy to navigate: a one-sentence plan,
  a few named parts, a table where it helps (Table 1 in Lemma 3.8 is the accepted form).
- **His notation wins.** Algorithm 1 uses his map `M`, `Lits`, `l[0]`, `l[1]`; he rejected the occurrence sets `O_i`.
  Before introducing any symbol, check that it is used at least three times and clashes with nothing.
- **Figures must match the proof.** When he asks for a figure change that would contradict the proof, explain
  the conflict and ask (Figure 10, 2026-10-09). Captions stay one line.
- **Short paragraphs, plain sentences, no text that reads as machine-written.**
- **Work incrementally:** one section, build, check, commit, push to `main` (fast-forward), show the PDF; then the
  next section. He follows the PDF, not the diff.
- **Ask in batches.** Collect the decisions that are his into one short numbered question list, recommend an
  answer for each, and continue with the work that does not depend on them.

## 2. Environment (cloud container)

- TeX: `apt-get install -y texlive-latex-extra texlive-science texlive-fonts-extra texlive-bibtex-extra latexmk poppler-utils cm-super`.
- PowerShell: GitHub release tarball `powershell-7.4.6-linux-x64.tar.gz` into `/opt/pwsh`, link `pwsh`.
- The scripts pass MiKTeX switches; on TeX Live put shims for `pdflatex` and `kpsewhich` that drop
  `-disable-installer`/`--miktex-disable-installer` first on `PATH`.
- Build: `pwsh -NoProfile -File scripts/build-project.ps1 -Project clanok-1-min-cut-path`; checks:
  `scripts/check-text.ps1`, `scripts/check-bib.ps1`. The full `package-project.ps1` run fails on Linux with an
  internal path check (`Refusing to delete outside tmp/package-*`); run it on the author's Windows machine.
- Pushing needs the Claude GitHub App on `nmichel159/latex-workspace`; if `git push` returns 403, tell the author
  at once and hand over a `git bundle` plus a zip so no work is lost.
- Usage limits cut long runs: subagents must save after every unit and log progress in a file.

## 3. Plan

### Phase A - decisions to collect first (one message, with recommendations)

1. Global renames of clashing symbols: cut `C` vs clauses `C_k`/`\mathcal{C}`; threshold `k` vs clause index `k`;
   solution `F` vs `S`; parts `I, J, K, L` (Section 4) vs links `I_i, T_i, L_{j,k}`; algorithm `A` vs sides
   `A_1, A_2`. Recommendation: clauses stay `C_k`; cut sides `A_1, A_2` -> `V_1, V_2`; parts -> `X_1, Y_1, Y_2, X_2`
   or keep and rename the links; threshold -> `t`; solution always `S`.
2. New results he may want (proposals in `issues-A.md` 8, `issues-B.md` 15-16): the 2-approximation
   `|C u P| < 2 cp(u,v)`; "deciding cp(u,v) = d(u,v) is NP-complete"; maximum degree three in the reduction graph.
3. Definition 2.5 vs Theorem 6.6 (uniform measure vs `G(n,p)`): restate Theorem 6.6 as a w.h.p. ratio bound
   (`issues-D.md` 8) or reword Definition 2.5 with a probability.
4. Definitions 3.3/3.4 (thread defined through "every other thread"; finished path vs path being extended):
   replace by a static description of the threads that Algorithm 1 creates (`issues-B.md` 10-11).
5. Lemma 4.2 as a definition (`issues-C.md` 1).
6. Front matter: title, keywords, novelty sentence vs his master's thesis (`issues-A.md` 1, 10-12), AI declaration
   (`projects/clanok-1-min-cut-path.submission/ai-declaration.tex`), funding, highlights.

### Phase B - verify the mathematics by computation (new; do this before more prose work)

- Implement Algorithm 1 in Python (networkx) exactly as printed, including `Calibrate`. For all 3-SAT formulas with
  up to 3-4 variables and 1-3 clauses (and random larger ones), check by brute force: Lemma 3.5 (shortest paths =
  chain paths), Lemmas 3.6-3.7, Lemma 3.8 and Theorem 3.9 (a separating shortest path exists iff the formula is
  satisfiable). Also check the vertex counts and `Lambda` against the running-time paragraph.
- Brute-force `cp(u,v)` on small graphs: verify Theorem 4.5 on all graphs of diameter two with up to 7 vertices,
  Theorem 5.1 on cacti, Lemma 2.4 in general, and the two parked counterexamples of the class "diam or cut 2".
- Keep the scripts in `projects/clanok-1-min-cut-path.submission/checks/`; report the results; any failure is a
  finding for the author, never a silent fix.

### Phase C - mathematics and structure, section by section

1. Section 3: give Lemmas 3.5-3.7 and the proof of Theorem 3.9 the same shape as Lemma 3.8 (plan sentence, named
   parts); check that every lemma states exactly what the theorem uses; the definitions of chain path, hit,
   consistent may become one `definition` environment if the author agrees.
2. Section 4: proof of Theorem 4.5 - make the counting readable (one display, three labelled contributions that
   match Figure 10); check the figure once more against the text.
3. Section 5: the cactus paragraph as a lemma with proof (it is now argued in running text).
4. Section 6: sources. Theorem 6.3 is not verified first-hand (Bollobas-Thomason 1985 / Bollobas, Section 7.2);
   theorem numbers of Chung-Lu (journal version) and Frieze-Karonski (printed edition) are open; the year of
   Frieze-Karonski (2015 or 2016). Use `cite-sources`; add `\cite[Theorem~x]` only with a verified location.
5. Section 1: related work. Repeat the logged searches (`knowledge/literature/searches.md`), look again for DAM
   papers (the author values them), and check that every sentence matches its reading note.

### Phase D - language and layout

- `check-text.ps1` must show only the known false positives (problem name "Most Vital Edges", authors before
  `\cite`, the one novelty sentence).
- Read each section aloud-test style: paragraphs at most about 6 sentences, no announcements or recaps.
- Layout: render pages with `pdftoppm`; reduce empty space around floats only with the class's own keys.

### Phase E - final review and hand-over

- An independent adversarial review (fresh agent, Opus) of the whole PDF as a DAM referee; fix what it finds or
  report it.
- Full packager run on Windows: `package-project.ps1 -Project clanok-1-min-cut-path -Template els-cas -Flat -KeepComments` must end with `Verdict: PASS`.
- Update the project notes, `REPORT.md`, the knowledge base (`knowledge/research/min-cut-path.md`), and the
  root `README.md` row.

## 4. Definition of done

- Every proof checked by hand and, for Sections 2-5, by computation on small cases.
- No symbol with two meanings; every symbol used at least three times or replaced by words.
- Every open item in `REPORT.md` either applied (with the author's approval) or explicitly declined by him.
- `check-text.ps1` and `check-bib.ps1` clean apart from judged false positives; full packager PASS.
- The author has seen the PDF of every section after its change.

## 5. What would make this plan better (reflection)

- **Gate early, not late.** The costliest loops of 2026-10-09 came from changes the author had not asked for
  (multigraph, `O_i`, compression). Phase A exists for this; keep it short and do it first.
- **Check by computation.** Hand checks and model reviews agreed on Lemma 3.8 three times while its presentation
  changed; an executable model of the reduction gives certainty that no rewrite breaks the argument.
- **Use subagents for review, not for writing the key proof.** Parallel editors produced inconsistent style and
  new notation; the accepted Lemma 3.8 was written in one hand after thinking. Let agents check, count and search.
- **One notation table** (symbol, meaning, where defined, how often used) maintained in the notes would have caught
  `O_i`, `delta(A)` vs `delta(G)` and `L_{j,k,i}` vs `L_{j,k}` before they reached the PDF.
- **Measure, do not guess:** pages and words per section before and after each phase, so length changes are
  deliberate.
- **Show, then commit to a direction:** for a rewrite of a central proof, show one page to the author before
  rewriting its neighbours in the same style.
