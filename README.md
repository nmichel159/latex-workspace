# LaTeX workspace

Articles, theses and the CV of Norbert Micheľ: one source folder per document, one build script, a knowledge base behind
the writing. Files are English; Slovak appears only as data (titles of Slovak documents, quotations, glossary columns);
chat with the owner is Slovak. Rules for Claude Code: [CLAUDE.md](CLAUDE.md).

## Projects

| Project | Document | Main file | PDF | Status |
|---|---|---|---|---|
| [cv](projects/cv/README.md) | CV (AltaCV, English, 2 pages) | `norbert-michel-cv.tex` | [outputs/cv/norbert-michel-cv.pdf](outputs/cv/norbert-michel-cv.pdf) | builds (2 pages) |
| [clanok-1-min-cut-path](projects/clanok-1-min-cut-path/README.md) | article "Min Cut-Path Problem" (English) for Discrete Applied Mathematics; class `cas-sc` (official Elsevier CAS template `els-cas`) | `main.tex` | [outputs/clanok-1-min-cut-path/main.pdf](outputs/clanok-1-min-cut-path/main.pdf) | proofread and revised, modular (`preamble/`, `sections/`); ported to the DAM template 2026-10-08, builds (16 pages since the review fixes of 2026-10-09); flat package `Verdict: PASS` (`-Template els-cas -Flat`); content changes and submission items (keywords, AI declaration, funding, figures, abstract results, figure citations) await the author |
| [clanok-2-min-cut-path](projects/clanok-2-min-cut-path/README.md) | second article, to be written from the master's thesis, for Algorithmica; class `sn-jnl` (official Springer Nature template `sn-jnl`) | `main.tex` | [outputs/clanok-2-min-cut-path/main.pdf](outputs/clanok-2-min-cut-path/main.pdf) | template prepared 2026-10-08, placeholder text only, builds (2 pages); flat package `Verdict: PASS` (`-Template sn-jnl -Flat`); waiting for the LaTeX source of the master's thesis |

## Layout

```
projects/     LaTeX sources, one folder = one document (edit here)
outputs/      generated PDFs and auxiliary files (never edit; every build overwrites them)
knowledge/    knowledge base: author, research maps, writing guides, venue cards, literature notes, bibliography, source theses
templates/    pristine starting points (article-modular, thesis-modular, venue templates els-cas, elsarticle and sn-jnl, altacv, new-aiaa); origins in SOURCES.tsv
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
| `.\scripts\package-project.ps1 -Project <project> [-Template <name>] [-MaxPages <n>] [-Flat] [-KeepComments] [-MainFile <file.tex>] [-CheckOnly]` | the only way to make what is sent: checks the venue files against `templates/<name>/` and its recorded download in `templates/SOURCES.tsv`, and that nothing refers outside the folder, builds a clean copy, scans everything sent for traces of the workspace and of AI tools (outside the AI declaration), writes `outputs/<project>/package/<project>-<date>.zip` with the PDF beside it and proves that the unpacked zip builds to the same text; last line `Verdict: PASS` or `FAIL`; `-CheckOnly` runs the static checks only |

Parameters and finding categories: the comment header of each script; bibliography rules:
[knowledge/bibliography/README.md](knowledge/bibliography/README.md); the invariant behind the packager (a project
follows its template and can be sent as it is):
[knowledge/writing/latex-conventions.md](knowledge/writing/latex-conventions.md) §1.1.

## Templates

| Folder | Use |
|---|---|
| `article-modular/` | default for every new article |
| `thesis-modular/` | dissertation (`main.tex`) and written work for the dissertation exam (`exam.tex`) |
| `els-cas/` | official Elsevier CAS bundle 2.4 for Discrete Applied Mathematics (class `cas-sc`), from the DAM guide for authors; article 1 |
| `elsarticle/` | official Elsevier `elsarticle` bundle, for Elsevier journals without a CAS template |
| `sn-jnl/` | official Springer Nature journal article template 3.1 (class `sn-jnl`), recommended by the Algorithmica submission guidelines; article 2 |
| `altacv/` | CV |
| `new-aiaa/` | former class of article 1 (retired 2026-10-08) |
| `<venue>/` | journal or conference template downloaded from the publisher's official page (linked from the venue's guide for authors) with the owner's consent, unpacked pristine; zip in `archives/`, row in `SOURCES.tsv`; never hand-made |

Details and status: [templates/README.md](templates/README.md).

## How to

| Goal | Do |
|---|---|
| Write or revise text | read the "By task" table in [knowledge/README.md](knowledge/README.md) (skill `academic-writing`) |
| New article | `Copy-Item -Recurse templates\article-modular projects\clanok-<n>-<topic>`, then build (skill `create-latex-pdf`) |
| New dissertation or exam text | copy `templates\thesis-modular` to `projects\praca-<type>-<topic>`; rules: [knowledge/writing/thesis.md](knowledge/writing/thesis.md) |
| New project, structure only | skill `new-latex-project` |
| Add or check a citation | skill `cite-sources` |
| Move an article into a journal template | name the journal; the template is downloaded (with the owner's consent) from the publisher's page that the journal's guide for authors links and filed by skill `process-inbox`, then skill `port-latex-template`: [knowledge/writing/template-porting.md](knowledge/writing/template-porting.md) |
| Send the paper to a reviewer, a co-author or a journal | `.\scripts\package-project.ps1 -Project <project> [-Template <venue>] [-Flat]`; send the zip from `outputs/<project>/package/` only when the last line is `Verdict: PASS`, never a hand-made archive |
| Prepare a submission | skill `prepare-submission`: [knowledge/writing/submission.md](knowledge/writing/submission.md) |
| Review a build or a PDF | skill `review-latex-pdf` |
| Add material | drop it into `inbox/`, say "process the inbox" (skill `process-inbox`) |

Every new project gets a row in the project table here and in `CLAUDE.md`.
Knowledge base: [knowledge/README.md](knowledge/README.md). Project layout, preamble, labels, macros:
[knowledge/writing/latex-conventions.md](knowledge/writing/latex-conventions.md).
