# Checklist

Run it after writing or revising any part, and in full before submission. Items marked ● correspond to an error that
actually occurred in article 1 or in the master's thesis ([academic-style.md](academic-style.md) §9–§10). References
point to the rule: AS = [academic-style.md](academic-style.md), PS = [paper-structure.md](paper-structure.md),
MW = [math-writing.md](math-writing.md), LG = [latex-guide.md](latex-guide.md),
LC = [latex-conventions.md](latex-conventions.md), SB = [submission.md](submission.md).

Machine checks first:

```powershell
.\scripts\check-text.ps1 -Project <project>    # phrases, sentence length, LaTeX hygiene
.\scripts\check-bib.ps1 -Project <project>     # citation keys, fields, agreement with the canonical .bib
.\scripts\build-project.ps1 -Project <project> # then read the log
```

## Structure

- [ ] The main claim fits in one sentence and appears in the abstract and in the introduction (PS §1).
- [ ] ● The abstract states results (classes, bounds, numbers), not only motivation; no citations, no undefined symbols (PS §4).
- [ ] Each contribution in the introduction is a checkable statement pointing to a theorem, table or section (PS §5).
- [ ] ● The introduction compares with the closest published work; a novelty claim rests on a logged search (PS §6).
- [ ] The relation to the author's earlier texts (master's thesis, conference abstract) is stated and cited (PS §5).
- [ ] ● Each heading names its content (PS §8).
- [ ] The conclusion does not repeat the introduction; open problems are specific questions (PS §10).

## Concision

- [ ] The first sentences of the paragraphs read as a continuous line (AS §5).
- [ ] ● No definition or statement appears twice (AS §3.4).
- [ ] ● No sentence merely announces the next sentence, definition or section (AS §3.7, §8).
- [ ] No scene-setting at the start of the abstract, the introduction or a section (AS §3.2).
- [ ] ● No evaluative adjectives about one's own work (AS §3.6).
- [ ] `check-text.ps1` reports no hit in `filler`, `wordy`, `hype`, `hedge`, `meta`, `ai-tic` that was not kept on purpose (AS §7).

## Leftovers from another document

- [ ] ● The article contains no *chapter*, *thesis*, *Chapter 3*; only *section*, *paper* (PS §13).
- [ ] ● No paragraph refers to a figure, theorem or notion that is not in the document (search the PDF for `??`).
- [ ] ● Notation is uniform (`CP(u,v)`, not `cut-path(u,v)` in places) (MW §1).

## Consistency

- [ ] ● The environment name matches the reference text (a lemma is not cited as *Claim*).
- [ ] ● *Lemma*, *Theorem*, *Section*, *Figure* before a reference are capitalized and joined by `~` (or `\cref`) (LC §7, LG §11).
- [ ] ● The same notion has the same name everywhere (*shortest path* vs. *min path*) (AS §3.9).
- [ ] ● The definition in the text and the problem box say the same thing (MW §3).
- [ ] ● No letter means two things (`m` = number of edges and number of clauses) (MW §1).
- [ ] ● Indices of one object keep their order everywhere (`L_{j,k,i}`) (MW §1).
- [ ] Spelling is consistently American (AS §2).

## Mathematics

- [ ] ● An optimization problem is *NP-hard*, a decision problem *NP-complete* (MW §4).
- [ ] ● Theorem hypotheses match those of the lemmas used (`p = ...` vs. `p ≥ ...`, `α > 0` vs. `α > 1`) (MW §4).
- [ ] ● Quantifiers are not mixed with a limit (*for all n > n₀* together with `lim`) (MW §1).
- [ ] ● Every theorem has a proof or a citation (MW §4).
- [ ] ● Pseudocode brackets match and its variables are those of the text (MW §6).
- [ ] ● A theorem quoted from the literature says what the source says (watch "for every `ε`" in concentration bounds) (MW §4).
- [ ] ● A cut in a statement is either "an edge set whose removal separates `u` and `v`" or `δ(A)`; parity and decomposition arguments hold only for the second kind.
- [ ] ● A letter for a set or object does not clash with a value (`c(u,v)` is a number, not a cut) (MW §1).
- [ ] Every theorem can be quoted on its own (contains its hypotheses) (MW §4).
- [ ] *With high probability* and asymptotic symbols have one definition in the document (MW §1).

## Experiments

Full list: [experiments-reporting.md](experiments-reporting.md) §9. At least:

- [ ] Every experiment answers a question stated in the text.
- [ ] Instances and their source, baselines with equal budgets, number of runs, spread, hardware and time are given.
- [ ] For LLMs: exact model identifier and access date, sampling parameters, prompts (appendix), calls, tokens, cost.
- [ ] Each table or plot is understandable from its caption alone; axes have names and units.
- [ ] Claims do not exceed the data; limitations are named (PS §9).
- [ ] Code and data are available, or the text says why not.

