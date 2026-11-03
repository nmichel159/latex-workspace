# Presentations (one collection)

All talks live in `projects/prezentacie/`, so that many talks do not mean many projects. This file is the only notes
file of the collection and its index; a talk has no notes file and no row in `CLAUDE.md` or the root `README.md`.
Rules for slides and the author's style: [knowledge/writing/presentations.md](../knowledge/writing/presentations.md).

## Layout

```
projects/prezentacie/
  ukazky/                                samples from the owner; reference only
  predmety/<course>/<talk>/              course talks, e.g. predmety/grafy/01-uvod/
  konferencie/<conference-year>/<talk>/  e.g. konferencie/csgt-2026/min-cut-path/
  seminare/<seminar>/<talk>/             research seminars
  ostatne/<group>/<talk>/                the rest, e.g. ostatne/phd/semester-3/
```

Except for `ostatne/phd/semester-3`, these example names are illustrations, not existing talks. Every talk sits at
exactly this depth, with lowercase ASCII names and hyphens; `package-project.ps1` accepts no other path. A talk folder
is flat and self-contained: `main.tex`, `references.bib`, figures. A figure used in two talks is copied, so that
changing one talk never changes another, and the look of the template can evolve without touching finished talks.

## Talks

| Talk (path below `projects/prezentacie/`) | What | Status |
|---|---|---|
| `ostatne/phd/semester-3` | PhD progress report after the reports of January and June 2026; about 20 minutes, 18 frames | fourth version of 2026-11-03, after the owner's notes and email; red `TODO(verify)` remains for the date only |

Samples in `ukazky/` (unpacked; original zips in `archives/prezentacie-ukazky/`): `phd-1-semester`, `phd-2-semester`,
`csgt-26`. They build as copies in `tmp/`; never edited.

## ostatne/phd/semester-3

"Semester 3" is inferred from the dates of the two earlier reports; TODO(verify) with the owner, with the date.

Time plan, 20 minutes:

| Part | Frames | Minutes |
|---|---|---|
| Title, Contents | 2 | 1 |
| Study and Teaching Activities | 2 | 2 |
| Supervision and Consulting | 1 | 2 |
| Collaboration with the Hospital | 4 | 7 |
| Research: Min Cut-Path | 2 | 3 |
| Research: LLMs for Optimization | 3 | 3 |
| Conferences and Events | 1 | 1 |
| Future Plans, References, Thank You | 3 | 1 |

The owner supplies what is printed in red: the date.

Sources of the hospital frames, all in the repository `Documents/scheduling`: `backend/app/services/schedule_generation_model.md`
(model, measured improvements), `ILP_SCHEDULE_AUDIT_REPORT.md` (21 consecutive pairs, 23/13/13/13), `SCHEDULER_TEST_REPORT.md`
of 2026-10-02 (validation), `CLAUDE.md` and the commits of 2026-10-28/29 (deployment). The test report predates the later
changes of the model.

Sources of the LLM frames: the owner's email to the supervisor (pasted 2026-11-03); its six sources are the only citations
of the deck (owner's request). LLM-A* advising once is checked in Algorithm 1, line 2, of `Meng2024LLMAStar`.

Sources of the other frames: the owner's notes of 2026-11-02 and 2026-11-03 (all six courses passed, coursework finished in
the summer semester 2025/26; Python and Project in Data Analysis II; master's thesis of Bc. Kiara Koščová, defense
expected 2028), and (defense, new master's thesis, same course, two articles,
Claude, Researchers' Night). Course name and details from the sample `phd-1-semester`, the winter course. Budapest: program
"V4AI in HE - Budapest workshop", preliminary plan, and the owner's train tickets (out 20 October, back 21 October, 16:25).
Research: abstract of article 1, intent table in `projects/clanok-2-min-cut-path.md`. Figure `obrazok_cut-path.png` from the
sample `csgt-26`. The four figures of the first version are in
`archives/removed-from-projects/prezentacie-ostatne-phd-semester-3/`.

## Known problems

- Article 2 was written by an AI assistant and the owner has not read it (notes of that project); the frame on the articles
  states its results.
- The frame "Related Ideas in the Literature" of the hospital part was removed on 2026-11-03, because only the sources of
  the owner's email are cited; its three rostering sources stay in the canonical `.bib`.
- The defense date on the frame, June 2026, comes from the date planned in the sample `phd-2-semester` (18.6.2026).
- `package-project.ps1` also reports `FAIL (trace)` for the word "Claude" on the frame "Two Articles". It is requested text;
  the check does not apply unless the deck is sent as a package.
- Sample `phd-2-semester`, references: FunSearch is cited as no. 7996, pp. 768-775; the canonical entry, checked in the
  Crossref DOI record, has no. 7995, pp. 468-475. The new deck uses the canonical entry.
- Same sample: DASH (`arXiv:2601.20868`) and G-LNS (`arXiv:2602.08253`) are not in the canonical `.bib`, so the new deck
  does not cite them until they are verified.
- Same sample: "All current methods focus on global rules" is a claim about the whole literature with no reading note
  and no logged search; `knowledge/research/llm-optimization.md` lists `Ke2026ASRO`, which targets overfitting to fixed
  instances. The new deck does not repeat the claim.
- `package-project.ps1` reports `FAIL (trace)` on the deck while it holds `TODO`; this ends when the date is filled.
