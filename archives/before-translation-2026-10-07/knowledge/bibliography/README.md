# Bibliografia

Ako sa zdroje hľadajú, overujú, zapisujú a citujú. Platí pre všetky projekty.

## 1. Kde čo je

| Miesto | Obsah | Pravidlo |
|---|---|---|
| [references.bib](references.bib) | kanonická bibliografia všetkých projektov | každý záznam má nad sebou stav a dátum overenia; opravy sa robia najprv tu |
| `projects/<projekt>/references.bib` | len záznamy, ktoré projekt cituje | kópia z kanonického súboru, nič sa tu neopravuje samostatne |
| [../literature/](../literature/README.md) | poznámky z prečítaných prác a záznam hľadaní | podklad pre každé tvrdenie o literatúre |
| [../sources/](../sources/README.md) | plné texty (PDF + `.txt`) vlastných prác a kľúčových zdrojov | pomenované podľa kľúča alebo typu práce |
| `projects/cv/publications.bib` | vlastné publikácie pre CV (biblatex) | zosúladené s `knowledge/author.md` |

## 2. Cesta novej citácie

1. **Nájdi primárny záznam**: stránka DOI u vydavateľa, DBLP, arXiv, zbMATH; pri knihe katalóg vydavateľa.
2. **Prepíš údaje zo záznamu.** Nie spamäti, nie zo zoznamu literatúry iného článku, nie z BibTeX exportu vyhľadávača (bývajú v ňom chybné strany, roky a typy).
3. **Zapíš záznam do `references.bib`** do príslušnej časti, s riadkom stavu nad ním.
4. **Over, že práca obsahuje to, čo jej chceme pripísať** – s číslom vety alebo strany. Pri práci, o ktorú sa text opiera, napíš poznámku do `knowledge/literature/`.
5. **Skopíruj záznam do projektu** a cituj.
6. Kontrola: `.\scripts\check-bib.ps1 -Project <projekt>`.

Údaj, ktorý sa nepodarilo overiť, sa do záznamu nepíše; chýbajúce pole je lepšie než vymyslené.

## 3. Stav záznamu

Riadok komentára nad záznamom (bez diakritiky, aby súbor prešiel aj 8-bitovým BibTeXom):

```bibtex
% OVERENE 2026-10-07 (DOI, stranka vydavatela).
% CIASTOCNE 2026-10-07: autori, nazov a rok overene; strany nie.
% TODO: co treba doriesit.
```

Do rukopisu určeného na odoslanie idú len záznamy `OVERENE`. `CIASTOCNE` sa pred odoslaním dotiahne alebo sa neoverené pole vynechá.

## 4. Kľúč

`Priezvisko` + `Rok` + voliteľne kľúčové slovo: `Bollobas2001`, `Cook1971Complexity`, `GomoryHu1961` (dvaja autori), `RomeraParedes2024FunSearch`.
Len ASCII, bez medzier a pomlčiek. Existujúce kľúče (`henzinger1997faster`, `itai1979maximum`) sa nemenia.
V `\cite` sa kľúč píše presne ako v `.bib` vrátane veľkosti písmen.

## 5. Typy záznamov

Kanonický súbor používa len typy a polia, ktoré pozná klasický BibTeX – taký záznam funguje v každej šablóne (BibTeX aj biblatex).

| Typ | Povinné polia | Poznámka |
|---|---|---|
| `@article` | author, title, journal, volume, number, pages, year, doi | názov časopisu celý, neskrátený |
| `@inproceedings` | author, title, booktitle, pages, publisher, year, doi | `booktitle` celým názvom so skratkou v zátvorke; pri LNCS/LIPIcs aj `series` a `volume`; číslo článku namiesto strán v tvare `12:1--12:17` |
| `@book` | author alebo editor, title, publisher, year, isbn | `edition`, `series`, `number` ak existujú |
| `@incollection` | author, title, booktitle, editor, publisher, year, pages | kapitola v zborníku; cituje sa kapitola, nie celý zborník |
| `@phdthesis`, `@mastersthesis` | author, title, school, year | `type = {Bachelor's thesis}` pre bakalársku prácu; `address`, `url` |
| `@misc` – preprint | author, title, year, eprint, archivePrefix, primaryClass | len kým neexistuje publikovaná verzia |
| `@misc` – softvér, dáta, model, web | author (organizácia v dvojitých zátvorkách), title, year, url, note | `note = {Version 1.2, accessed 2026-10-07}`; pri LLM presný identifikátor modelu |
| `@techreport` | author, title, institution, year, number | |

