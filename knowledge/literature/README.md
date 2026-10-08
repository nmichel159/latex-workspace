# Literature notes

What we actually read in other people's papers and what we use from it. Every claim a manuscript makes about the
literature traces to a note with a location in the source; related-work comparisons are never written from memory.

## Files

| File | Contents |
|---|---|
| `<BibKey>.md` | note on one paper; the file name is its key in [../bibliography/references.bib](../bibliography/references.bib) |
| [searches.md](searches.md) | log of literature searches: date, source, query, what was found |
| [_template.md](_template.md) | template for a note |
| `../sources/papers/<BibKey>.pdf` | full text, if the author supplied it (+ `.txt` from `pdftotext`) |
| `../research/<topic>.md` | topic map: how papers group, what is known, what is open |

Write a note for every paper a text relies on (uses its theorem, compares against it, adopts its definition).
A paper cited only for a standard notion needs no note.

## Notes in this folder

All notes below belong to the map [../research/llm-optimization.md](../research/llm-optimization.md); all were written 2026-10-08.

| Note | Topic | Reading status |
|---|---|---|
| [RomeraParedes2024FunSearch.md](RomeraParedes2024FunSearch.md) | FunSearch: evolutionary program search with an LLM | main text and Methods |
| [Liu2024EoH.md](Liu2024EoH.md) | EoH: co-evolving thoughts and code | sections 1-6 |
| [Ye2024ReEvo.md](Ye2024ReEvo.md) | ReEvo: reflective evolution, LLM as hyper-heuristic | sections 3-8, Appendix C |
| [Zhang2024EvolutionarySearch.md](Zhang2024EvolutionarySearch.md) | critical study: is the evolutionary search needed? | sections 1-5, Appendices A-B |
| [Sim2025BeyondHype.md](Sim2025BeyondHype.md) | critical study: LLM-evolved bin-packing heuristics vs. classical rules | full text |
| [Gideoni2026SimpleBaselines.md](Gideoni2026SimpleBaselines.md) | critical study: simple baselines vs. code evolution | sections 1-7 |

## Rules

- Write in your own words; at most one verbatim quotation, short, with its page or section.
- Give every result a **location in the source** (Theorem 3.2, p. 14) and every note a **reading status**
  (full / parts / abstract only). Take no precise claim into a manuscript from a paper read only as an abstract.
- Record notation or definitions that differ from ours explicitly; this is the most common source of errors when a result is reused.
- "Difference from our work": one or two English sentences, reusable in a Related work section.
- A novelty claim in a manuscript (*has not been studied*) needs an entry in [searches.md](searches.md) no older than three months before submission.
- Mark unverified facts `TODO(verify)`.

## Adding a paper

1. Entry in `references.bib` following [../bibliography/README.md](../bibliography/README.md).
2. If a PDF is available: `knowledge/sources/papers/<BibKey>.pdf` and its text via `pdftotext -layout -enc UTF-8`.
3. Note `<BibKey>.md` from the template.
4. Update the topic map `knowledge/research/<topic>.md` (where the paper belongs, what it changes).
