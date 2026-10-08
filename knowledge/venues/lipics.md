# LIPIcs series: MFCS, STACS, ESA, WG

Checked 2026-10-08. Each conference sets its own limits every year: re-open the current call before writing.

## Series rules (Dagstuhl Publishing)

| Field | Value |
|---|---|
| Type, publisher | conference proceedings series *Leibniz International Proceedings in Informatics*; Schloss Dagstuhl, open access |
| LaTeX | class `lipics-v2021` (v2021.1.3): [zip](https://submission.dagstuhl.de/styles/download-tag/lipics/v2021.1.3/authors/zip), [releases on GitHub](https://github.com/dagstuhl-publishing/styles/releases); pdfLaTeX; do not change fonts, spacing or colours; no `enumitem`, `paralist`, `wrapfig`; some conferences use the wrapper `socg-lipics-v2021.cls` (line counting) |
| Metadata macros | `\author{Name}{affiliation with city and country}{email}{ORCID}{funding}`, `\authorrunning`, `\Copyright`, `\ccsdesc` (ACM CCS 2012), `\keywords`, `\relatedversion` (persistent URL, e.g. arXiv), `\supplementdetails`, `\funding` |
| Citation style | BibTeX with `\bibliographystyle{plainurl}`; do not change it; no `natbib`, no author-year; no `\nocite{*}`; a `.bbl`-only bibliography is not enough; DOIs or URLs preferred |
| Limits | set by each conference; Dagstuhl recommends about 20 main-text pages for the final version (title page, abstract and bibliography excluded) |
| Figures | at least 300 dpi, preferably PDF; TikZ may be externalised to PDF |
| Licence, fees | CC BY 4.0, authors keep copyright; the conference pays a per-paper fee, authors are not charged |
| AI policy | Dagstuhl GenAI statement: no AI authors; language and formatting help allowed; minor spelling and grammar fixes need no disclosure; any other use disclosed (acknowledgments or before the references: type, purpose, extent of human review; tool, version and date optional); no AI-generated references; reviewers may not use GenAI at all. [submission.md](../writing/submission.md#11-policy-table-checked-2026-10-08) |
| ORCID | optional field in `\author` |

## Conferences

| Conference | Latest call seen | Deadline | Limit | Anonymity | Other |
|---|---|---|---|---|---|
| **STACS 2027** (Göttingen, 2027-03-08 to 12) | [submissions page](https://events.gwdg.de/event/1460/page/476-submissions) | **2026-10-11** 23:59 AoE; rebuttal 2026-11-30 to 12-02; notification 2026-12-22 | 15 pages excluding title page, references, appendix; title page with title and abstract only | lightweight double-blind (track PC sees names, sub-reviewers do not) | EasyChair; tracks A (algorithms, complexity) and B (automata, logic); arXiv posting strongly encouraged; AI: ACM authorship policy plus mandatory detailed disclosure of AI used in the research |
| **MFCS 2026** (Paris, 2026-08-24 to 28); 2027 call not found | [mfcs2026.irif.fr](https://mfcs2026.irif.fr/) | 2026-04-24 (passed) | 12 pages excluding separate title page, references, optional appendix | **not anonymous** (single-blind) | HotCRP; appendix read at PC discretion; up to 10 papers may be presented by video |
| **ESA 2026**; 2027 call not checked | [algo-conference.org/2026/esa](https://algo-conference.org/2026/esa/) | abstract 2026-04-21, paper 2026-04-23 (passed) | **500 lines** of text excluding front matter, references, marked appendix; class `socg-lipics-v2021.cls` | **not anonymous** (single-blind) | tracks A (theory), E (engineering, experiments), S (simplicity); EasyChair; on-site presentation required |
| **WG 2027** (Schloss Schney, 2027-06-15 to 18) | [call](https://www.uni-bamberg.de/en/wg2027/call-for-papers/), [submissions](https://www.uni-bamberg.de/en/wg2027/submissions/) | abstract 2027-01-31, paper 2027-02-05, notification 2027-04-09 | **500 lines** (about 12 pages) by `socg-lipics-v2021.cls` (option `anonymous`), references excluded, appendix unlimited | lightweight double-blind; third-person self-citation | LIPIcs format required (not LNCS); EasyChair link and AI rules "TBA"; arXiv allowed; in-person presentation |

## Fit

Min Cut-Path NP-completeness and polynomial cases: STACS track A, MFCS, WG (graph-theoretic), ESA track A;
an LLM-designed algorithm with an experimental study: ESA track E.
