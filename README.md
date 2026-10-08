# LaTeX workspace

Articles, theses and the CV of Norbert Micheľ: one source folder per document, one build script, a knowledge base behind
the writing. Files are English; Slovak appears only as data (titles of Slovak documents, quotations, glossary columns);
chat with the owner is Slovak. Rules for Claude Code: [CLAUDE.md](CLAUDE.md).

## Projects

| Project | Document | Main file | PDF | Status |
|---|---|---|---|---|
| [cv](projects/cv/README.md) | CV (AltaCV, English, 2 pages) | `norbert-michel-cv.tex` | [outputs/cv/norbert-michel-cv.pdf](outputs/cv/norbert-michel-cv.pdf) | builds (2 pages) |
| [clanok-1-min-cut-path](projects/clanok-1-min-cut-path/README.md) | article "Min Cut-Path Problem" (English); class `new-aiaa` is temporary, the target journal is undecided and the article will be ported to its template later | `main.tex` | [outputs/clanok-1-min-cut-path/main.pdf](outputs/clanok-1-min-cut-path/main.pdf) | proofread and stylistically revised, modular (`preamble/`, `sections/`), builds without warnings (23 pages); content changes await the author's review |
| [clanok-2-min-cut-path](projects/clanok-2-min-cut-path/README.md) | second article, to be written from the master's thesis | – | – | empty, waiting for the LaTeX source of the master's thesis |

## Layout

```
projects/     LaTeX sources, one folder = one document (edit here)
outputs/      generated PDFs and auxiliary files (never edit; every build overwrites them)
knowledge/    knowledge base: author, research maps, writing guides, venue cards, literature notes, bibliography, source theses
templates/    pristine starting points (article-modular, thesis-modular, new-aiaa, altacv, venue templates)
scripts/      build-project.ps1, check-text.ps1, check-bib.ps1, package-project.ps1
inbox/        new, unprocessed material (zips, PDFs, templates, .bib files)
archives/     original zips, files retired from projects, snapshots before bulk changes
tmp/          scratch (previews, test builds); can be deleted at any time
installers/, .latex-tools/   MiKTeX and Perl installers, portable fallback toolchain
.claude/      skills for Claude Code
```

## Scripts

Run from the workspace root in PowerShell.

| Script | Does |
|---|---|
| `.\scripts\build-project.ps1 -Project <project> [-MainFile <file.tex>] [-InstallMissing]` | the only way to build; PDF lands in `outputs/<project>/`, its path is printed last; `-InstallMissing` lets MiKTeX download a missing package |
| `.\scripts\check-text.ps1 -Project <project> [-Summary]` | style and hygiene findings in the `.tex` sources (phrase list, long sentences, LaTeX hygiene, TODO markers, spelling); changes nothing |
| `.\scripts\check-bib.ps1 -Project <project> [-Summary]` | citations vs. `.bib`, project `.bib` vs. canonical `.bib`, entry hygiene; `-CanonicalOnly` checks the canonical file |
| `.\scripts\package-project.ps1 -Project <project> [-Template <name>] [-MaxPages <n>] [-Flat] [-KeepComments] [-MainFile <file.tex>] [-CheckOnly]` | the only way to make what is sent: checks the venue files against `templates/<name>/` and that nothing refers outside the folder, builds a clean copy, writes `outputs/<project>/package/<project>-<date>.zip` with the PDF beside it and proves that the unpacked zip builds to the same text; last line `Verdict: PASS` or `FAIL`; `-CheckOnly` runs the static checks only |

Parameters and finding categories: the comment header of each script; bibliography rules:
[knowledge/bibliography/README.md](knowledge/bibliography/README.md); the invariant behind the packager (a project
follows its template and can be sent as it is):
[knowledge/writing/latex-conventions.md](knowledge/writing/latex-conventions.md) §1.1.

## Templates

| Folder | Use |
|---|---|
| `article-modular/` | default for every new article |
| `thesis-modular/` | dissertation (`main.tex`) and written work for the dissertation exam (`exam.tex`) |
| `new-aiaa/` | temporary class of article 1 |
| `altacv/` | CV |
| `<venue>/` | journal or conference template from `inbox/`, unpacked pristine |

Details and status: [templates/README.md](templates/README.md).

## How to

| Goal | Do |
|---|---|
| Write or revise text | read the "By task" table in [knowledge/README.md](knowledge/README.md) (skill `academic-writing`) |
| New article | `Copy-Item -Recurse templates\article-modular projects\clanok-<n>-<topic>`, then build (skill `create-latex-pdf`) |
| New dissertation or exam text | copy `templates\thesis-modular` to `projects\praca-<type>-<topic>`; rules: [knowledge/writing/thesis.md](knowledge/writing/thesis.md) |
| New project, structure only | skill `new-latex-project` |
| Add or check a citation | skill `cite-sources` |
| Move an article into a journal template | put the template into `inbox/`, say "process the inbox" (Slovak: *spracuj inbox*), then skill `port-latex-template`: [knowledge/writing/template-porting.md](knowledge/writing/template-porting.md) |
| Send the paper to a reviewer, a co-author or a journal | `.\scripts\package-project.ps1 -Project <project>`; send the zip from `outputs/<project>/package/` only when the last line is `Verdict: PASS`, never a hand-made archive |
| Prepare a submission | skill `prepare-submission`: [knowledge/writing/submission.md](knowledge/writing/submission.md) |
| Review a build or a PDF | skill `review-latex-pdf` |
| Add material | drop it into `inbox/`, say "process the inbox" (skill `process-inbox`) |

Every new project gets a row in the project table here and in `CLAUDE.md`.
Knowledge base: [knowledge/README.md](knowledge/README.md). Project layout, preamble, labels, macros:
[knowledge/writing/latex-conventions.md](knowledge/writing/latex-conventions.md).
