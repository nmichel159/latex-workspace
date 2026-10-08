---
name: cite-sources
description: Add or check citations and literature (bibliography entries, reading notes, search log) in a project; use for any new reference, related-work statement or novelty claim.
---

# Cite sources

Use this skill when the user asks to add a citation, to check the bibliography, to write or verify related work, or to
support a claim that something is new.

1. **Path of a citation:** `knowledge/bibliography/README.md`, section 2: primary record, entry with a status line in
   the canonical `knowledge/bibliography/references.bib` first, then the copy in `projects/<project>/references.bib`.
2. Never cite from memory. Never invent a field: what the primary record does not confirm is left out and the status
   line says so (`PARTIAL` or `TODO`). A manuscript that is submitted cites `VERIFIED` entries only.
3. A work the text builds on (its theorem, definition, comparison): reading note in `knowledge/literature/`
   (`knowledge/literature/README.md`, "Adding a paper"). A statement about a work rests on its note.
4. A novelty claim ("has not been studied"): search, then a row in `knowledge/literature/searches.md`, also when
   nothing was found. A claim needs a row no older than three months before submission.
5. The sentence that carries the citation: form in `knowledge/bibliography/README.md`, section 8; a related-work
   paragraph: `knowledge/writing/paper-structure.md`, section 6; more than a sentence: skill `academic-writing`.
   Run `.\scripts\check-text.ps1 -Path <changed file>`. Update the topic map in `knowledge/research/`.
6. Run `.\scripts\check-bib.ps1 -Project <project>` (after editing the canonical file also `-CanonicalOnly`).
   Resolve every finding or say why not.
7. Rebuild with `.\scripts\build-project.ps1 -Project <project>`; no `[?]` in the PDF.
8. Report: keys added or changed with their status, what remains `TODO(verify)`, searches logged, and the clickable
   PDF link `[outputs/<project>/<main>.pdf](outputs/<project>/<main>.pdf)`.
