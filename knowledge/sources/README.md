# Zdrojové dokumenty

Pôvodné práce a podklady v PDF. Ku každému PDF je `.txt` s extrahovaným textom (`pdftotext -layout`), v ktorom sa dá hľadať.
Vzorce sú v `.txt` rozsypané – slúži na vyhľadanie miesta, presné znenie čítaj v PDF.

| Súbor | Dokument | Rok | Jazyk | Strán | Prehľad |
|---|---|---|---|---|---|
| `bakalarska-praca-2024-mriezkove-mnohosteny.pdf` | Bakalárska práca *Mrežové mnohosteny v n-rozmernej kocke*, UPJŠ Košice, vedúci Mgr. Martin Vodička | 2024 | SK | 42 | [research/lattice-polytopes.md](../research/lattice-polytopes.md) |
| `diplomova-praca-2025-min-cut-path.pdf` | Diplomová práca *Min Cut-Path*, Univerzita Karlova (MFF), vedúci prof. RNDr. Martin Loebl, CSc. | 2025 | EN | 77 | [research/min-cut-path.md](../research/min-cut-path.md) |

LaTeX zdroje týchto prác v repozitári nie sú (len PDF). Ak sa nájdu, patria do `projects/praca-bakalarska-…` a `projects/praca-diplomova-…`.

## Známe chyby v prácach (errata)

Práce sú odovzdané a v PDF sa nedajú opraviť. Pri preberaní textu do článkov treba tieto miesta opraviť.

**Diplomová práca (2025)** – podrobne v [research/min-cut-path.md](../research/min-cut-path.md), časť 5a:
- Theorem 28 a Claim 29 (koncentrácia stupňov a `c(u,v)` v `(1 ± ε) α log n`) pre pevné `α` neplatia; správne sú konštantné hranice `β₁ log n`, `β₂ log n`.
- Theorem 24: treba `α > 1`.
- NP-ťažkosť je uvádzaná ako otvorený problém – vyriešené v článku 1.
- Bibliografia: 5 neplatných ISBN, Diestel (6. vyd.) má rok 2025, OpenIntro Statistics (4. vyd.) rok 2019 a iné poradie autorov, položka 7 má autorov Blanc, Lange, Qiao, Tan; Roughgarden je editor zborníka.

**Bakalárska práca (2024)**:
- Bibliografia: pri položkách 2, 5 a 6 (časopisecké články) sú uvedené ISBN, ktoré k nim nepatria; položka 2 (Smith, Vamanamurthy) vyšla v roku 1989, nie 2018; mená autorov sú v nesprávnom poradí iniciálok (napr. „A. P. Christian Haase, Benjamin Nill“ = Haase, Nill, Paffenholz).

Overené záznamy oboch prác sú v [bibliography/references.bib](../bibliography/references.bib).

## Pridanie nového zdroja

1. PDF pomenuj `<typ>-<rok>-<tema>.pdf` (malé písmená, pomlčky, bez diakritiky) a ulož sem.
2. Vytvor text:
   ```powershell
   pdftotext -layout -enc UTF-8 knowledge\sources\<nazov>.pdf knowledge\sources\<nazov>.txt
   ```
   Prepínač `-enc UTF-8` je nutný, inak sa stratí diakritika.
3. Doplň riadok do tabuľky vyššie.
4. Ak ide o vlastnú prácu alebo kľúčový zdroj, napíš prehľad do `knowledge/research/`.

## Hľadanie

- Číslované tvrdenia diplomovky: `Definition 30`, `Theorem 22`, `Claim 36`, `Algorithm 8`.
- Číslované tvrdenia bakalárky: `Definícia 2.1.1`, `Veta 4.2.2`.
