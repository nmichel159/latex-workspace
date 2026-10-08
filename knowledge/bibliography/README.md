# Bibliography

How sources are found, verified, recorded and cited. Applies to every project.

## 1. Where things are

| Place | Content | Rule |
|---|---|---|
| [references.bib](references.bib) | canonical bibliography of all projects | every entry has a status line above it; corrections are made here first |
| `projects/<project>/references.bib` | the entries that project cites | copy of the canonical entries; nothing is corrected here separately |
| `projects/cv/publications.bib` | the author's own publications for the CV (biblatex) | consistent with [../author.md](../author.md); not copied from the canonical file |
| [../literature/](../literature/README.md) | reading notes and the search log | evidence for every statement about the literature |
| [../sources/](../sources/README.md) | full texts (PDF and `.txt`) of the author's theses and key sources | named by key or type of work |

## 2. Path of a new citation

1. **Open the primary record:** the publisher's DOI page, DBLP, arXiv, zbMATH; for a book the publisher's catalog.
2. **Copy the data from the record.** Not from memory, not from another paper's reference list, not from a search engine's BibTeX export (they carry wrong pages, years and types).
3. **Write the entry** into `references.bib`, in the right section, with a status line ([section 3](#3-status-line)).
4. **Check that the work contains what the text attributes to it**, with a sentence or page number. For a work the text builds on, write a note in `knowledge/literature/`.
5. **Copy the entry into the project** and cite it.
6. **Run the checker:** `.\scripts\check-bib.ps1 -Project <project>` ([section 10](#10-check-bibps1)).

A value that could not be verified is left out of the entry; a missing field is better than an invented one.

## 3. Status line

A comment directly above every canonical entry, ASCII only (8-bit BibTeX fails on diacritics in comments):

```bibtex
% VERIFIED 2026-10-08 (publisher page, DOI resolves).
% PARTIAL 2026-10-08: authors, title and year verified; pages not.
% TODO: what has to be resolved.
```

| Tag | Form | Meaning |
|---|---|---|
| `VERIFIED` | `% VERIFIED <ISO date> (<where it was checked>)` | every field compared with the primary record on that date |
| `PARTIAL` | `% PARTIAL <ISO date>: <what is and is not verified>` | part of the data verified; the rest is as in the source it was copied from |
| `TODO` | `% TODO: <what>` | known problem |

- Only `VERIFIED` entries go into a manuscript that is submitted. A `PARTIAL` entry is completed first, or its unverified field is dropped.
- Further comment lines (what was corrected, what the source got wrong) follow the status line and stay in the same comment block. One status line per entry.
- Legacy tags `OVERENE` (= `VERIFIED`) and `CIASTOCNE` (= `PARTIAL`) from the first version of the file are accepted. `check-bib.ps1` counts them in one note per file; they are converted when an entry is next touched.

## 4. Key

`Surname` + `Year` + optional keyword: `Bollobas2001`, `Cook1971Complexity`, `GomoryHu1961` (two authors), `RomeraParedes2024FunSearch`. With three or more authors, the first author's surname.

Letters and digits only: ASCII, no spaces, hyphens or colons. Existing keys (`henzinger1997faster`, `itai1979maximum`) are not renamed. In `\cite` the key is written exactly as in the `.bib`, with the same letters in the same case; BibTeX treats keys case-insensitively, so two keys that differ only in case are one key.

## 5. Entry types and required fields

The canonical file uses only the types and fields of classic BibTeX, so an entry works in any template (BibTeX and biblatex). `check-bib.ps1` reports a missing required field as `required` and a missing recommended field as `recommended`.

| Type | Required | Recommended | Note |
|---|---|---|---|
| `@article` | author, title, journal, year, volume, pages | number, doi | full journal name; `pages` may be `eid` or `articleno` |
| `@inproceedings` | author, title, booktitle, year, pages | publisher, doi | `booktitle` in full with the abbreviation in parentheses; LNCS/LIPIcs also `series` and `volume`; an article number instead of pages as `12:1--12:17` |
| `@book` | author or editor, title, publisher, year | isbn | `edition`, `series`, `number` where they exist |
| `@incollection` | author, title, booktitle, publisher, year, pages | editor, doi | a chapter of a volume; cite the chapter, not the volume |
| `@phdthesis`, `@mastersthesis` | author, title, school, year | | `type = {Bachelor's thesis}` for a bachelor's thesis; `address`, `url` |
| `@misc`, preprint | author, title, year, eprint, archivePrefix | primaryClass | only until a published version exists |
| `@misc`, software, data, model, web page | author or organization, title, year, url or howpublished | note | see [section 9](#9-llms-software-and-datasets) |
| `@techreport` | author, title, institution, year | number | |
| `@unpublished` | author, title, note | year | manuscripts in preparation |

Other BibTeX types (`@inbook`, `@proceedings`, `@manual`, `@booklet`) are checked against the BibTeX required fields. Types that exist only in biblatex (`@online`, `@report`, `@thesis`, `@software`, `@dataset`) are not used in the canonical file.

## 6. Writing the fields

- **Names:** `Surname, Given`, joined with `and`; all authors, no `and others`. Diacritics as LaTeX commands in braces: `Bollob{\'a}s`, `Karo{\'n}ski`, `Miche{\v{l}}`, `Erd{\H{o}}s`. An organization in double braces: `{{Google DeepMind}}`. `check-bib.ps1` prints the escape for every non-ASCII character it finds.
- **Title:** exactly as in the published version. Capitals that must stay are protected with braces: `{NP}`, `{LLM}`, `{E}rd{\H{o}}s--{R}{\'e}nyi`, proper names, formulas. Do not put braces around the whole title.
- **Pages:** `151--158` (double hyphen, no spaces); `12:1--12:17` for article numbers.
- **DOI:** bare (`10.1145/800157.805047`), without `https://doi.org/` or `doi:`. **URL:** only when there is no DOI, or for a freely available full text.
- **Preprint and published version:** cite the published one; keep `eprint` in the entry. The key does not change when a preprint becomes a publication unless the year changes; then it is changed in all projects at once.
- **ISBN:** ISBN-13 digits weighted 1, 3, 1, 3, ... sum to a multiple of 10; ISBN-10 digits weighted 10 ... 1 sum to a multiple of 11 (`X` = 10). Every new ISBN is recomputed; several in the original files were invalid.
- **Do not include:** `abstract`, `keywords`, `file`, `month`, `language`, reference-manager fields (`annote`, `timestamp`, `owner`, `groups`, `comment`, `mendeley-*`, `bdsk-*`), and biblatex-only fields (`date`, `journaltitle`, `location`, `urldate`, `eprinttype`, `eprintclass`, `langid`). An access date goes into `note`.

## 7. Sections of `references.bib`

Sections are separated by a comment block of ASCII dashes; a new topic gets a new section. Section titles are in English.

| Section | Content |
|---|---|
| Graphs, algorithms and complexity | textbooks and basic results |
| Cuts, flows and connectivity | |
| Random graphs and probability | including average-case analysis |
| Problems related to Min Cut-Path | work next to the problem of article 1 |
| LLMs and optimization | topic of the dissertation; map in [../research/llm-optimization.md](../research/llm-optimization.md) |
| Experimental methodology | benchmarking, statistics, reporting of experiments |
| Writing and publishing | style guides and publisher rules the guides in `knowledge/writing/` rely on |
| Convex geometry | sources of the bachelor's thesis |
| Author's own work | theses and publications of the author |

## 8. Citing in the text

- Cite the **original source** of a result; a textbook for standard notions.
- The citation stands at the statement it supports, after a non-breaking space: `...minimum cuts~\cite{GomoryHu1961}`.
- A specific theorem or page: `\cite[Theorem~7.3]{Bollobas2001}`.
- A citation is not a noun: *Gomory and Hu~\cite{GomoryHu1961} showed ...*, not *\cite{GomoryHu1961} shows ...*. The sentence must stay correct without the citation; a switch to an author-year style is then mechanical ([../writing/template-porting.md](../writing/template-porting.md) §4).
- Write plain `\cite{...}`; `\citet` and `\citep` only in a project whose template requires an author-year style.
- Several works in one command: `\cite{a,b,c}`; the style orders them.
- Do not cite for the count. A reference the author has not seen is an error.
- The author's own earlier work is cited whenever the text builds on it.
- Software, datasets, benchmarks and language models are cited as sources ([section 9](#9-llms-software-and-datasets)).

## 9. LLMs, software and datasets

Each is a citable item with an entry in the canonical file. If the item has a paper, cite the paper; if it also has a version that the experiments used, add the `@misc` entry for the version.

| Item | Entry | Fields |
|---|---|---|
| language model | `@misc` | `author` = vendor in double braces; `title` = model name; `year` of the release; `url` of the model card or API documentation; `note` = exact model identifier as sent to the API, and the access date |
| software, library, solver | `@misc` | `author` = developers or organization; `title`; `year`; `url`; `note` = version or commit, access date |
| dataset, benchmark | `@misc` | `author`; `title`; `year`; `url`; `doi` if the host issues one; `note` = version, access date |

```bibtex
% TODO: copy the values from the model card, then change this line to VERIFIED.
@misc{VendorYYYYModel,
  author = {{<vendor>}},
  title  = {<model name>},
  year   = {<release year>},
  url    = {<model card or API documentation>},
  note   = {Model identifier <exact API string>, accessed <YYYY-MM-DD>}
}
```

The settings that make a run reproducible (decoding parameters, prompts, dates of the calls, seeds) go into the paper, not into the `.bib`: [../writing/experiments-reporting.md](../writing/experiments-reporting.md) §4. Rules of publishers and venues for citing AI tools: [../writing/submission.md](../writing/submission.md).

## 10. `check-bib.ps1`

Read-only; the exit code is 0 even when there are findings, 2 for invalid parameters.

```powershell
.\scripts\check-bib.ps1 -Project <project> [-Canonical <path>] [-Summary]
.\scripts\check-bib.ps1 -Path <folder> [-Canonical <path>] [-Summary]
.\scripts\check-bib.ps1 -CanonicalOnly [-Canonical <path>] [-Summary]
```

`-Project` takes a folder of `projects/`; `-Path` any folder with `.tex` and `.bib` files (a copy in `tmp/`); `-Canonical` points to another canonical file; `-Summary` prints only the counts. Output line: `file:line: [category] key: message`.

The script finds the `.bib` files from `\bibliography{...}` (BibTeX) or `\addbibresource{...}` (biblatex), reads the keys from all `\cite`-type commands in the `.tex` files (comments ignored; `\nocite{*}` switches the `unused` check off), and compares every project entry with the canonical one.

| Category | Finding | Fix |
|---|---|---|
| `cite-missing`, `cite-case` | a cited key is not in the `.bib`, or differs in case | copy the entry from the canonical file; correct the key |
| `unused` | an entry is never cited | delete it from the project copy |
| `duplicate-key`, `duplicate-doi`, `duplicate-entry` | same key (case-insensitive), DOI, or title and year twice | keep one |
| `canonical-missing`, `canonical-diff` | the entry is not in the canonical file, or a field differs | correct the canonical entry first, then copy it |
| `status` | no status line, a malformed one, a future date, `PARTIAL`/`TODO` in a cited entry | [section 3](#3-status-line) |
| `required`, `recommended` | a field of [section 5](#5-entry-types-and-required-fields) is missing | add it, or accept that the source has none |
| `doi`, `isbn`, `pages`, `year` | DOI with a prefix or implausible syntax, wrong ISBN check digit, page range without `--`, year not four digits | [section 6](#6-writing-the-fields) |
| `non-ascii` | a non-ASCII character in a field or a comment (BibTeX projects and the canonical file); the message gives the escape | use the escape |
| `field`, `biblatex` | a field or type that does not belong; a biblatex-only field or type in a BibTeX project | delete or rename |
| `author`, `title-case`, `key-style` | author list not in `Surname, Given` form or with `and others`; capitals a style may lowercase; a key with characters other than letters and digits | [section 6](#6-writing-the-fields), [section 4](#4-key) |
| `syntax`, `bib-file` | unbalanced braces, a repeated field, an unknown type; a `.bib` file that is missing | fix the file |

A project that loads biblatex (`\addbibresource`, `\printbibliography`) is checked with biblatex rules: UTF-8 and biblatex fields are allowed, no `title-case` or `key-style` findings, and an entry that is not in the canonical file is reported as a note (own entries may stay local).

Run `-CanonicalOnly` after editing `references.bib`, and `-Project` before every build that goes to a co-author or a journal. The checker does not open the network: DOI resolution, page numbers and authorship are verified by hand against the primary record ([section 2](#2-path-of-a-new-citation)).

## 11. Bibliography style

The style (`.bst` or biblatex settings) belongs to the template of the venue and lives in the project. Data in the `.bib` is not changed for a style; if the style does not print the DOI or shortens a title, the style is changed, not the entry. Mechanics (packages, `natbib` options, biber): [../writing/latex-guide.md](../writing/latex-guide.md) §10.

| Document | System |
|---|---|
| article | BibTeX with the style of the template (neutral template: `natbib` + `plainnat`) |
| dissertation | as the university template requires; if it allows a choice, biblatex + biber |
| CV | biblatex + biber, style `ieee`, own file `publications.bib` |
