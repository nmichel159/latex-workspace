---
name: review-latex-pdf
description: Compile a LaTeX project, inspect the log and the PDF, and report actionable source-side problems together with a link to the PDF.
---

# Review a document

Use this skill when the user asks whether a project compiles, wants a PDF checked, or reports a build error.

1. Locate the project in `projects/<project>/` and read its `README.md`.
2. Build with `.\scripts\build-project.ps1 -Project <project>`.
3. Read `outputs/<project>/<main>.log` and the `.blg`:
   - fatal errors and missing files;
   - missing packages (`File 'x.sty' not found`): ask before installing, then use `-InstallMissing`;
   - undefined references and citations, duplicate labels;
   - bibliography warnings (missing fields, key case mismatch).
4. Look at the PDF itself when layout is in question: render pages with
   `pdftoppm -r 80 -png outputs\<project>\<main>.pdf tmp\<project>-preview` and read the images.
5. For article or thesis text, go through the checklist in `knowledge/writing/academic-style.md`.
6. Fix source-side problems that are within the request and rebuild. Record the rest in the project `README.md`
   under "Známe problémy" with line numbers.
7. Report material findings only; overfull-box warnings matter only when they visibly damage the layout.
   End with the clickable PDF link `[outputs/<project>/<main>.pdf](outputs/<project>/<main>.pdf)`.
