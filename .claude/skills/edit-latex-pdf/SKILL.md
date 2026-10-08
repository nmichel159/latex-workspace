---
name: edit-latex-pdf
description: Change an existing LaTeX document (text, layout, images, citations, styling), rebuild it and hand back a link to the refreshed PDF.
---

# Edit an existing document

Use this skill when the user asks to change something in an existing project.

1. Locate the project in `projects/<project>/`; read its `README.md` and the part of the source to be changed.
2. Make only the source changes the request needs. Follow `knowledge/writing/latex-conventions.md` for new labels,
   macros, file names and citations. Do not rewrite statements, proofs or wording that were not part of the request;
   list what you noticed instead.
3. A substantial change of wording: skill `academic-writing`. A new or changed citation: skill `cite-sources`.
4. Rebuild:

   ```powershell
   .\scripts\build-project.ps1 -Project <project>
   ```

5. Verify the result in `outputs/<project>/`: no errors, no `??` or `[?]`, page count and layout as expected.
   For the CV the document must stay on two pages. If the change added, renamed or moved a file, added a package or
   touched class files, also run `.\scripts\package-project.ps1 -Project <project> -CheckOnly`
   (`knowledge/writing/latex-conventions.md`, section 1.1); never edit a venue's `.cls` or `.bst`.
6. If the change fixes an item listed under "Known problems" in the project `README.md`, remove that item.
7. Report: which file and place changed, anything noticed but left alone, and the clickable PDF link
   `[outputs/<project>/<main>.pdf](outputs/<project>/<main>.pdf)`. Send the PDF with `SendUserFile` when available.
