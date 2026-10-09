# Templates

Starting points for new projects. A project is a copy in `projects/<project>/`; templates themselves change only
as workspace infrastructure, and the pristine venue templates never: `scripts/package-project.ps1` compares the
venue files of a project with them byte by byte (`knowledge/writing/latex-conventions.md`, section 1.1).

| Folder | Use | Origin | Main file | Edit |
|---|---|---|---|---|
| `article-modular/` | **default for new articles**; venue-neutral (`article`, natbib + `plainnat`, cleveref) | built in this workspace 2026-10-07/08 | `main.tex` | infrastructure only |
| `thesis-modular/` | dissertation (`main.tex`) and written work for the dissertation exam (`exam.tex`); rules: `knowledge/writing/thesis.md`, section 7 | built in this workspace 2026-10-08 | `main.tex`, `exam.tex` | infrastructure only |
| `new-aiaa/` | former class of article 1 (until 2026-10-08; article 1 now uses `els-cas/`): `new-aiaa.cls` v1.2, `new-aiaa.bst`, from Overleaf, not a publisher download (kind `other` in `SOURCES.tsv`); `main.tex` and `references.bib` are a workspace skeleton with the author's preamble, not the venue's sample | Overleaf export of article 1 | `main.tex` | never |
| `altacv/` | CV | `archives/CV.zip` (AltaCV 1.7.x, sample `sample.tex`) | `sample.tex` | never |
| `els-cas/` | **template of Discrete Applied Mathematics** and of the other Elsevier journals that ask for the CAS bundle: class `cas-sc` (single column; `cas-dc` is the two-column twin), `cas-common.sty`, `cas-model2-names.bst`, samples, documentation in `doc/`, icons in `thumbnails/` (the class reads `thumbnails/cas-email.jpeg` and `thumbnails/cas-url.jpeg` by relative path), figures of the sample in `figs/`; CAS bundle 2.4, `\ProvidesClass`: `cas-sc 2024/05/04, 2.4` | Elsevier, `els-cas-templates.zip`, linked as "LaTeX template" from the DAM guide for authors (URLs: `SOURCES.tsv`); archive `archives/els-cas-templates.zip`; downloaded 2026-10-08 | `cas-sc-template.tex` (minimal sample: `cas-sc-sample.tex`) | never |
| `elsarticle/` | Elsevier's general class for journals that have no CAS template; numeric citations `elsarticle-template-num.tex`, author-year `elsarticle-template-harv.tex`; `\ProvidesClass`: `elsarticle 2024/04/04, 3.4: Elsevier Ltd` | Elsevier, `elsarticle.zip`, linked as the template package from the Elsevier LaTeX instructions page (URLs: `SOURCES.tsv`); archive `archives/elsarticle.zip`; downloaded 2026-10-08. The zip ships the sources only: `elsarticle.cls` is **generated** from `elsarticle.ins` / `elsarticle.dtx` (docstrip, `latex -disable-installer elsarticle.ins` on a copy, 2026-10-08) and is the only file in the folder that is not in the zip; its SHA-256 is in `SOURCES.tsv` | `elsarticle-template-num.tex` | never |
| `sn-jnl/` | **Springer Nature journal article template** (any Springer Nature journal; recommended by the Algorithmica submission guidelines): class `sn-jnl`, nine `.bst` files in `bst/` (the chosen one is copied next to the main file; Algorithmica: `sn-mathphys-num`, inferred, TODO(verify) in `knowledge/venues/algorithmica.md`), sample `sn-article.tex` and its PDF, `sn-bibliography.bib`, `user-manual.pdf`, dummy figures `empty.eps`, `fig.eps`; template 3.1 (December 2024), `\ProvidesClass`: `sn-jnl 2019/11/18 v0.1` | Springer Nature, zip "Download the journal article template package (December 2024 version)" linked from the Springer Nature LaTeX author support page, which the Algorithmica guidelines link (URLs: `SOURCES.tsv`); archive `archives/sn-article-template.zip`; downloaded 2026-10-08 | `sn-article.tex` | never |
| `<venue>/` | journal or conference template downloaded from the publisher's official page (see "Provenance"); folder name = the packager's `-Template` (naming: `knowledge/writing/template-porting.md`, section 1, step 1) | unpacked pristine | per sample file | never |

## Provenance

