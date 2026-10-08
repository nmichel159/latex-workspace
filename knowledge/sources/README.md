# Source documents

Original theses and background material as PDF. Every PDF has a `.txt` with the extracted text (`pdftotext -layout`) that can be searched.
Formulas are scrambled in the `.txt`: use it to locate a passage, read the exact wording in the PDF.

| File | Document | Year | Language | Pages | Overview |
|---|---|---|---|---|---|
| `bakalarska-praca-2024-mriezkove-mnohosteny.pdf` | Bachelor's thesis *Mrežové mnohosteny v n-rozmernej kocke* (Lattice polytopes inside the n-dimensional cube), UPJŠ Košice, supervisor Mgr. Martin Vodička | 2024 | SK | 42 | [research/lattice-polytopes.md](../research/lattice-polytopes.md) |
| `diplomova-praca-2025-min-cut-path.pdf` | Master's thesis *Min Cut-Path*, Charles University (MFF), supervisor prof. RNDr. Martin Loebl, CSc. | 2025 | EN | 77 | [research/min-cut-path.md](../research/min-cut-path.md) |

The LaTeX sources of these theses are not in the repository (PDFs only). If found, they belong in `projects/praca-bakalarska-…` and `projects/praca-diplomova-…`.

## Known errors in the theses (errata)

The theses are submitted and cannot be corrected in the PDF. Correct these places when reusing text in articles.

**Master's thesis (2025)** – details in [research/min-cut-path.md](../research/min-cut-path.md), Section 5a:
- Theorem 28 and Claim 29 (concentration of degrees and of `c(u,v)` in `(1 ± ε) α log n`) do not hold for fixed `α`; the correct bounds are the constants `β₁ log n`, `β₂ log n`.
- Theorem 24: `α > 1` is required.
- NP-hardness is stated as an open problem – solved in article 1.
- Bibliography: 5 invalid ISBNs, Diestel (6th ed.) is dated 2025, OpenIntro Statistics (4th ed.) 2019 with a different author order, entry 7 has authors Blanc, Lange, Qiao, Tan; Roughgarden is the editor of a collected volume.

**Bachelor's thesis (2024)**:
- Bibliography: entries 2, 5 and 6 (journal articles) carry ISBNs that do not belong to them; entry 2 (Smith, Vamanamurthy) appeared in 1989, not 2018; author names have the initials in the wrong order (e.g. "A. P. Christian Haase, Benjamin Nill" = Haase, Nill, Paffenholz).

Verified entries for both theses are in [bibliography/references.bib](../bibliography/references.bib).

## Adding a new source

1. Name the PDF `<type>-<year>-<topic>.pdf` (lowercase, hyphens, no diacritics) and store it here.
2. Create the text:
   ```powershell
   pdftotext -layout -enc UTF-8 knowledge\sources\<name>.pdf knowledge\sources\<name>.txt
   ```
   The `-enc UTF-8` switch is required, otherwise diacritics are lost.
3. Add a row to the table above.
4. For the author's own work or a key source, write an overview into `knowledge/research/`.

## Searching

- Numbered statements of the master's thesis: `Definition 30`, `Theorem 22`, `Claim 36`, `Algorithm 8`.
- Numbered statements of the bachelor's thesis (Slovak text; *Definícia* = definition, *Veta* = theorem): `Definícia 2.1.1`, `Veta 4.2.2`.
