---
name: create-latex-pdf
description: Start a new LaTeX document (article, thesis, CV, report, letter) from a workspace template and produce its first PDF.
---

# Create a new document

Use this skill when the user asks for a new document.

1. Choose the project name (rules: `knowledge/writing/latex-conventions.md`, section 1).
2. Start from a template in `templates/` (overview: `templates/README.md`):

   | Document | Template |
   |---|---|
   | article | `article-modular` (default) |
   | dissertation | `thesis-modular`, main file `main.tex` |
   | written work for the dissertation exam | `thesis-modular`, main file `exam.tex` (`-MainFile exam.tex`) |
   | CV | `altacv` |
   | article for a venue whose template is in `templates/<venue>/` | `article-modular`, then skill `port-latex-template` |
   | anything else | minimal `main.tex` per `latex-conventions.md`; tell the user which class you chose |

   `new-aiaa` (the former class of article 1, which now uses `els-cas`) only when the owner asks for it.
3. Keep the layout of the template: wrapper `main.tex`, `preamble/`, `sections/` (thesis: `chapters/`),
   `references.bib`, `img/`, class and `.bst` inside the project (`knowledge/writing/latex-conventions.md`, section 1).
4. Article: write the four answers of `knowledge/writing/paper-structure.md` section 1 into the project `README.md`
   ("Intent") before any text. Dissertation: follow `knowledge/writing/thesis.md`.
5. Fill author and affiliation from `knowledge/author.md`. Take definitions and notation from the topic file in
   `knowledge/research/`. Citations: skill `cite-sources`.
6. Write `projects/<project>/README.md` (model: `projects/clanok-1-min-cut-path/README.md`) and add the project
   to the tables in `CLAUDE.md` and the root `README.md`.
7. Build with `.\scripts\build-project.ps1 -Project <project>` and confirm the PDF exists in `outputs/<project>/`.
   Then `.\scripts\package-project.ps1 -Project <project> -CheckOnly`: the folder follows its template and can be
   sent from the first day (`knowledge/writing/latex-conventions.md`, section 1.1).
8. Report the new project path and the clickable PDF link.

Ask about missing content, language, target venue or page format only when it materially affects the document.
