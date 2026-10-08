# Knowledge base

Everything to read before writing or revising an article, a dissertation text or the CV: the author's research, writing
rules, venue facts, literature notes, bibliography. Files are English; Slovak appears only as data (official names, glossary).

## Files

| Path | Contents | Read when |
|---|---|---|
| [author.md](author.md) | name forms, affiliation, studies, supervisors, planned publications | title page, author block, acknowledgments, CV |
| [research/min-cut-path.md](research/min-cut-path.md) | Min Cut-Path: definitions, notation, results map (thesis vs. article 1), errors in the thesis, open problems, glossary | any text on Min Cut-Path |
| [research/lattice-polytopes.md](research/lattice-polytopes.md) | bachelor's thesis: lattice polytopes in the cube, main results | the thesis is mentioned or cited |
| [research/llm-optimization.md](research/llm-optimization.md) | dissertation field: LLMs for algorithm design and optimization, directions, critical studies, evaluation practice, terminology, unverified leads | any text on the dissertation topic, related work |
| [writing/academic-style.md](writing/academic-style.md) | sentences, paragraphs, concision rules, the author's habits, English of a Slovak author, revision procedure | writing or revising any text |
| [writing/paper-structure.md](writing/paper-structure.md) | what goes into title, abstract, introduction, related work, core, conclusion; thesis to paper | planning or writing a section |
| [writing/math-writing.md](writing/math-writing.md) | notation, definitions, statements, proofs, algorithms, figures for constructions | any mathematical content |
| [writing/experiments-reporting.md](writing/experiments-reporting.md) | instances, baselines, budgets, LLM specifics, statistics, reproducibility, what to claim | any computational experiment |
| [writing/checklist.md](writing/checklist.md) | tick list after each change and before submission | after writing; before submission |
| [writing/phrase-list.tsv](writing/phrase-list.tsv) | phrase patterns read by `scripts/check-text.ps1` | adding or changing a pattern |
| [writing/latex-conventions.md](writing/latex-conventions.md) | house rules: project layout, the invariant "follows its template and can be sent" with the packager (§1.1), preamble order, environments, labels, macros, citations | starting a project; editing sources; adding files or packages; sending a project |
| [writing/latex-guide.md](writing/latex-guide.md) | LaTeX craft with reasons: packages, references, math, floats, tables, bibliography, build hygiene, PDF quality | a layout, package or build problem |
| [writing/template-porting.md](writing/template-porting.md) | moving a manuscript into a venue class; front-matter map, class quirks, porting log | a venue template is chosen or arrives |
| [writing/submission.md](writing/submission.md) | AI-use policies and statement, arXiv, submission package, cover letter, response to reviewers, preprints and licenses | preparing a submission or revision |
| [writing/thesis.md](writing/thesis.md) | UPJŠ rules: dissertation, written work for the dissertation exam, dissertation from papers, template requirements | any dissertation or exam text |
| [bibliography/](bibliography/README.md) | `references.bib` (canonical, status line per entry) and the rules: path of a citation, fields, keys, `check-bib.ps1` | adding, checking or citing a source |
| [literature/](literature/README.md) | one reading note per paper (`<BibKey>.md`), `searches.md` search log, `_template.md` | citing a work the text builds on; related work; novelty claim |
| [venues/](venues/README.md) | comparison table and one card per journal or conference series | choosing a venue; before submitting |
| [sources/](sources/README.md) | PDFs and extracted text of the author's theses, errata; later also papers by others (subfolder papers, see `literature/README.md`) | exact wording of a definition, theorem or proof |

## By task

Read in the order given; `check-*` and `package-project.ps1` are the scripts in `scripts/`.

| Task | Read |
|---|---|
| New section | `research/<topic>.md` → `paper-structure.md` → `academic-style.md` §9 → `math-writing.md` (if definitions or proofs) → `latex-conventions.md` → `check-text.ps1` |
| Revise for concision | `academic-style.md` §3, §9, §11 → `check-text.ps1` → `checklist.md` "Concision" |
| Definition or proof | `research/<topic>.md` (notation) → `math-writing.md` → `sources/*.txt`, then the PDF (exact wording) → `latex-conventions.md` §4, §6 |
| Experiments | `experiments-reporting.md` → `research/llm-optimization.md` §9 → `literature/` notes → `checklist.md` "Experiments" |
| Add a citation | `bibliography/README.md` §2 → `literature/README.md` → `check-bib.ps1` |
| Related work | `paper-structure.md` §6 → `research/<topic>.md` → `literature/` notes → `literature/searches.md` → `bibliography/README.md` §8 |
| Choose a venue | `venues/README.md` (table) → cards of the candidates → `paper-structure.md` → `author.md` |
| Port to a template | `template-porting.md` → `venues/<venue>.md` → `latex-guide.md` §3 → `latex-conventions.md` (§1.1) → `package-project.ps1` |
| Submit | `venues/<venue>.md` → `checklist.md` → `submission.md` → `check-text.ps1`, `check-bib.ps1` → `package-project.ps1` |
| Send a project to a reviewer, co-author or Overleaf | `latex-conventions.md` §1.1 → `package-project.ps1` |
| Dissertation or exam text | `thesis.md` → `paper-structure.md` → `academic-style.md` → `checklist.md` "Dissertation and dissertation-exam text" → `templates/thesis-modular/README.md` |

## Maintenance

| Event | Update |
|---|---|
| Material arrives in `inbox/` | skill `process-inbox`; a PDF goes to `sources/` with its `.txt` and a row in `sources/README.md` |
| A project adds a result, definition or notation | `research/<topic>.md` (results map, notation, glossary) |
| A new citation | canonical `bibliography/references.bib` first, then the project copy |
| A paper is read | note in `literature/`; row in the topic map in `research/` |
| A literature search is run | row in `literature/searches.md`, also when nothing was found |
| A venue page is read | card in `venues/` with the checked date |
| A project changes status | `projects/<project>/README.md` |
| A project gains, renames or loses a file, a package or class files | `package-project.ps1 -CheckOnly` (`writing/latex-conventions.md` §1.1) |

- Unverified fact: `TODO(verify)`. A guess is never a statement.
- Dates in ISO form (`2026-10-08`). Every fact about the outside world carries its source (URL, file, page) and the date it was checked.
- Exact wording of a thesis: `sources/*.txt` locates it, the PDF decides (formulas in `.txt` are scrambled).
- Pointer, not copy: a rule lives in one file; other files link to it.
