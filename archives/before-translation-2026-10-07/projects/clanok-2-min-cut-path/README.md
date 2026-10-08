# Článok 2 – Min Cut-Path (zatiaľ prázdny)

| | |
|---|---|
| Typ | článok do časopisu – rezervované miesto, zdroje ešte nie sú |
| Zdroj obsahu | **diplomová práca *Min Cut-Path* (2025)** – rozhodnutie autora zo 7. 10. 2026 |
| Hlavný súbor | – (po založení `main.tex`) |
| Kompilácia | `.\scripts\build-project.ps1 -Project clanok-2-min-cut-path` (až keď tu bude `main.tex`) |
| PDF | – |
| Pôvod | prázdny priečinok `clanok_2 min cut-path`, 7. 10. 2026 premenovaný podľa konvencie |

## Čo treba pred začatím

1. **LaTeX zdroj diplomovej práce.** V repozitári je len PDF a extrahovaný text
   (`knowledge/sources/diplomova-praca-2025-min-cut-path.*`). Ak zdroj existuje (Overleaf, disk), vlož zip do `inbox/` –
   vzorce, algoritmy a obrázky sa potom preberú presne. Bez neho sa text prepisuje z PDF.
2. **Rozsah a názov.** Článok 1 už z diplomovky použil: priemer 2, rez najviac 2, náhodné grafy (aproximačná schéma).
   Nepoužité ostali (pozri [knowledge/research/min-cut-path.md](../../knowledge/research/min-cut-path.md), časť 4):
   - kap. 2: tree-cut, 2-aproximácia, globálne minimum, partial path / partial cut property;
   - kap. 3.3: trieda *diam or cut 2*, general square graph decomposition, polynomiálny a lineárny algoritmus;
   - kap. 4.5: almost polynomial average-case algoritmus (Path-Cut);
   - kap. 5: symetrický prípad `c = d = cp`, Filter-BFS, Local-Cut, nearly k-regular grafy.
   CV uvádza dva pracovné názvy: *Polynomial-Time Solutions for Island Structures in the Min Cut-Path Problem* a
   *Random Graph Models for the Min Cut-Path Problem*.
3. **Šablóna.** Zatiaľ `templates/new-aiaa/` (rovnaká ako článok 1); cieľový časopis sa určí neskôr.

## Na čo si dať pozor pri preberaní z diplomovky

Zoznam chýb zistených v diplomovke je v [knowledge/research/min-cut-path.md](../../knowledge/research/min-cut-path.md), časť 5a
(koncentrácia stupňov, `α > 1`, bibliografia, „NP-hardness is open“). Text treba prispôsobiť článku podľa
[knowledge/writing/academic-style.md](../../knowledge/writing/academic-style.md): sekcie namiesto kapitol, `Lemma`/`Theorem`,
notácia `\cp`, `\CP`, citovať článok 1 pre NP-úplnosť.
