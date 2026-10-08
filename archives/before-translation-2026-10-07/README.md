# LaTeX workspace

Pracovný priestor na písanie článkov, záverečných prác a CV. Každý dokument má vlastný priečinok so zdrojmi,
všetko sa kompiluje jedným skriptom a k písaniu je pripravená znalostná báza.

## Projekty

| Projekt | Dokument | Hlavný súbor | PDF | Stav |
|---|---|---|---|---|
| [cv](projects/cv/README.md) | životopis (AltaCV, EN) | `norbert-michel-cv.tex` | [outputs/cv/norbert-michel-cv.pdf](outputs/cv/norbert-michel-cv.pdf) | kompiluje sa (2 strany) |
| [clanok-1-min-cut-path](projects/clanok-1-min-cut-path/README.md) | článok *Min Cut-Path Problem* (EN) | `main.tex` | [outputs/clanok-1-min-cut-path/main.pdf](outputs/clanok-1-min-cut-path/main.pdf) | po korektúre a štylistickej revízii, kompiluje sa bez varovaní (23 strán); obsahové zmeny čakajú na kontrolu autora; šablóna časopisu neskôr |
| [clanok-2-min-cut-path](projects/clanok-2-min-cut-path/README.md) | článok 2 – bude sa pripravovať z diplomovej práce | – | – | prázdny, čaká na LaTeX zdroj diplomovky |

## Štruktúra

```
projects/     zdrojové súbory, jeden priečinok = jeden dokument (tu sa upravuje)
outputs/      vygenerované PDF a pomocné súbory (needitovať, každá kompilácia ich prepíše)
knowledge/    znalostná báza: autor, výskum, konvencie, bibliografia, pôvodné práce v PDF + text
templates/    čisté šablóny pre nové projekty (článok new-aiaa, CV AltaCV)
inbox/        sem patrí všetko nové a nespracované (zipy, PDF, šablóny)
archives/     pôvodné zipy a súbory odložené z projektov
scripts/      build-project.ps1 – jediný spôsob kompilácie
tmp/          dočasné súbory (náhľady strán), dá sa kedykoľvek zmazať
installers/   inštalátory MiKTeX a Strawberry Perl
.latex-tools/ prenosná záložná kópia MiKTeX + Perl (na PATH je až za inštaláciou zo scoop)
.claude/      skilly pre Claude Code
CLAUDE.md     pravidlá pre Claude Code
```

## Kompilácia

Z koreňového priečinka v PowerShelli:

```powershell
.\scripts\build-project.ps1 -Project cv
```

```powershell
.\scripts\build-project.ps1 -Project clanok-1-min-cut-path
```

- Hlavný súbor sa nájde sám (`main.tex`, inak jediný `.tex` s `\documentclass`); dá sa zadať cez `-MainFile`.
- Výsledok je v `outputs/<projekt>/`; skript na konci vypíše cestu k PDF.
- Ak chýba LaTeX balík, kompilácia hneď skončí chybou. S prepínačom `-InstallMissing` si ho MiKTeX stiahne sám.

## Nový dokument

1. Skopíruj šablónu: `Copy-Item -Recurse templates\new-aiaa projects\clanok-2-<tema>`.
2. Názov projektu: malé písmená a pomlčky (`clanok-<n>-<tema>`, `praca-<typ>-<tema>`).
3. Skompiluj a doplň riadok do tabuľky projektov tu a v `CLAUDE.md`.

Podrobné pravidlá (názvy súborov, preambula, labely, citácie): [knowledge/writing/latex-conventions.md](knowledge/writing/latex-conventions.md).

## Znalostná báza

Vstupný bod: [knowledge/README.md](knowledge/README.md).

| Čo | Kde |
|---|---|
| Autor, afiliácie, školitelia, plánované publikácie | [knowledge/author.md](knowledge/author.md) |
| Min Cut-Path: definície, notácia, mapa výsledkov, otvorené problémy, slovník | [knowledge/research/min-cut-path.md](knowledge/research/min-cut-path.md) |
| Bakalárska práca (mriežkové mnohosteny) | [knowledge/research/lattice-polytopes.md](knowledge/research/lattice-polytopes.md) |
| Štýl odborného textu a kontrolný zoznam | [knowledge/writing/academic-style.md](knowledge/writing/academic-style.md) |
| Overená bibliografia | [knowledge/bibliography/references.bib](knowledge/bibliography/references.bib) |
| Bakalárska a diplomová práca (PDF + text) | [knowledge/sources/](knowledge/sources/README.md) |

## Nové podklady

Zip z Overleafu, PDF alebo šablónu vlož do `inbox/` a napíš „spracuj inbox“ – obsah sa rozbalí, zaradí a doplní do znalostnej bázy.
