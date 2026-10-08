---
name: academic-writing
description: Write or revise text of a research article or thesis (sections, proofs, abstracts, related work) so it matches the author's notation, terminology and style, using the workspace knowledge base.
---

# Write or revise academic text

Use this skill when the user asks to draft, extend, shorten, translate or proofread a part of an article or a
thesis, or to move material from the thesis into an article.

## Before writing

1. Read `projects/<project>/README.md` and the surrounding source, not only the passage to change.
2. Read, in this order (the "By task" table in `knowledge/README.md` lists the variants):
   - the topic file in `knowledge/research/` (definitions, notation, what is proven where);
   - `knowledge/writing/academic-style.md`, especially section 9 "The author's habits";
   - `knowledge/writing/paper-structure.md` for the part being written (title, abstract, introduction, related work,
     conclusion; thesis to paper: section 13), `knowledge/writing/math-writing.md` for definitions, statements,
     proofs and algorithms, `knowledge/writing/experiments-reporting.md` for experiments;
   - `knowledge/writing/latex-conventions.md` for environments, labels, macros; `knowledge/writing/thesis.md` for
     dissertation text.
3. Exact wording of an existing result: search `knowledge/sources/*.txt`, confirm in the PDF.

## While writing

- Use the document's notation and environment names; no second symbol for the same thing.
- Never change mathematical content silently. A statement that looks wrong: say so, propose the fix separately,
  record it in the project `README.md` under "Known problems".
- A statement about the literature needs a source: skill `cite-sources`.
- Write in the manuscript's own language (English by default) and follow `academic-style.md` section 2.

## After writing

1. Run `.\scripts\check-text.ps1 -Path <changed file>` once per changed file (`-Path` takes one file or folder), or
   `-Path projects\<project>\sections` for the whole folder. Resolve each finding or justify it in the report.
2. Build with `.\scripts\build-project.ps1 -Project <project>` and check for `??` and `[?]`.
3. Update `knowledge/research/*.md` if a result, definition or notation was added or changed, and the project
   `README.md` if the status or "Known problems" changed.
4. Report what was written, open questions for the author, remaining findings with reasons, and the clickable PDF link.
