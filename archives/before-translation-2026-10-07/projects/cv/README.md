# CV – Norbert Micheľ

| | |
|---|---|
| Typ | životopis, 2 strany A4 |
| Jazyk | angličtina |
| Hlavný súbor | `norbert-michel-cv.tex` |
| Trieda | `altacv.cls` 1.7.3 (LianTze Lim, licencia LPPL – `LICENSE.md`) |
| Publikácie | `publications.bib` cez biblatex + biber, nastavenie v `pubs-num.tex` |
| Kompilácia | `.\scripts\build-project.ps1 -Project cv` |
| PDF | [outputs/cv/norbert-michel-cv.pdf](../../outputs/cv/norbert-michel-cv.pdf) |
| Čistá šablóna | `templates/altacv/` |

## Súbory

```
norbert-michel-cv.tex       celý životopis (makrá + obsah)
norbert-michel-cv.xmpdata   metadáta PDF (názov, autor, kľúčové slová)
publications.bib            vlastné publikácie
pubs-num.tex                nastavenie biblatexu (číselný štýl ieee)
altacv.cls                  trieda dokumentu
latexmkrc                   nastavenie latexmk pre pdfx
pdfa.xmpi                   generuje balík pdfx pri kompilácii (needitovať)
```

## Čo treba vedieť pri úprave

- Vlastné makrá sú na začiatku súboru: `\cvsect`, `\cvrole`, `\cvproject`, `\cvaward`, `\cvedu`, `\cvlang`, `\cvtag` / `\cvtagmain`, `\cvtimeline`.
- Časová os: mesiace sú orientačné; `\tlnow` (dnešný dátum na osi) je zadaný ručne – pri úprave ho posuň (`rok + (mesiac − 1)/12`).
- `\fillin{…}` označuje text na doplnenie; v hotovom CV nesmie ostať.
- Dokument musí ostať na 2 stranách; po každej zmene skontroluj zlomy a pretečené riadky v PDF.
- Publikácie v CV musia sedieť s `knowledge/author.md` (momentálne dva rukopisy „in preparation“).

## História

**7. 10. 2026 – korektúra**
- `analyses` → `analyzes` (zvyšok CV je v americkom pravopise), `front-ends` → `front ends` (ako `front end`, `back end` inde v texte).
- Názov diplomovej práce: *Min Cut-Path* (podľa titulnej strany práce; pôvodne *The Min Cut-Path Problem*).
- Publikácie: meno autora `Micheľ, N.` namiesto `Michel, N.` (zhodne s hlavičkou CV), `\mynames{Micheľ/N.}`.
- `\tlnow` posunuté na október 2026.
- Nezmenené, na zváženie: názov témy PhD *Optimisation Algorithms Powered by LLMs* je v britskom pravopise
  (inde *Optimization*) – ponechané, lebo oficiálne znenie názvu nepoznám; rovnako kľúčové slovo v `.xmpdata`.
- Publikácie „in preparation“ treba zosúladiť s článkami 1 a 2, keď budú ich názvy definitívne.

**7. 10. 2026 – upratanie**

Pozostatky šablóny (`sample.tex`, `sample.bib`, `pubs-authoryear.tex`, vzorové obrázky, README a CHANGELOG triedy)
boli 7. 10. 2026 presunuté do `archives/removed-from-projects/cv/`; CV ich nepoužíva.