## 6. Zápis polí

- **Mená:** `Priezvisko, Meno` oddelené `and`; všetci autori, žiadne `and others` z vlastnej vôle. Diakritika ako LaTeX príkazy v zátvorkách (`Bollob{\'a}s`, `Karo{\'n}ski`, `Miche{\v{l}}`, `Erd{\H{o}}s`). Organizácia: `{{Google DeepMind}}`.
- **Názov:** presne ako v publikovanej verzii. Veľké písmená, ktoré musia ostať, sa chránia zátvorkami: `{NP}`, `{LLM}`, `{E}rd{\H{o}}s--{R}{\'e}nyi`, vlastné mená, vzorce. Celý názov sa do dvojitých zátvoriek nedáva.
- **Strany:** `151--158`. **DOI:** holé (`10.1145/800157.805047`), bez `https://doi.org/`. **URL:** len ak DOI nie je, alebo pre voľne dostupný plný text.
- **Preprint a publikovaná verzia:** cituje sa publikovaná; `eprint` v zázname ostáva. Kľúč sa pri prechode z preprintu na publikovanú verziu nemení, ak sa nezmenil rok – inak sa upraví vo všetkých projektoch naraz.
- **Nepatria sem:** `abstract`, `keywords`, `file`, `month`, `language` a polia len pre biblatex (`date`, `journaltitle`, `@online`).
- **ISBN-13:** súčet číslic s váhami 1, 3, 1, 3, … je deliteľný 10. Každé nové ISBN sa prepočíta – v pôvodných súboroch bolo viacero neplatných.

## 7. Členenie `references.bib`

Časti oddelené komentárom; nový okruh dostane novú časť.

| Časť | Obsah |
|---|---|
| Grafy, algoritmy, zložitosť | učebnice a základné výsledky |
| Rezy, toky, súvislosť | |
| Náhodné grafy, pravdepodobnosť | |
| Príbuzné problémy | práce k Min Cut-Path |
| LLM a optimalizácia | téma dizertácie; mapa v `knowledge/research/llm-optimization.md` |
| Písanie | príručky, z ktorých vychádza `knowledge/writing/` |
| Konvexná geometria | zdroje bakalárskej práce |
| Vlastné práce | záverečné práce a publikácie autora |

## 8. Citovanie v texte

- Cituje sa **pôvodný zdroj** výsledku; učebnica pre štandardné pojmy.
- Citácia stojí pri tvrdení, ktoré podopiera, s nezlomiteľnou medzerou: `…minimum cuts~\cite{GomoryHu1961}`.
- Konkrétna veta alebo strana: `\cite[Theorem~7.3]{Bollobas2001}`.
- Citácia nie je podstatné meno. *Gomory and Hu~\cite{GomoryHu1961} show…*, nie *\cite{GomoryHu1961} shows…*. Veta musí byť správna aj po vynechaní citácie – vtedy funguje v číselnom aj menno-rokovom štýle.
- V zdroji sa píše obyčajné `\cite{…}`; `\citet` a `\citep` len v projekte, ktorého šablóna predpisuje menno-rokový štýl.
- Viac prác v jednom príkaze: `\cite{a,b,c}`; poradie rieši štýl.
- Necituje sa pre počet. Práca v zozname literatúry, ktorú autor nevidel, je chyba.
- Vlastná predchádzajúca práca sa cituje vždy, keď z nej text vychádza.
- Softvér, dátové sady, benchmarky a jazykové modely sa citujú ako zdroje.

## 9. Štýl bibliografie

Štýl (`.bst` alebo nastavenie biblatexu) patrí k šablóne miesta publikovania a je v projekte. Dáta v `.bib` sa kvôli štýlu nemenia; ak štýl nezobrazí DOI alebo skráti názov inak, rieši sa to v štýle, nie v zázname.

| Dokument | Systém |
|---|---|
| článok | BibTeX so štýlom šablóny (pri neutrálnej šablóne `natbib` + `plainnat`) |
| dizertácia | podľa univerzitnej šablóny; ak dovoľuje voľbu, biblatex + biber |
| CV | biblatex + biber, štýl `ieee`, vlastný súbor `publications.bib` |