## Typesetting

- [ ] ● Operators with a backslash (`\deg`, `\min`, `\max`, `\log`, `\lim`) (LC §6, LG §5).
- [ ] ● `\[ ... \]` instead of `$$ ... $$`; no stray `\Bigr.` (LG §5).
- [ ] ● Variables in running text are in math mode (`$p$`, not `(p)`) (LG §11).
- [ ] ● Every figure has a `\caption` (a title and a description) and is cited in the text by its number (`Figure~\ref{fig:...}`), not only shown; a figure that appears only in its own caption is not cited (MW §7, LC §8).
- [ ] ● The end-of-proof mark is not alone on a line (`\qedhere`) and "Proof." is not attached to an algorithm (LC §4, LG §6).
- [ ] Tables without vertical rules (`booktabs`), numbers aligned on the decimal point (LG §9).
- [ ] The PDF contains no `??`, no `[?]`, no line overflowing into the margin (LG §12, §17).

## Language

- [ ] ● Typos and doubled words (*egde*, *prove show*, *the this*) (AS §10).
- [ ] ● Articles: *an average*, not *a Average*; *a shortest path*; no article before *Claim 19* (AS §10).
- [ ] ● Capitals only at the start of a sentence, in proper names and in numbered references (*Lemma 3*, not *lemma 3*) (AS §10).
- [ ] ● Parentheticals set off by dashes or commas (`objectives---connectivity and control---serve`) (LG §11).
- [ ] ● No sentence missing its noun (*for large random graphs*).
- [ ] ● No Slovak calques: *thanks to*, *it holds that*, *for better understanding*, *we will* for the text itself (AS §10).
- [ ] Uncountable nouns without a plural (*information*, *research*, *work*, *literature*) (AS §10).

## Bibliography

Rules and status tags: [../bibliography/README.md](../bibliography/README.md).

- [ ] ● Every cited key exists and the PDF shows no `[?]`.
- [ ] ● Journal, volume and pages agree with the DOI; ISBNs have a valid check digit.
- [ ] ● The cited work really contains what is attributed to it (reading note in `knowledge/literature/`).
- [ ] ● The author's own earlier work is cited where the text relies on it.
- [ ] A preprint is replaced by its published version if one exists.
- [ ] Every project entry comes from `knowledge/bibliography/references.bib` and has the status `VERIFIED` there (legacy `OVERENE` counts as verified).

## Dissertation and dissertation-exam text

- [ ] Formal requirements, structure and template follow [thesis.md](thesis.md) §2–§3 and §7.
- [ ] Chapters built from papers give the full reference of each paper and the author's share; results of the master's thesis are cited as prior work ([thesis.md](thesis.md) §4).

## Before submission

- [ ] The venue card was re-opened and updated; template, length, citation style and mandatory statements match it (SB §3.2 step 1, `knowledge/venues/`).
- [ ] ● The manuscript meets the card's rules on the abstract, figures, math and tables, checked in the PDF: the abstract states the main results; every figure is cited in the text and its caption has a title and a description; the venue's math conventions (DAM: solidus for small inline fractions, `\exp` for powers of e, consecutive equation numbers); tables without vertical rules and shading (`knowledge/venues/<venue>.md`).
- [ ] The project meets the clean-build criteria (LC §2).
- [ ] The author has checked the items under "Content changes to review" in the project `README.md`.
- [ ] The AI-use statement follows the publisher's policy (SB §1).
- [ ] No `TODO`, `\fillin`, commented-out old text or notes for co-authors are left in the source.
- [ ] Form title, abstract, keywords and codes come from `projects/<project>/submission/metadata.txt` (SB §3.1).
- [ ] `package-project.ps1` ends with `Verdict: PASS` for the venue's template, page limit and folder form; every `[layout]`, `[comment]` and `[unused]` line is resolved or justified; the uploaded zip is the one it wrote (LC §1.1, SB §3.2 step 3).
- [ ] No trace of the workspace or of AI tools in the package: no `[trace]` FAIL; every allowed `[trace]` note is the AI declaration or a term in `submission/package-allow.txt` with a reason; `Template origin:` shows the venue's download; the `AI declaration:` line matches what was used and what the venue requires (LC §1.1 point 4, SB §1.3).
- [ ] The PDF built by the submission system is compared with the one in `upload/` (SB §3.2 step 7).
- [ ] Double-anonymous venue: the anonymization sweep is done (SB §3.3).
- [ ] The cover letter is written where the venue asks for one (SB §4).
- [ ] The uploaded state is frozen in `archives/submissions/<project>/` (SB §3.2 step 6).
- [ ] arXiv: endorsement, source bundle and metadata follow SB §2.
- [ ] Revision: response letter and marked PDF are done, every cited location exists in the revised PDF (SB §5).
