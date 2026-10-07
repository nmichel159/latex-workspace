# LaTeX workspace rules

Workspace for Norbert Micheľ's academic writing: journal articles, theses and the CV. Every document is built
the same way, follows the same conventions, and is backed by a knowledge base of the author's research.

## Rules that always apply

1. **Link the PDF after every change.** Whenever a document source changes, rebuild it and end the reply with a
   clickable link to the generated PDF, e.g. `[outputs/cv/norbert-michel-cv.pdf](outputs/cv/norbert-michel-cv.pdf)`.
   Also send the PDF with `SendUserFile` when that tool is available. This holds for one-line edits too.
   If the build failed, say so, quote the error, and do not present a stale PDF as current.
2. **Sources live only in `projects/<project>/`.** `outputs/` is generated; never edit it by hand.
3. **Never delete the user's files.** Retire a file by moving it to `archives/removed-from-projects/<project>/`.
4. **Do not change scientific content beyond the request** (statements, proofs, wording of a manuscript).
   Problems noticed along the way go into the project's `README.md` under "Známe problémy" and into the report.
5. **Read the knowledge base before writing or revising academic text** (see "Knowledge base" below) and keep it
   current when a document introduces a new result, definition or notation.
6. **Missing LaTeX packages:** the build fails fast with `File 'x.sty' not found`. Installing downloads from the
   MiKTeX repository, so ask the user first, then build with `-InstallMissing`. Never run `kpsewhich` or `pdflatex`
   directly without `--miktex-disable-installer` / `-disable-installer`: a bare call can install silently or hang
   on a hidden dialog.
7. **Language:** talk to the user in Slovak. `README.md` files and `knowledge/` are Slovak; `CLAUDE.md` and skills
   are English; a manuscript is edited in its own language.

## Map

| Path | Contents | Editable |
|---|---|---|
| `projects/<project>/` | LaTeX sources, images, `.bib`, class files, project `README.md` | yes |
| `outputs/<project>/` | generated PDF and auxiliary files | no (build output) |
| `knowledge/` | knowledge base: author, research summaries, conventions, bibliography, source PDFs with extracted text | yes, keep current |
| `templates/` | pristine starting points for new projects | no (copy from) |
| `inbox/` | unprocessed material dropped by the user | process and empty |
| `archives/` | original zips and files retired from projects | add only |
| `scripts/build-project.ps1` | the single supported build entry point | infrastructure |
| `tmp/` | scratch (page previews etc.) | disposable |
| `installers/`, `.latex-tools/` | MiKTeX and Perl installers, portable fallback toolchain | do not touch |

## Projects

| Project | Document | Main file | PDF |
|---|---|---|---|
| `cv` | CV (AltaCV, English, 2 pages) | `norbert-michel-cv.tex` | `outputs/cv/norbert-michel-cv.pdf` |
| `clanok-1-min-cut-path` | article "Min Cut-Path Problem" (English); class `new-aiaa` is temporary, the target journal is undecided and the article will be ported to its template later | `main.tex` | `outputs/clanok-1-min-cut-path/main.pdf` |
| `clanok-2-min-cut-path` | second article, to be written from the master's thesis; no sources yet (only `README.md`) | – | – |

Each project has a `README.md` with its status, file list and known problems. Read it before editing the project
and update it when the status changes. Add a row here and in the root `README.md` when a project is created.

## Workflow

1. Identify the project; read `projects/<project>/README.md`.
2. For academic text, read the relevant knowledge-base files first.
3. Change only files under `projects/<project>/` unless the user asks for an infrastructure change.
4. Build from the workspace root:

   ```powershell
   .\scripts\build-project.ps1 -Project <project> [-MainFile <main.tex>] [-InstallMissing]
   ```

   `-MainFile` is optional: the script uses `main.tex`, otherwise the only `.tex` containing `\documentclass`.
   The last lines of the output give the PDF path and the relative link.
5. Inspect the result: check the log for errors, undefined references (`??`, `[?]`) and overfull boxes that damage
   the layout; render pages to `tmp/` with `pdftoppm` when the layout matters.
6. Report what changed (file and place), anything noticed but not changed, and the PDF link.

## Knowledge base

| Need | Read |
|---|---|
| Overview and maintenance rules | `knowledge/README.md` |
| Author name, affiliation, supervisors, planned papers | `knowledge/author.md` |
| Min Cut-Path: definitions, notation, results map (thesis vs. article), open problems, glossary | `knowledge/research/min-cut-path.md` |
| Bachelor thesis on lattice polytopes | `knowledge/research/lattice-polytopes.md` |
| Project layout, preamble, labels, notation macros, citation rules | `knowledge/writing/latex-conventions.md` |
| Structure and phrasing of the author's texts, pre-submission checklist | `knowledge/writing/academic-style.md` |
| Verified bibliography entries | `knowledge/bibliography/references.bib` |
| Exact wording of a definition, theorem or proof | `knowledge/sources/*.txt` (search), then the PDF |

Facts that are not verified are marked `TODO(overiť)`; do not turn them into statements.

## Conventions in one paragraph

Project names are lowercase with hyphens (`clanok-<n>-<tema>`, `praca-<typ>-<tema>`, `cv`). The main file is
`main.tex`, the bibliography `references.bib`, images live in `img/`. A project is self-contained (class, `.bst`
and all inputs inside its folder) so it can be zipped for Overleaf or a journal. Labels use prefixes (`sec:`,
`def:`, `thm:`, `lem:`, `fig:`, `alg:`). Details: `knowledge/writing/latex-conventions.md`.

## Skills

- `latex-workflow`: the shared rules for any LaTeX task here.
- `edit-latex-pdf`: change an existing document, rebuild, link the PDF.
- `review-latex-pdf`: compile, inspect and report on a document.
- `create-latex-pdf`: start a new document from a template and produce its first PDF.
- `new-latex-project`: scaffold a project folder without writing content.
- `academic-writing`: write or revise article and thesis text using the knowledge base.
- `process-inbox`: unpack and file new material from `inbox/` and extend the knowledge base.

## Environment

- Windows, PowerShell. MiKTeX 25.12 and Perl come from scoop and are first on `PATH`; `.latex-tools/` is a
  portable fallback copy. `latexmk` drives pdfLaTeX and picks BibTeX or biber itself.
- `pdftotext`, `pdftoppm` and `pdfinfo` are available for reading and previewing PDFs.
- The folder sits inside a git repository rooted at the user's home directory and is untracked there.
  Do not commit, stage or `git init` unless the user asks.
