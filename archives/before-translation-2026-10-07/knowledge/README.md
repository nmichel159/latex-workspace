# Znalostná báza

Všetko, čo treba vedieť pred písaním alebo úpravou článku, záverečnej práce či CV.
Súbory sú písané po slovensky; matematická terminológia ostáva v jazyku dokumentov (angličtina).

## Čo kde je

| Súbor | Obsah | Kedy čítať |
|---|---|---|
| [author.md](author.md) | Meno a jeho zápis, afiliácie, štúdium, školitelia, plánované publikácie | Titulná strana, hlavička článku, poďakovanie, CV |
| [research/min-cut-path.md](research/min-cut-path.md) | Problém Min Cut-Path: definície, notácia, mapa výsledkov (diplomovka ↔ článok 1), otvorené problémy, slovník EN/SK/CZ | Každý text o Min Cut-Path |
| [research/lattice-polytopes.md](research/lattice-polytopes.md) | Bakalárska práca: mriežkové mnohosteny v kocke, hlavné vety | Keď sa spomína bakalárka alebo geometria mnohostenov |
| [writing/latex-conventions.md](writing/latex-conventions.md) | Jednotné LaTeX konvencie: štruktúra projektu, názvy súborov, prostredia, labely, notačné makrá, citácie | Pred založením projektu a pri každej úprave zdrojov |
| [writing/academic-style.md](writing/academic-style.md) | Štýl a stavba odborného textu + kontrolný zoznam chýb, ktoré sa v textoch opakujú | Pri písaní a korektúre textu |
| [bibliography/references.bib](bibliography/references.bib) | Kanonická (overená) bibliografia naprieč projektmi | Pri pridávaní citácie do projektu |
| [sources/](sources/README.md) | Pôvodné práce v PDF + extrahovaný text (`.txt`, dá sa v ňom hľadať) | Keď treba presné znenie definície, vety alebo dôkazu |

## Ako bázu používať

1. Rýchla orientácia: prečítaj príslušný súbor v `research/`.
2. Presné znenie: hľadaj v `sources/*.txt` (napr. `Theorem 22`, `Definition 40`), pri pochybnosti o sadzbe vzorca otvor PDF.
3. Stav konkrétneho dokumentu (čo je hotové, známe problémy): `projects/<projekt>/README.md`.

## Ako bázu udržiavať

- Nový podklad (PDF, zip) patrí do `inbox/`; po spracovaní sa PDF presunie do `sources/` spolu s `.txt` a pridá sa riadok do [sources/README.md](sources/README.md).
- Nový výsledok, definícia alebo zmena notácie v niektorom projekte → doplň príslušný súbor v `research/`.
- Nová citácia → najprv over údaje (DOI, vydavateľ), zapíš do `bibliography/references.bib`, až potom kopíruj do projektu.
- Údaj, ktorý nie je overený, označ `TODO(overiť)`; nepíš domnienky ako fakty.
