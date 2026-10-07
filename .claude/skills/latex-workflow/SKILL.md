---
name: latex-workflow
description: Shared rules for any LaTeX task in this workspace - where sources, outputs and knowledge live, how to build, and how to report the result with a PDF link.
---

# LaTeX project workflow

Use this skill whenever a task creates, edits, compiles or diagnoses a LaTeX document in this workspace.
`CLAUDE.md` is the authority; this is the short operational version.

1. Find the project in `projects/<project>/` and read its `README.md` (main file, status, known problems).
   The project registry is the table in `CLAUDE.md`.
2. For article or thesis text, read the knowledge base first: `knowledge/README.md` routes to the right file.
3. Edit only inside `projects/<project>/`. Never edit `outputs/`. Never delete a user file; move it to
   `archives/removed-from-projects/<project>/`.
4. Build from the workspace root:

   ```powershell
   .\scripts\build-project.ps1 -Project <project>
   ```

   Add `-MainFile <file.tex>` only when the project has several candidate main files.
5. If the build stops with `File 'x.sty' not found`, a MiKTeX package is missing. Ask the user before installing,
   then rebuild with `-InstallMissing`.
6. Check the log for errors, undefined references and citations; open the PDF when layout matters.
7. End the reply with a clickable link to the PDF, `[outputs/<project>/<main>.pdf](outputs/<project>/<main>.pdf)`,
   and send the file with `SendUserFile` when available. This is required after every change.