A venue template comes only from the publisher's or the venue's official page, downloaded with the owner's consent;
nobody writes one by hand and no third-party copy replaces it. Every template folder has one row in
[`SOURCES.tsv`](SOURCES.tsv) (tab-separated; columns `folder`, `kind`, `version`, `official_url`, `linked_from`,
`archive`, `sha256`, `retrieved`, `note`): the download URL, the official page that links it, the archived zip
under `archives/`, the SHA-256 of that zip and the date. `kind` is `venue` (downloaded from the publisher),
`house` (built in this workspace) or `other` (third-party, not a publisher download). `scripts/package-project.ps1`
checks this file (finding `[template-origin]`): the package fails when the template folder has no row, when a
`venue` row lacks an https URL, its archive or the archive's recorded SHA-256, when the kind is unknown, when the
project's class is a file that no folder here ships (or that the `-Template` folder does not ship), when a folder of
kind `house` holds a class or style file, and when the folder no longer matches its archive file by file (kind
`venue`: every file; kind `other`: the `.cls`, `.bst`, `.sty` files; a file generated from the archive counts when
the row's note records its SHA-256, as for `elsarticle.cls`); a row of kind `other` is reported as a note. So a
folder here is never edited: restore a changed file from the archive. A new venue
template adds its row (and a row in the table above) in the same step that files it (skill `process-inbox`).

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
- `els-cas/` builds as downloaded: `cas-sc-sample.tex` (7 pages) and `cas-sc-template.tex` (4 pages) with
  `latexmk -pdf`, exit code 0, BibTeX with `cas-model2-names.bst` (tested 2026-10-08). MiKTeX packages the class
  needs beyond the base installation: `makecell`, `sttools` (`stfloats.sty`), `moreverb`, `wrapfig`, `colortbl`,
  `stix`, `grfext` (installed 2026-10-08 with the owner's consent). No MiKTeX package ships `charis.sty` (`charissil`
  ships `CharisSIL.sty`), so the class takes its `stix` branch: STIX text and math, as in the publisher's own
  `cas-sc-sample.pdf`. The class also asks for T1 Computer Modern fonts (sans-serif regular and bold extended,
  typewriter), which come from `cm-super` (installed 2026-10-08 with the owner's consent): `cas-sc-template.tex` then
  has Type 1 fonts only (`pdffonts`, 2026-10-08), as the publisher's sample has; without `cm-super` MiKTeX renders
  them as Type 3 bitmaps. Without the `thumbnails/` folder next to the main file the build reports
  `Package pdftex.def Error: File 'thumbnails/cas-email.jpeg' not found` (a flat copy with the icons beside the
  main file fails the same way).
- `elsarticle/`: only the `.cls` generation was checked; a trial build of `elsarticle-template-num.tex` stops at
  `example-image-a` (package `mwe`, not installed).
- `sn-jnl/` builds as downloaded: `sn-article.tex` with `sn-mathphys-num.bst` copied next to it (as the user manual
  instructs), `latexmk -pdf`, exit code 0, 12 pages A4, Type 1 fonts only (tested 2026-10-08; results in
  `archives/test-evidence/2026-10-09/sn-jnl-sample/`). MiKTeX packages installed for it on 2026-10-08 with the owner's consent:
  `threeparttable` (loaded by the class), `jknappen` (`mathrsfs.sty`) and `ncctools` (`manyfoot.sty`), both loaded by
  the sample. Option `lineno` loads `vruler`, not installed (untested). Warnings of the pristine sample:
  `U/rsfs/m/n` size substitutions, `OMS/cmss/m/n` undefined, `h` float specifier changed to `ht`, "No positions in
  optional float specifier", one overfull line (7.56 pt), hyperref "Difference (4) between bookmark levels", and pdfTeX
  "destination with the same identifier" once per float (`float`, loaded by the sample's `algorithm`, comes after the
  class's `hyperref`; a project loads `float` before `\documentclass`, as article 2 does). The
  publisher's `sn-article.pdf` cites author-year ("Campbell and Gear (1995)"), so it was not made from the sample's
  active `sn-mathphys-num` line; a rebuild prints [1]. Line endings in the zip are mixed (`sn-jnl.cls` CR only, some
  files CRLF, others LF); with `.gitattributes` (`* text=auto`, `*.cls text`, `*.bst text`) and `core.autocrlf=true` a
  commit and fresh checkout can rewrite LF and CRLF (lone CR stays), so the folder may then no longer be byte-identical
  to the zip; the same holds for the LF files of `els-cas/`.
- An official UPJŠ dissertation template, if one appears, goes through `inbox/` (skill `process-inbox`).
