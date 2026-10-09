# Source documents

Original theses and background material as PDF. Every PDF has a `.txt` with the extracted text (`pdftotext -layout`) that can be searched.
Formulas are scrambled in the `.txt`: use it to locate a passage, read the exact wording in the PDF.

| File | Document | Year | Language | Pages | Overview |
|---|---|---|---|---|---|
| `bakalarska-praca-2024-mriezkove-mnohosteny.pdf` | Bachelor's thesis *Mrežové mnohosteny v n-rozmernej kocke* (Lattice polytopes inside the n-dimensional cube), UPJŠ Košice, supervisor Mgr. Martin Vodička | 2024 | SK | 42 | [research/lattice-polytopes.md](../research/lattice-polytopes.md) |
| `diplomova-praca-2025-min-cut-path.pdf` | Master's thesis *Min Cut-Path*, Charles University (MFF), supervisor prof. RNDr. Martin Loebl, CSc. | 2025 | EN | 77 | [research/min-cut-path.md](../research/min-cut-path.md) |

The LaTeX sources of these theses are not in the repository (PDFs only). If found, they belong in `projects/praca-bakalarska-…` and `projects/praca-diplomova-…`.

## Other material

`Overleaf Projects (1 items) (11).zip` (added by the owner 2026-10-08, file name as exported): an Overleaf export
that holds `CSGT 26.zip`, the beamer talk *Min Cut-Path Problem* (`main.tex`, English, UPJŠ title page) with its
images. Read on 2026-10-09 for the figures of article 1; not unpacked in the repository.

| Images in the talk | Content | Use |
|---|---|---|
| `figures/chain.png`, `chain_link.png`, `Chain_link_example.png`, `chain_threads.png`, `Threading.png` | gadgets of the reduction (draw.io) | byte-identical to the five PNG figures article 1 already had |
| `figures/obrazok_cut-path.png` | schematic cut-path: path (red), cut (blue) | article 1, `cut-path.png` |
| `figures/triedy_zlozitosti_diam_or_cut-2.png` | class diagram: NP, diameter 2, cut 2, diam or cut 2 | not used: the owner decided on 2026-10-09 to keep it out of article 1 for now (a copy is in `archives/removed-from-projects/clanok-1-min-cut-path/2026-10-09-conclusion-figures/`); `figures/triedy_zlozitosti.png` is the same diagram without the class *diam or cut 2* |
| `figures/2-sych.png`, `figures/3-sych.png` | the two 2-synchronization and the two 3-synchronization threads | redrawn in TikZ for article 1 (see below) |
| `example_cut2.png`, `example_diam2.png` (draw.io); `example_cut2c.png`, `example_diam2c.png` (the same with the cut-path in red) | counterexamples in the class *diam or cut 2* (MT Fig. 3.3) | redrawn in TikZ (see below), but not in article 1: the owner decided on 2026-10-09 to keep them out for now; candidates for article 2 |
| `general_square_graph.png`, `Transformation_A.png`, `Transformation_B.png`, `Transformation_C.png` | general square graph and the three transformations of its construction (MT Section 3.3.1) | material for article 2; article 1 does not define these notions |
| the remaining images (`2_cut-path.png`, `vela_cut-path.png`, `general_path.png`, `square_graph.png`, `ISP.png`, logos, photographs) | not used by the talk's `main.tex` | - |

**AI-generated images:** `figures/2-sych.png`, `figures/3-sych.png`, `example_cut2c.png` and `example_diam2c.png`
carry a C2PA manifest in a `caBX` chunk, signed by Google on 2026-06-04, with the actions "Created by Google
Generative AI" and "Applied imperceptible SynthID watermark" (source type `trainedAlgorithmicMedia`). Publishers
restrict such images (`knowledge/writing/submission.md` §1.1), so they do not go into a manuscript; the owner chose
vector redraws in TikZ instead (2026-10-09; sources in `projects/clanok-1-min-cut-path.submission/figures/`).
Check the chunks of any further image from this archive before using it.

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
