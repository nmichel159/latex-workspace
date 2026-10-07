---
name: academic-writing
description: Write or revise text of a research article or thesis (sections, proofs, abstracts, related work) so it matches the author's notation, terminology and style, using the workspace knowledge base.
---

# Write or revise academic text

Use this skill when the user asks to draft, extend, shorten, translate or proofread a part of an article or a
thesis, or to move material from the thesis into an article.

## Before writing

1. Read `projects/<project>/README.md` and the surrounding source, not only the passage to change.
2. Read the knowledge base for the topic:
   - `knowledge/research/min-cut-path.md` for definitions, notation, what is already proven where, and the
     differences between the master thesis and article 1;
   - `knowledge/writing/academic-style.md` for structure, typical phrasing and the checklist;
   - `knowledge/writing/latex-conventions.md` for environments, labels, macros and citations.
3. When exact wording of an existing result is needed, search `knowledge/sources/*.txt` and confirm in the PDF.

## While writing

- Use the document's existing notation and environment names; do not introduce a second symbol for the same thing.
- Text taken from the thesis must be adapted: sections instead of chapters, `Lemma`/`Theorem` naming of the
  article, `CP(u, v)` instead of `cut-path(u, v)`, no references to objects that are not in the article.
- Every theorem gets a proof or a citation. Do not strengthen, weaken or "repair" a mathematical claim silently;
  if a statement looks wrong, say so and propose the fix separately.
- A fact about the literature needs a verified source. Add the entry to `knowledge/bibliography/references.bib`
  first; never invent bibliographic data.
- Write in the document's language (articles: American English, authorial "we", present tense).

## After writing

1. Run the checklist in `knowledge/writing/academic-style.md` on the changed passage.
2. Build with `.\scripts\build-project.ps1 -Project <project>` and check for `??` and `[?]`.
3. Update `knowledge/research/*.md` if a result, definition or notation was added or changed, and the project
   `README.md` if the status or the list of known problems changed.
4. Report what was written, open questions for the author, and the clickable PDF link.
