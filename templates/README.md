# Templates

Starting points for new projects. A project is a copy in `projects/<project>/`; templates themselves change only
as workspace infrastructure, and the pristine venue templates never: `scripts/package-project.ps1` compares the
venue files of a project with them byte by byte (`knowledge/writing/latex-conventions.md`, section 1.1).

| Folder | Use | Origin | Main file | Edit |
|---|---|---|---|---|
| `article-modular/` | **default for new articles**; venue-neutral (`article`, natbib + `plainnat`, cleveref) | built in this workspace 2026-10-07/08 | `main.tex` | infrastructure only |
| `thesis-modular/` | dissertation (`main.tex`) and written work for the dissertation exam (`exam.tex`); rules: `knowledge/writing/thesis.md`, section 7 | built in this workspace 2026-10-08 | `main.tex`, `exam.tex` | infrastructure only |
| `new-aiaa/` | the class article 1 uses for now (`new-aiaa.cls` v1.2, `new-aiaa.bst`, from Overleaf): the pristine venue files article 1 is compared with; `main.tex` and `references.bib` are a workspace skeleton with the author's preamble, not the venue's sample | Overleaf export of article 1 | `main.tex` | never |
| `altacv/` | CV | `archives/CV.zip` (AltaCV 1.7.x, sample `sample.tex`) | `sample.tex` | never |
| `<venue>/` | journal or conference template the owner drops into `inbox/`; folder name = the packager's `-Template` (naming: `knowledge/writing/template-porting.md`, section 1, step 1) | unpacked pristine | per sample file | never |

## New project

```powershell
# article
Copy-Item -Recurse templates\article-modular projects\clanok-<n>-<topic>
.\scripts\build-project.ps1 -Project clanok-<n>-<topic>

# dissertation
Copy-Item -Recurse templates\thesis-modular projects\praca-<type>-<topic>
.\scripts\build-project.ps1 -Project praca-<type>-<topic>

# written work for the dissertation exam (same project, other main file)
.\scripts\build-project.ps1 -Project praca-<type>-<topic> -MainFile exam.tex
```

Then write the project `README.md` and add the project to the tables in the root `README.md` and `CLAUDE.md`
(details: `article-modular/README.md`, `thesis-modular/README.md`). Moving a manuscript into a venue template:
`knowledge/writing/template-porting.md`. After the copy and after every later structural change:
`.\scripts\package-project.ps1 -Project <project> -CheckOnly`.

## Status (2026-10-08)

- `article-modular/` builds with exit code 0 and no LaTeX warnings (tested in `archives/test-evidence/2026-10-08/latex-article-test4/`, 2026-10-08).
- `thesis-modular/` builds with exit code 0 as the dissertation (`main.tex`, 21 pages) and as the exam work
  (`exam.tex`, 19 pages); the only warnings are the abstract-length checks on the placeholder text. Slovak text
  extracts intact (`pdftotext`), all fonts are Type 1 (tested 2026-10-08), in numeric and in author-date citation
  mode (`settings.tex`). Not provided: PDF/A, the A5 autoreferát; details in `thesis-modular/README.md`.
- `new-aiaa/main.tex` builds (checked 2026-10-07). Until the skeleton cites something, BibTeX reports
  "I found no \citation commands"; the first `\cite` removes it.
- An official UPJŠ dissertation template, if one appears, goes through `inbox/` (skill `process-inbox`).
