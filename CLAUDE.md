# LaTeX workspace rules

Workspace for Norbert Micheľ's academic writing: journal and conference papers, the PhD dissertation (optimization
algorithms powered by LLMs, UPJŠ Košice), earlier theses and the CV. Every document is built the same way, follows
the same conventions, and is backed by a knowledge base of the author's research, writing rules and sources.

## Rules that always apply

1. **Link the PDF after every change.** Whenever a document source changes, rebuild it and end the reply with a
   clickable link to the generated PDF, e.g. `[outputs/cv/norbert-michel-cv.pdf](outputs/cv/norbert-michel-cv.pdf)`.
   Also send the PDF with `SendUserFile` when that tool is available. This holds for one-line edits too.
   If the build failed, say so, quote the error, and do not present a stale PDF as current.
2. **Sources live only in `projects/<project>/`.** `outputs/` is generated; never edit it by hand.
3. **Never delete the user's files.** Retire a file by moving it to `archives/removed-from-projects/<project>/`.
4. **Do not change scientific content beyond the request** (statements, proofs, wording of a manuscript).
   Problems noticed along the way go into the project's `README.md` under "Known problems" and into the report.
5. **Read the knowledge base before writing or revising academic text** (table "What to read") and keep it current
   when a document introduces a new result, definition, notation or source.
6. **Missing LaTeX packages:** the build fails fast with `File 'x.sty' not found`. Installing downloads from the
   MiKTeX repository, so ask the user first, then build with `-InstallMissing`. Never run `kpsewhich` or `pdflatex`
   directly without `--miktex-disable-installer` / `-disable-installer`: a bare call can install silently or hang
   on a hidden dialog.
7. **Language:** talk to the user in Slovak. Write every file in English (manuscripts, `README.md`, `knowledge/`,
   skills, templates, script comments and messages) unless the user asks for Slovak for a specific text. Slovak
   stays only as data: official names, quotations, glossary entries, the Slovak parts a thesis requires.
8. **Write tight.** Academic text follows `knowledge/writing/academic-style.md`: every sentence carries a
   definition, a result, a reason or a cited fact; no filler, hype, announcements or recaps. Run
   `scripts/check-text.ps1` on changed text and resolve or justify each finding.
9. **Cite only verified sources.** Never write a reference or a claim about the literature from memory. A citation
   enters the canonical `.bib` with a status line first, then the project (`knowledge/bibliography/README.md`);
   a novelty or related-work claim rests on a reading note or a logged search (`knowledge/literature/`). Run
   `scripts/check-bib.ps1` after touching citations.
10. **Unverified facts are marked `TODO(verify)`.** Do not turn them into statements; verify or ask.
11. **Agents:** large multi-part work goes to subagents, at most 4 at a time, each owning its own files and saving
    as it goes. Opus for judgment-heavy work (style audits, regulations, expert guides, adversarial review);
    Sonnet for well-specified or mechanical work (translation, implementing a spec, sweeps, look-ups, integration).
