---
name: new-latex-project
description: Scaffold an empty LaTeX project folder with the workspace's standard layout, without writing document content.
---

# Scaffold a project

Use this skill when the user wants only the structure prepared (for example before pasting their own text or
importing sources). For a document with content, use `create-latex-pdf`.

When creating a project named `<name>` (naming: `knowledge/writing/latex-conventions.md`, section 1):

1. Copy the matching template into `projects/<name>/`: article -> `templates/article-modular`; dissertation or
   dissertation-exam work -> `templates/thesis-modular`; CV -> `templates/altacv`. Without a fitting template create
   `main.tex`, `references.bib` and `img/`.
2. Keep class files, `.bst`, images and local configuration inside the project, venue files unmodified, so it stays
   self-contained and sendable (invariant: `knowledge/writing/latex-conventions.md`, section 1.1).
3. Do not put generated files (`.pdf`, `.log`, `.aux`, `.bbl`, `.bcf`, `.fls`, `.synctex.gz`) in the project;
   they belong to `outputs/<name>/`.
4. Write `projects/<name>/README.md` and add the project to the tables in `CLAUDE.md` and the root `README.md`.
5. Build once with `.\scripts\build-project.ps1 -Project <name>` to prove the scaffold compiles (dissertation exam
   work: add `-MainFile exam.tex`), then run `.\scripts\package-project.ps1 -Project <name> -CheckOnly`.
6. Report the folder and the clickable link `[outputs/<name>/<main>.pdf](outputs/<name>/<main>.pdf)`.
