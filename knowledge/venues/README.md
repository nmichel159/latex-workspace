# Venues

One card per venue or series. A card lists what the venue publishes about itself on a given day; it is a candidate
list, not a recommendation. Which venue suits a manuscript is decided from the manuscript
([paper-structure.md](../writing/paper-structure.md)) and from [../author.md](../author.md).

## Rules

1. **Cards are dated snapshots; re-check before use.** Every card carries a "Checked" date. Only the card of a venue
   that is being chosen or submitted to is kept current: if its date is older than one month, or the venue is a
   conference (limits, dates, anonymity and AI rules change every year), open the listed URLs again and update the
   card first, then write. Cards of other venues are not refreshed; a new card is written when a venue becomes a candidate.
2. A fact without a page read on the checked date is `TODO(verify)`; do not turn it into a statement. A conflict
   between two pages of one publisher is written down as a conflict.
3. Cards hold constraints only: scope in own words, publisher, submission system, class and download URL, citation
   style, limits, anonymity, supplementary rules, source files, OA model and fees, AI policy (linked to the row in
   [../writing/submission.md](../writing/submission.md#11-policy-table-checked-2026-10-08)), review time only if the
   venue states it, URLs.
4. Moving a manuscript into a card's template: [../writing/template-porting.md](../writing/template-porting.md).
   Submission package, cover letter, response to reviewers, preprints and licenses:
   [../writing/submission.md](../writing/submission.md). Final tick list: [../writing/checklist.md](../writing/checklist.md).
5. Never install a class to test a card. A class missing from MiKTeX (journal classes, `acmart`, `IEEEtran`) reaches a
   project as the publisher's download from the page the venue's guide links, fetched with the owner's consent (or
   dropped into `inbox/` by the owner), archived and recorded in `templates/SOURCES.tsv` (skill `process-inbox`;
   [../writing/template-porting.md](../writing/template-porting.md) §1); the card records the download URL.
6. A card gives the packager its switches ([../writing/latex-conventions.md](../writing/latex-conventions.md) §1.1):
   *LaTeX* names the folder `templates/<name>/` once the template has arrived (`-Template`), *Limits* the page limit
   (`-MaxPages`), *Source files* whether the submission system builds from one directory (`-Flat`). A field that
   does not answer this is `TODO(verify)`, not a guess.

## Comparison (checked 2026-10-08)

Limits are the venue's own numbers; "none" means none stated on the pages read. Fees are list prices from the
cited page, without taxes.

| Venue | Type | Publisher | Template / class | Citation style | Limit | OA model | Matches |
|---|---|---|---|---|---|---|---|
| [Discrete Applied Mathematics](discrete-applied-mathematics.md) | journal | Elsevier | `els-cas-templates` (`cas-sc`, `templates/els-cas/`), `elsarticle` | alphabetical, then numbered | Note at most 10 pages; Contribution above 10; abstract 250 words | hybrid, APC USD 3460, CC BY, CC BY-NC or CC BY-NC-ND | Min Cut-Path (algorithms, complexity); target of article 1, ported 2026-10-08 |
| [Theoretical Computer Science](theoretical-computer-science.md) | journal | Elsevier | same | numbered | none; abstract 250 words | hybrid, APC USD 3190, CC BY, CC BY-NC or CC BY-NC-ND | complexity; section Natural Computing |
| [Information Processing Letters](information-processing-letters.md) | journal | Elsevier | same | numbered | about 9 pages; highlights required | hybrid, APC USD 2880, CC BY, CC BY-NC or CC BY-NC-ND | one short result |
| [Journal of Graph Theory](journal-of-graph-theory.md) | journal | Wiley | Wiley NJD / `WileyDesign` | numbered, alphabetical | none; no footnotes | hybrid, fee TODO(verify) | structural and algorithmic graph results |
| [Networks](networks.md) | journal | Wiley | same | numbered, alphabetical | none; six keywords or more | hybrid, fee TODO(verify) | network optimization with algorithms |
| [Algorithmica](algorithmica.md) | journal | Springer | `sn-jnl` (`templates/sn-jnl/`), option `sn-mathphys-num` (inferred) | numbered | none; abstract 150-250 words, 4-6 keywords | hybrid, APC EUR 2790 / USD 3390 / GBP 2490 | algorithms, experimental algorithmics; target of article 2, template prepared 2026-10-08 |
| [Discussiones Mathematicae Graph Theory](discussiones-mathematicae-graph-theory.md) | journal | Univ. of Zielona Gora | `dmgt` (after acceptance) | `\bibitem` | 30 pages requested | no APC | structural graph theory |
| [Discrete Mathematics & Theoretical Computer Science](dmtcs.md) | journal | Episciences | `dmtcs_episciences` (after acceptance) | TODO(verify) | none | no fees, CC BY | discrete mathematics, theory |
| [Journal of Combinatorial Optimization](journal-of-combinatorial-optimization.md) | journal | Springer | `svjour3`, `smallextended` | author-year | none; abstract 150-250 words | hybrid, APC EUR 2790 / USD 3390 / GBP 2390 | combinatorial optimization, ML-based design |
| [Mathematical Programming Computation](mathematical-programming-computation.md) | journal | Springer | `svjour3`, `smallextended` | numbered | none; software required | hybrid, APC EUR 2590 / USD 3390 / GBP 2290 | computational optimization with code |
| [INFORMS Journal on Computing](informs-joc.md) | journal | INFORMS | INFORMS style files (`JOC-template.tex`) | author-year | 25 pages plus 10 appendix; 12 pt, 1.5 spacing | INFORMS Open Option USD 3150 | LLM optimization with code and data |
| [IEEE Trans. on Evolutionary Computation](ieee-tevc.md) | journal | IEEE CIS | `IEEEtran` | IEEE numbered | 10 pages (15 maximum) with over-length charge | hybrid, APC USD 2800 | evolutionary search |
| [ACM TELO](acm-telo.md) | journal | ACM | `acmart` `acmsmall` | author-year | none; 30 pages expected | open access, APC USD 950 / 1450 (2026) | evolutionary and LLM-guided search |
| [Evolutionary Computation](evolutionary-computation.md) | journal | MIT Press | TODO(verify) | TODO(verify) | TODO(verify) | hybrid, conversion fee USD 1800 | evolutionary computation |
| [LIPIcs series](lipics.md): STACS, MFCS, ESA, WG | conference | Dagstuhl | `lipics-v2021` | `plainurl` | 12-15 pages, ESA and WG 500 lines | open access, CC BY, no author fee | graph algorithms and complexity |
| [LNCS series](lncs.md): SOFSEM, IWOCA | conference | Springer | `llncs` | MathPhySci / `splncs04` | 12 pages | not covered by institutional agreements | combinatorial algorithms |
| [GECCO](gecco.md) | conference | ACM SIGEVO | `acmart` `sigconf` | ACM format | 8 pages plus references | ACM open access, APC | LLM-guided evolutionary search |
| [NeurIPS](neurips.md) | conference | NeurIPS | year's style file | style package | 9 pages plus references | proceedings online, license TODO(verify) | LLM-driven optimization |
| [ICML](icml.md) | conference | PMLR | `icml2026` style | style package | 8 pages plus references | PMLR proceedings | LLM-driven optimization |
| [ICLR](iclr.md) | conference | OpenReview | `iclr-2027-style-files` | style package | 9 pages plus references | OpenReview, public | LLM-driven optimization |

## Reading the table for this workspace

- Constraints that change the manuscript, not only the template: IPL page limit and required highlights; IJOC
  single-column 12 pt with a 25-page cap and a cover letter naming IJOC papers; MPC and IJOC release of code;
  double-anonymous venues (TEVC, TELO, GECCO, NeurIPS, ICML, ICLR) forbid author names and affiliations in the
  submitted file, and most also remove the acknowledgments (see the cards).
- Classes not installed in MiKTeX on 2026-10-08: `elsarticle`, `acmart`, `IEEEtran`, `llncs`, `lipics-v2021`,
  `svjour3`, the INFORMS and Wiley classes, `dmgt`. `sn-jnl` is filed as the template `templates/sn-jnl/` and builds
  from a project folder after the MiKTeX package installs of 2026-10-08 (`threeparttable`, `jknappen`, `ncctools`);
  `svjour3` is still not installed.
- Conference calls seen on 2026-10-08 are mostly for 2026-2027 editions; their deadlines for 2027-2028 are
  `TODO(verify)` until the next call appears. STACS 2027 closes 2026-10-11.

## Card template

Copy an existing card and keep the field order: Scope, Type and publisher, Submission system, LaTeX, Citation style,
Limits, Anonymity, Supplementary or appendix, Source files, Prior publication, ORCID, OA and fees, Self-archiving,
AI policy, Review time, Fit, Sources.