12. **Articles follow their template and stay sendable.** A project with a venue template uses the venue's files
    unmodified, a wrapper `main.tex` written from the venue's sample, and no layout overrides. `projects/<project>/`
    is self-contained at all times. What goes to a journal, reviewer or co-author is the zip made by
    `scripts/package-project.ps1` with `Verdict: PASS`, never a hand-made archive; run it with `-CheckOnly` after
    any structural change (new file, new package, class files touched). A venue template is only ever the
    publisher's download from the official page the venue's guide links, fetched with the user's consent and
    recorded in `templates/SOURCES.tsv`, never hand-made; the package must pass the no-trace check (nothing in it
    names this workspace or an AI tool outside the venue's AI declaration). Full statement, switches and findings:
    `knowledge/writing/latex-conventions.md` §1.1.

## Map

| Path | Contents | Editable |
|---|---|---|
| `projects/<project>/` | LaTeX sources, images, `.bib`, class files, project `README.md` | yes |
| `outputs/<project>/` | generated PDF and auxiliary files | no (build output) |
| `knowledge/` | knowledge base: author, research maps, writing and LaTeX rules, bibliography, literature notes, venue cards, source PDFs with extracted text | yes, keep current |
| `templates/` | starting points for new projects; pristine venue templates | no (copy from) |
| `inbox/` | unprocessed material dropped by the user (templates, PDFs, `.bib`, zips) | process and empty |
| `archives/` | original zips, files retired from projects, snapshots, frozen submission packages (`archives/submissions/<project>/`) | add only |
| `scripts/` | `build-project.ps1`, `check-text.ps1`, `check-bib.ps1`, `package-project.ps1` | infrastructure |
| `tmp/` | scratch (test builds, page previews) | disposable |
| `installers/`, `.latex-tools/` | MiKTeX and Perl installers, portable fallback toolchain | do not touch |

## Projects

| Project | Document | Main file | PDF |
|---|---|---|---|
| `cv` | CV (AltaCV, English, 2 pages) | `norbert-michel-cv.tex` | `outputs/cv/norbert-michel-cv.pdf` |
| `clanok-1-min-cut-path` | article "Min Cut-Path Problem" (English) for Discrete Applied Mathematics, modular (`preamble/`, `sections/`); class `cas-sc` from template `els-cas`; package with `-Template els-cas -Flat` | `main.tex` | `outputs/clanok-1-min-cut-path/main.pdf` |
| `clanok-2-min-cut-path` | second article, to be written from the master's thesis, for Algorithmica; modular skeleton with placeholder text; class `sn-jnl` from template `sn-jnl`; package with `-Template sn-jnl -Flat` | `main.tex` | `outputs/clanok-2-min-cut-path/main.pdf` |

Each project has a `README.md` with its status, file list and known problems. Read it before editing the project
and update it when the status changes. Add a row here and in the root `README.md` when a project is created.

## Workflow

1. Identify the project; read `projects/<project>/README.md`.
2. For academic text, read the knowledge-base files for the task (table below) first.
3. Change only files under `projects/<project>/` unless the user asks for an infrastructure change.
4. Build from the workspace root:

   ```powershell
   .\scripts\build-project.ps1 -Project <project> [-MainFile <main.tex>] [-InstallMissing]
   ```

   `-MainFile` is optional: the script uses `main.tex`, otherwise the only `.tex` containing `\documentclass`.
   The last lines of the output give the PDF path and the relative link.
5. Check: the log for errors, undefined references (`??`, `[?]`) and overfull boxes that damage the layout; pages
   rendered to `tmp/` with `pdftoppm` when the layout matters; and, both read-only:

   ```powershell
   .\scripts\check-text.ps1 -Project <project>      # or -Path <file or folder>: style and hygiene findings
   .\scripts\check-bib.ps1 -Project <project>       # or -CanonicalOnly: citations, .bib hygiene, canonical file
   ```

   Every build ends with the static package verdict (`Package check (static): Verdict: ...`); a `FAIL` there is
   fixed before anything else. Before anything is sent, the full run:

   ```powershell
   .\scripts\package-project.ps1 -Project <project> [-MainFile <file.tex>] [-Template <name>] [-Flat] [-KeepComments] [-CheckOnly] [-MaxPages <n>]
   ```

   It checks the venue files against `templates/<venue>/` and its row in `templates/SOURCES.tsv`, builds a clean
   copy (no `*.md`, `submission/`, `experiments/`, comments), scans everything sent for traces, writes
   `outputs/<project>/package/<project>-<date>.zip` with the PDF beside it and proves that the unzipped package
   compiles to the same text.

6. Report what changed (file and place), anything noticed but not changed, and the PDF link.

## What to read

Full map with maintenance rules: `knowledge/README.md`. Paths below are relative to `knowledge/`.

| Task | Read |
|---|---|
| Author name, affiliation, supervisors, planned papers | `author.md` |
| Min Cut-Path: definitions, notation, results map (thesis vs. article), open problems, glossary | `research/min-cut-path.md` |
| LLMs for optimization (dissertation topic): directions, evaluation practice, terminology | `research/llm-optimization.md`, notes in `literature/` |
| Bachelor thesis on lattice polytopes | `research/lattice-polytopes.md` |
| Writing or revising prose; the author's recurring habits to remove | `writing/academic-style.md` (phrase list: `writing/phrase-list.tsv`) |
| Shape of a paper or section, abstract, introduction, thesis-to-paper | `writing/paper-structure.md` |
| Definitions, statements, proofs, notation, algorithms | `writing/math-writing.md` |
| Computational experiments, LLM-specific reporting, reproducibility | `writing/experiments-reporting.md` |
| Project layout, load order, labels, notation macros | `writing/latex-conventions.md` |
| What may be sent; template conformance; packager findings | `writing/latex-conventions.md` §1.1 |
| How to do something in LaTeX: packages, figures, tables, PDF quality | `writing/latex-guide.md` |
| Moving a manuscript into a journal or conference template | `writing/template-porting.md`, `venues/<venue>.md` |
| Adding or checking a citation | `bibliography/README.md`, `bibliography/references.bib` |
| Related work, novelty claims | `literature/README.md`, `literature/searches.md` |
| Choosing a venue; what a venue requires | `venues/README.md`, `venues/<venue>.md` |
| AI-use statement, arXiv, submission package, cover letter, response to reviewers, self-archiving | `writing/submission.md` |
| Dissertation and dissertation-exam text, UPJŠ rules | `writing/thesis.md` |
| Before handing over any text | `writing/checklist.md` |
| Exact wording of a definition, theorem or proof in the author's theses | `sources/*.txt` (search), then the PDF |

## Templates

| Template | Use |
|---|---|
| `templates/article-modular/` | default for every new article: venue-neutral wrapper `main.tex` + portable `preamble/`, `sections/` |
| `templates/thesis-modular/` | dissertation (`main.tex`) and written work for the dissertation exam (`exam.tex`, build with `-MainFile exam.tex`) |
| `templates/els-cas/` | official Elsevier CAS bundle 2.4 for Discrete Applied Mathematics (class `cas-sc`), from the DAM guide for authors; article 1 |
| `templates/elsarticle/` | official Elsevier `elsarticle` bundle, for Elsevier journals without a CAS template |
| `templates/sn-jnl/` | official Springer Nature journal article template 3.1 (class `sn-jnl`, `.bst` files in `bst/`), recommended by the Algorithmica submission guidelines; article 2 |
| `templates/altacv/`, `templates/new-aiaa/` | CV; former class of article 1 (retired 2026-10-08) |
| `templates/<venue>/` | venue template downloaded from the publisher's official page with the user's consent, archived zip and row in `templates/SOURCES.tsv` (skill `process-inbox`); never edited, because the packager compares projects with it; the folder name is the value of `-Template` |

## Conventions in one paragraph

Project names are lowercase with hyphens (`clanok-<n>-<topic>`, `praca-<type>-<topic>`, `cv`). The main file is
`main.tex`, the only template-dependent file; packages, environments and macros live in `preamble/`, text in
`sections/NN-name.tex` (thesis: `chapters/`), the bibliography in `references.bib`, images in `img/`. A project is
self-contained (class, `.bst` and all inputs inside its folder); `package-project.ps1` turns it into the zip for
Overleaf, a journal or a reviewer.
Labels use prefixes (`sec:`, `def:`, `thm:`, `lem:`, `fig:`, `tab:`, `alg:`, `eq:`); references use cleveref.
New text is written one sentence per source line. Submission material that is not part of the paper (form metadata,
reviews, rebuttal drafts) lives in `projects/<project>/submission/`. Details: `knowledge/writing/latex-conventions.md`.

## Skills

- `latex-workflow`: the shared rules for any LaTeX task here.
- `edit-latex-pdf`: change an existing document, rebuild, link the PDF.
- `review-latex-pdf`: compile, inspect and report on a document.
- `create-latex-pdf`: start a new document from a template and produce its first PDF.
- `new-latex-project`: scaffold a project folder without writing content.
- `academic-writing`: write or revise article and thesis text using the knowledge base.
- `cite-sources`: add or check citations, reading notes and literature searches.
- `port-latex-template`: move a manuscript into a journal or conference template.
- `prepare-submission`: get a manuscript ready for a journal, conference or arXiv.
- `process-inbox`: unpack and file new material from `inbox/` and extend the knowledge base.

## Environment

- Windows, PowerShell. MiKTeX 25.12 and Perl come from scoop and are first on `PATH`; `.latex-tools/` is a
  portable fallback copy. `latexmk` drives pdfLaTeX and picks BibTeX or biber itself.
- Run `build-project.ps1`, `package-project.ps1` and `latexmk` from PowerShell, never from Git Bash: there BibTeX gets `/c/...` paths,
  cannot find the project's `.bst` and `.bib` and may silently read a stray file from the MiKTeX tree (seen 2026-10-08).
- `pdftotext`, `pdftoppm`, `pdfinfo` and `pdffonts` are available for reading and previewing PDFs.
- `latexdiff.exe` on `PATH` is a MiKTeX stub without its script: do not run it. Marked changes for a revision:
  `knowledge/writing/submission.md` §5.3.
- The workspace is its own git repository (branch `main`). Do not commit or stage unless the user asks.
