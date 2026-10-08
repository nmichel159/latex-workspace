# Mriežkové mnohosteny v n-rozmernej kocke – prehľad bakalárskej práce

Zdroj: *Mrežové mnohosteny v n-rozmernej kocke*, bakalárska práca, UPJŠ Košice 2024, vedúci Mgr. Martin Vodička,
42 strán, po slovensky. Plný text: `knowledge/sources/bakalarska-praca-2024-mriezkove-mnohosteny.txt`.

Anglický názov v zadaní: *Lattice polytopes inside n-dimensional cube*.
Kľúčové slová: mriežka, báza mriežky, konvexné mnohosteny, Stred-mnohosten, skosený mnohosten, zmiešaný objem.

## Téma

Objemy konvexných mnohostenov, ktorých vrcholy ležia vo vrcholoch `n`-rozmernej kocky: priemerný objem
náhodného mnohostena, objem konvexnej kombinácie dvoch mnohostenov a extrémne (maximálne a minimálne) objemy.

## Štruktúra a hlavné výsledky

| Kapitola | Obsah | Kľúčové tvrdenia |
|---|---|---|
| 1 Základy | mriežkový mnohosten, vrchol, mriežková báza, izomorfizmus, objem cez determinant; gama funkcia, Stirlingov vzťah, objem ihlana a gule | Veta 1.2.7: `V(M) ≤ ∏\|m₀ − mᵢ\| / n!` pre simplex |
| 2 Priemerný objem mnohostena v kocke | Stred-mnohosten `M_{n,k}` (vrcholy so súradnicami 0, 1, 0.5; práve `k` súradníc je 0.5) | Veta 2.1.2: `M_{n,k+1} ⊆ M_{n,k}`; Veta 2.2.1: ak každý vrchol kocky vyberieme nezávisle s pravdepodobnosťou `p ∈ (0,1)`, tak `E[V(conv A)] → 1` pre `n → ∞` |
| 3 Zmiešaný objem a konvexné kombinácie | Minkowského súčet, zmiešaný objem, skosený mnohosten (ihlan) | Veta 3.0.4: `c_k² ≥ c_{k−1}·c_{k+1}`; Veta 3.1.1: objem `conv(M, O)` nie je zhora ohraničený; Veta 3.2.2: vzorec pre objem skoseného mnohostena; Veta 3.4.1: minimálny objem `conv(M, N)` medzi rovnobežnými nadrovinami je objem skoseného ihlana |
| 4 Extrémne objemy v kocke | maximum pri `k` vrcholoch, maximum pre simplex (súvis s Hadamardovým problémom maximálneho determinantu), minimum | Veta 4.1.1: pre `k ≥ 2^{n−1}` je `V ≤ 1 − (2ⁿ − k)/n!`; Veta 4.2.2: `V(M) ≤ √(n+1)^{n+1} · 0.5ⁿ / n!` pre simplex, rovnosť len ak `n + 1 = 4k`; Veta 4.2.3: konštrukcia extrémneho simplexu v dimenzii `2n + 1`; Hypotéza o rekurencii `D(n, m)` pre minimálne objemy; Veta 4.3.3: priemer minimálnych objemov `→ 1 + ln(1/2)` |

Poznámka: vzorce v tabuľke sú prepísané z extrahovaného textu, kde sa sadzba zlomkov a odmocnín rozpadá. Pred citovaním
over presné znenie v PDF (`knowledge/sources/bakalarska-praca-2024-mriezkove-mnohosteny.pdf`).

## Terminológia zavedená v práci

| SK | EN (abstrakt) |
|---|---|
| mriežkový mnohosten | lattice polytope |
| Stred-mnohosten | centre-polytope |
| skosený mnohosten / sklonený ihlan | truncated polyhedron |
| zmiešaný objem | mixed volume |
| minimálny rozdielový odhad `D(n, m)` | – |

## Literatúra práce

Správne údaje (overené 7. 10. 2026, ak nie je uvedené inak); čo je v PDF inak, je v poslednom stĺpci.

| # | Zdroj | V PDF práce chybne |
|---|---|---|
| 1 | Haase, Nill, Paffenholz: *Lecture Notes on Lattice Polytopes*, preprint TU Darmstadt, 2020 (neoverované) | poradie mien („A. P. Christian Haase, Benjamin Nill“) |
| 2 | Smith, Vamanamurthy: *How Small Is a Unit Ball?*, Mathematics Magazine 62(2), 1989, 101–107 | rok 2018, uvedené ISBN |
| 3 | Gubner: *The Gamma Function and Stirling's Formula*, poznámky, 2021 (neoverované) | – |
| 4 | Martini, Montejano, Oliveros: *Bodies of Constant Width*, Birkhäuser 2019, ISBN 978-3-030-03866-3 (e-kniha 978-3-030-03868-7) | poradie mien |
| 5 | Stein: *A Note on the Volume of a Simplex*, The American Mathematical Monthly 73(3), 1966 (strany neoverené) | uvedené ISBN |
| 6 | Hedayat, Wallis: *Hadamard Matrices and Their Applications*, The Annals of Statistics 6(6), 1978, 1184–1238, DOI 10.1214/aos/1176344370 | poradie mien, uvedené ISBN |
| 7 | Weisstein: *Hadamard's Maximum Determinant Problem*, MathWorld (neoverované) | – |

Overené záznamy sú v `knowledge/bibliography/references.bib` (časť „Konvexná geometria“).

## Súvis s ďalšou prácou

Tematicky je bakalárka samostatná (konvexná geometria); s Min Cut-Path ju spája len spoločný aparát:
pravdepodobnostné odhady a limitné správanie pre `n → ∞`.
