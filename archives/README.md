# Archive

Original files as they arrived, files retired from projects, and snapshots taken before bulk changes.
Nothing here is compiled and nothing here is edited.

| Item | What it is | Where the content was unpacked |
|---|---|---|
| `CV.zip` | AltaCV template with a sample CV (2026-09-25) | `templates/altacv/` (pristine copy); the working CV is `projects/cv/` |
| `clanok_1_min_cut_path.zip` | Overleaf export of article 1 (2026-10-07) | `projects/clanok-1-min-cut-path/` |
| `els-cas-templates.zip` | Elsevier CAS bundle 2.4 (`cas-sc.cls`, `cas-dc.cls`), the LaTeX template of Discrete Applied Mathematics, downloaded from the publisher 2026-10-08; SHA-256 and URLs in `templates/SOURCES.tsv` | `templates/els-cas/` (pristine copy of the top folder `els-cas-templates/`) |
| `elsarticle.zip` | Elsevier `elsarticle` bundle (class sources `elsarticle.ins` / `elsarticle.dtx`, templates, `.bst` files), downloaded from the publisher 2026-10-08; SHA-256 and URLs in `templates/SOURCES.tsv` | `templates/elsarticle/` (pristine copy of the top folder `elsarticle/` plus the generated `elsarticle.cls`) |
| `sn-article-template.zip` | Springer Nature journal article template package 3.1 (December 2024 version; class `sn-jnl`), recommended by the Algorithmica submission guidelines, downloaded from the publisher 2026-10-08; the server's file name, SHA-256 and URLs in `templates/SOURCES.tsv` (archived under the name of its top folder) | `templates/sn-jnl/` (pristine copy of the top folder `sn-article-template/`) |
| `removed-from-projects/cv/` | template leftovers retired from `projects/cv/`: modified `sample.tex`, `sample.bib`, `pubs-authoryear.tex`, sample images, logo `nieco2.jpg`, class README and CHANGELOG; in `outputs/` the old PDF and auxiliary files from `sample.tex` | – |
| `removed-from-projects/clanok-1-min-cut-path/` | original `sample.bib` (with sample AIAA entries) and unused `graph.jpg`; earlier versions of the article sources and bibliography: `main-before-revision-2026-10-07.tex`, `main-before-split-2026-10-07.tex`, `references-before-revision-2026-10-07.bib` | – |
| `submissions/<project>/<YYYY-MM-DD>-<venue>-<stage>/` | frozen submission package: `upload/` (every uploaded file) and `source/` (copy of the project at that moment); stage `v1`, `r1`, `final`, `arxiv-v1` | created by the procedure in `knowledge/writing/submission.md` §3.2; none yet |
| `test-evidence/2026-10-08/` | sources of the test builds that the guides, template READMEs and the article 1 README cite (package and counter tests, class-compatibility harness, template builds, thesis template variants, before/after hashes of the article 1 split); copied from the disposable `tmp/`; table of folders and citing documents in its `README.md` | – |
| `test-evidence/2026-10-09/` | results of the test builds behind the Springer Nature template and article 2 (pristine `sn-article.tex` build, float-anchor and EPS test); table of folders and citing documents in its `README.md` | – |
| `before-translation-2026-10-07/` | snapshot of the workspace documents taken on 2026-10-07 before their translation into English, kept under the same relative paths (`CLAUDE.md`, `README.md`, `.claude/skills/`, `archives/README.md`, `inbox/README.md`, `knowledge/`, `projects/*/README.md`, `scripts/`, `templates/`); compare a current file with `before-translation-2026-10-07/<same path>` to check a translation | – |

## Rules

- A zip that arrives in `inbox/` is moved here under its original name after unpacking.
- A file retired from a project is not deleted – it moves to `removed-from-projects/<project>/`.
- A snapshot folder such as `before-translation-2026-10-07/` is never edited or deleted; its files keep their pre-translation wording.
- A submission package is frozen on the day of the upload and never edited; the next revision gets its own folder.
