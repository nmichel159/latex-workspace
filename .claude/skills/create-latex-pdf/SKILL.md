---
name: create-latex-pdf
description: Start a new LaTeX document (article, thesis, CV, report, letter) from a workspace template and produce its first PDF.
---

# Create a new document

Use this skill when the user asks for a new document.

1. Choose the project name: lowercase, hyphens, no diacritics. Articles are `clanok-<n>-<tema>`, theses
   `praca-<typ>-<tema>`, talks `prezentacia-<tema>`.
2. Start from a template in `templates/` (see `templates/README.md`):
   - article: copy `templates/new-aiaa/` to `projects/<project>/`;
   - CV: copy `templates/altacv/`;
   - no fitting template: build a minimal `main.tex` following `knowledge/writing/latex-conventions.md`
     and tell the user which class you chose.
3. Keep the layout uniform: `main.tex`, `references.bib`, images in `img/`, class and `.bst` inside the project.
   Use UTF-8; load Slovak language support when the document is Slovak.
4. Fill in author and affiliation from `knowledge/author.md`. For Min Cut-Path texts take definitions and notation
   from `knowledge/research/min-cut-path.md`, and copy cited entries from `knowledge/bibliography/references.bib`.
5. Write `projects/<project>/README.md` (model: `projects/clanok-1-min-cut-path/README.md`) and add the project
   to the tables in `CLAUDE.md` and the root `README.md`.
6. Build with `.\scripts\build-project.ps1 -Project <project>` and confirm `outputs/<project>/main.pdf` exists.
7. Report the new project path and the clickable PDF link.

Ask about missing content, language, target venue or page format only when it materially affects the document.
