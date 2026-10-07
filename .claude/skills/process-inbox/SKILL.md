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
   | zip with a LaTeX project | extract to `projects/<project>/` (name per convention), move the zip to `archives/` |
   | zip with a template | extract to `templates/<name>/`, move the zip to `archives/` |
   | PDF of the author's work or a key reference | `knowledge/sources/<typ>-<rok>-<tema>.pdf` plus extracted text |
   | `.bib` file | verified entries into `knowledge/bibliography/references.bib` |

   Extract text with `pdftotext -layout -enc UTF-8 <file>.pdf <file>.txt`.
3. For a new project: bring it to the standard layout (`main.tex`, `references.bib`, `img/`), move unused template
   leftovers to `archives/removed-from-projects/<project>/`, write its `README.md`, add it to the project tables in
   `CLAUDE.md` and the root `README.md`, and build it.
4. For a new source document: add a row to `knowledge/sources/README.md` and write or extend a summary in
   `knowledge/research/` (problem, notation, main results with their numbers, open problems, bibliography).
   Compare with what the knowledge base already says and record differences.
5. Never delete anything from the inbox; every file ends up in a project, `templates/`, `knowledge/` or `archives/`.
   Leave what cannot be classified and ask the user.
6. Report what went where, what was learned, any problems found, and a clickable PDF link for every project built.
