# Šablóna `article-modular`

Neutrálna šablóna článku (trieda `article`, 11pt, A4, pdfLaTeX) s rozložením, ktoré je štandardom pre všetky
projekty: obsah rukopisu je v súboroch, ktoré sa pri zmene šablóny časopisu nemenia, a od šablóny závisí len
tenký obal `main.tex`.

## Rozloženie

```
main.tex                    obal – JEDINÝ súbor závislý od šablóny: \documentclass, písmo a okraje, natbib, hyperref,
                            názov, autor, obal abstraktu a kľúčových slov, \input častí, príkazy bibliografie
preamble/packages.tex       prenosné balíky (matematika, grafika, algoritmy)
preamble/environments.tex   prostredia definition, theorem, lemma, … (jedno počítadlo v sekcii), rámček problem, číslovanie rovníc
preamble/macros.tex         notačné makrá (\N, \Z, \R, \E, \OPT, \diam, \poly, \abs, \ceil, \floor, \set, \problemname)
sections/00-abstract.tex    len TEXT abstraktu (bez \begin{abstract})
sections/01-introduction.tex … 04-conclusion.tex   každý súbor začína \section{…} a \label{sec:…}
sections/90-acknowledgments.tex   len text poďakovania; nadpis dodáva obal
references.bib              bibliografia (BibTeX cez natbib, štýl plainnat)
img/                        obrázky
```

## Čo závisí od šablóny

Len `main.tex` a súbory triedy (`.cls`, `.bst`). Pri prechode na šablónu časopisu sa `main.tex` nahradí obalom
novej triedy, ktorý v rovnakom poradí načíta `preamble/packages` → (hyperref, cleveref) → `preamble/environments` →
`preamble/macros` a cez `\input` vloží tie isté súbory zo `sections/`. Názov, autor, afiliácia a kľúčové slová sa
prepíšu do syntaxe novej triedy. Ak trieda niektorý balík alebo prostredie načítava sama, príslušný riadok
v `preamble/` sa zakomentuje – text v `sections/` sa nemení.

## Nový projekt

```powershell
Copy-Item -Recurse templates\article-modular projects\clanok-<n>-<tema>
.\scripts\build-project.ps1 -Project clanok-<n>-<tema>
```

Potom v projekte prepíš tento súbor na `README.md` projektu (vzor: `projects/clanok-1-min-cut-path/README.md`)
a doplň riadok do tabuľky projektov v koreňovom `README.md` a v `CLAUDE.md`. Notáciu projektu pridaj do
`preamble/macros.tex`, sekcie premenuj a pridaj podľa obsahu (`sections/NN-nazov.tex`, vkladané cez `\input`).

## Stav (7. 10. 2026)

- Kompiluje sa bez chýb (1 strana). Kým `references.bib` neobsahuje citovaný záznam, natbib hlási
  „Empty `thebibliography' environment“ a BibTeX „I found no \citation commands“ – po prvom `\cite` to zmizne.
- `cleveref`, `mathtools` a `booktabs` nie sú v MiKTeX-e nainštalované, preto ich šablóna nenačítava: odkazy sa
  píšu ručne (`Theorem~\ref{…}`), `\abs`, `\ceil`, `\floor`, `\set` majú jednoduché definície. Miesta, kde sa
  balíky po inštalácii zapnú, sú v `main.tex` a `preamble/packages.tex` zakomentované.
- Písmo Latin Modern nemá tučné kapitálky: `\problemname{…}` v nadpise rámčeka `problem` sa vysádza tučným
  základným rezom (varovanie „Font shape T1/lmr/bx/sc undefined“). So šablónou časopisu to závisí od jej písma.
