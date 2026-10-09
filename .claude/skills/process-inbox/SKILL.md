---
name: process-inbox
description: Unpack and file new material the user dropped into inbox/ (zips, PDFs, templates, .bib files), and extend the knowledge base with what it contains.
---

# Process the inbox

Use this skill when the user says there is new material, asks to unpack or sort files, or when `inbox/` is not
empty at the start of a task.

1. List `inbox/` and look inside every archive before extracting (`unzip -l`). Read text files; view images.
2. File each item:

   | Item | Destination |
   |---|---|
   | zip of a project that already exists here | section "Returned copy of a project" |
   | zip with a LaTeX project | extract to `projects/<project>/` (naming: `knowledge/writing/latex-conventions.md`, section 1), move the zip to `archives/` |
   | zip or folder with a venue template | section "Venue template" |
   | PDF of the author's own work | `knowledge/sources/<type>-<year>-<topic>.pdf` plus text; steps in `knowledge/sources/README.md` |
   | PDF of a paper by others | section "Paper PDF" |
   | `.bib` file | section "`.bib` file" |
   | anything else | by content; what cannot be classified stays, ask the user |

   Extract text with `pdftotext -layout -enc UTF-8 <file>.pdf <file>.txt`.
3. New project: bring it to the layout of `templates/article-modular/` (wrapper `main.tex`, `preamble/`, `sections/`,
   `references.bib`, `img/`; thesis: `chapters/`; `knowledge/writing/latex-conventions.md`, section 1), move
   unused template leftovers to `archives/removed-from-projects/<project>/`, write its `README.md`, add it to the
   project tables in `CLAUDE.md` and the root `README.md`, and build it. A class that came with the project
   (`.cls`, `.bst`, e.g. in an Overleaf export) is not a publisher download: copy it unmodified to
   `templates/<name>/` with a `templates/SOURCES.tsv` row of kind `other` (archive: the project zip), so the packager
   can compare the project with it; before the project is sent to a venue, the venue's official template replaces it
   (section "Venue template", then skill `port-latex-template`). Material filed into a project is sent one day:
   comments that name workspace files, `TODO` markers and image metadata naming tools fail the packager's `[trace]`
   check (`knowledge/writing/latex-conventions.md`, section 1.1, point 4). Finish with
   `.\scripts\package-project.ps1 -Project <project> -CheckOnly` (same file, section 1.1).
4. New source document of the author: add a row to `knowledge/sources/README.md` and write or extend the overview in
   `knowledge/research/`; compare with what the knowledge base already says and record differences.
5. Never delete anything from the inbox; every file ends up in a project, `templates/`, `knowledge/` or `archives/`.
6. Report what went where, what was learned, any problems found, and a clickable PDF link for every project built.

## Venue template

A venue template is only ever the publisher's download, never hand-made, reconstructed or taken from a third-party
copy (Overleaf gallery, an old project, a co-author's folder).

1. **Source.** Find the template link on the venue's guide for authors (or on the publisher's LaTeX page that the
   guide points to). Ask the owner before downloading, naming the file, the URL and the size; download into an
   empty folder. A zip the owner dropped into `inbox/` counts as the publisher's only when its SHA-256 equals that
   of the download from the official URL; otherwise file the official download and archive the dropped zip as
   other material.
2. Unpack pristine to `templates/<venue>/`, move the zip to `archives/` under its original name, never edit the
   folder afterwards: the packager compares every project that uses the template with it, byte by byte. Folder
   name: the template's name (`knowledge/writing/template-porting.md`, section 1, step 1). A file the bundle ships
   only as source (e.g. `elsarticle.cls` from `.ins`/`.dtx`) is generated on a copy and recorded in the row's note.
3. Add a row to `templates/SOURCES.tsv` (tab-separated: `folder`, `kind` = `venue`, `version` = the
   `\ProvidesClass` line, `official_url` = the https download URL, `linked_from` = the guide page that links it,
   `archive` = the zip under `archives/`, `sha256` of that zip, `retrieved` date, `note`) and a row to
   `templates/README.md`. The packager's `[template-origin]` check fails a project whose template folder has no
   such row (`templates/README.md`, Provenance).
4. Write the card `knowledge/venues/<venue>.md`, or update the existing one, from the template's own documentation
   (sample file, author guide) and the venue's pages, following `knowledge/venues/README.md` (rules, card template).
   Its *LaTeX* field names the folder in `templates/`. Dated facts, unknowns `TODO(verify)`; a new card is added to
   the comparison table there.
5. Build the template's own sample in a copy under `tmp/` and record missing packages and warnings in the Status
   section of `templates/README.md`.
6. Offer skill `port-latex-template` for the project the owner has in mind. Its package must pass the packager,
   including the no-trace check (`knowledge/writing/latex-conventions.md`, section 1.1, point 4).

## Returned copy of a project

A zip or Overleaf export of an existing project that comes back from a co-author, the supervisor or a journal:

1. Never unpack it over `projects/<project>/`. Unpack to `tmp/returned-<project>-<YYYY-MM-DD>/`; move the zip to `archives/`.
2. Compare: `git diff --no-index --stat projects/<project> tmp/returned-<project>-<YYYY-MM-DD>`, then the same
   without `--stat` per changed file (`--word-diff` for text). A flat copy made with `-Flat` has no subfolders:
   compare file by file.
3. Show the owner the list of changes; apply the accepted ones by hand in `projects/<project>/` (changes to
   statements or proofs: CLAUDE.md rule 4), rebuild, run `package-project.ps1 -CheckOnly`, record the round in the
   project README under "Change history".

## Paper PDF

1. Entry first: skill `cite-sources` (the file name is the BibKey).
2. PDF to `knowledge/sources/papers/<BibKey>.pdf` (create the folder if missing), text next to it as `<BibKey>.txt`.
3. Reading note and topic map: `knowledge/literature/README.md`, section "Adding a paper".

## `.bib` file

Every entry goes through `knowledge/bibliography/README.md`, section 2. An entry not confirmed against its primary
record gets a `TODO` or `PARTIAL` status line, never `VERIFIED`. Then `.\scripts\check-bib.ps1 -CanonicalOnly`.
