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
   project tables in `CLAUDE.md` and the root `README.md`, and build it. A venue class that came with the project
   (`.cls`, `.bst`) is also copied unmodified to `templates/<venue>/`: the packager compares the project with it.
   Finish with `.\scripts\package-project.ps1 -Project <project> -CheckOnly` (same file, section 1.1).
4. New source document of the author: add a row to `knowledge/sources/README.md` and write or extend the overview in
   `knowledge/research/`; compare with what the knowledge base already says and record differences.
5. Never delete anything from the inbox; every file ends up in a project, `templates/`, `knowledge/` or `archives/`.
6. Report what went where, what was learned, any problems found, and a clickable PDF link for every project built.

## Venue template

1. Unpack pristine to `templates/<venue>/`, move the zip to `archives/`, never edit the folder afterwards: the
   packager compares every project that uses the template with it, byte by byte. Folder name: the template's name
   (`knowledge/writing/template-porting.md`, section 1, step 1).
2. Add a row to `templates/README.md` with origin URL and class version (the `\ProvidesClass` line).
3. Write the card `knowledge/venues/<venue>.md`, or update the existing one, from the template's own documentation
   (sample file, author guide) and the venue's pages, following `knowledge/venues/README.md` (rules, card template).
   Its *LaTeX* field names the folder in `templates/`. Dated facts, unknowns `TODO(verify)`; a new card is added to
   the comparison table there.
4. Offer skill `port-latex-template` for the project the owner has in mind.

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
