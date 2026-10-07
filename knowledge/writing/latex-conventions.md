# LaTeX konvencie

Jednotné pravidlá pre všetky projekty. Vychádzajú z toho, ako sú napísané existujúce zdroje (článok 1, CV);
kde sa existujúce zdroje od pravidla líšia, je to uvedené v stĺpci „Stav“ a v `README.md` daného projektu.

## 1. Projekt

| Pravidlo | Hodnota | Stav |
|---|---|---|
| Umiestnenie | `projects/<projekt>/`, jeden dokument = jeden priečinok | ✓ |
| Názov projektu | malé písmená, pomlčky, bez diakritiky: `clanok-<n>-<tema>`, `praca-<typ>-<tema>`, `prezentacia-<tema>`, `cv` | ✓ |
| Hlavný súbor | `main.tex` | CV má `norbert-michel-cv.tex`, lebo názov PDF sa posiela ďalej |
| Bibliografia | `references.bib` | CV má `publications.bib` (len vlastné publikácie) |
| Obrázky | `img/`, názvy malými písmenami s pomlčkami | ✓ |
| Dlhý dokument | kapitoly v `chapters/NN-nazov.tex`, vkladané cez `\input` | zatiaľ žiadny |
| Popis projektu | `README.md`: účel, hlavný súbor, príkaz na kompiláciu, odkaz na PDF, stav, známe problémy | ✓ |
| Sebestačnosť | trieda (`.cls`), štýl bibliografie (`.bst`) a všetky vstupy sú v priečinku projektu, aby sa dal zabaliť a nahrať na Overleaf alebo do časopisu | ✓ |
| Kódovanie | UTF-8 | ✓ |
| Generované súbory | len v `outputs/<projekt>/`; výnimka je `pdfa.xmpi`, ktorý balík `pdfx` zapisuje vedľa zdroja | ✓ |

## 2. Kompilácia

```powershell
.\scripts\build-project.ps1 -Project <projekt> [-MainFile <subor.tex>] [-InstallMissing]
```

- Engine je pdfLaTeX cez `latexmk`; bibliografiu (BibTeX alebo biber) si `latexmk` zistí sám.
- Bez `-InstallMissing` kompilácia pri chýbajúcom balíku hneď skončí chybou `File 'xyz.sty' not found`.
  Inštalácia balíkov sťahuje súbory z repozitára MiKTeX, preto sa robí len so súhlasom používateľa.
- Kompilácia sa zastaví na prvej chybe (`-halt-on-error`). Overleaf chyby preskakuje a PDF vyrobí aj tak,
  preto projekt, ktorý na Overleafe „išiel“, môže tu najprv zlyhať – chybu treba opraviť v zdroji.
- Výstup: `outputs/<projekt>/<main>.pdf`; skript na konci vypíše cestu aj relatívny odkaz.
- Kontrola textu v PDF: `pdftotext -enc UTF-8 -layout …` (bez `-enc UTF-8` sa znaky ako `ľ`, `š` z výpisu stratia, hoci v PDF sú).

## 3. Preambula matematického článku

Blok z článku 1 – používaj ho rovnako v ďalších článkoch a v dizertácii, aby číslovanie a vzhľad sedeli.

```latex
% Len s triedou new-aiaa (alebo inde, kde sa načíta newtxmath): newtxmath už definuje
% \openbox a \Bbbk, takže amsthm a amssymb by skončili chybou "Command ... already defined".
\let\openbox\relax
\let\Bbbk\relax
\usepackage{amsmath,amssymb,amsthm}
\numberwithin{equation}{section}

\theoremstyle{definition}
\newtheorem{definition}{Definition}[section]

\theoremstyle{plain}
\newtheorem{theorem}[definition]{Theorem}
\newtheorem{lemma}[definition]{Lemma}
\newtheorem{claim}[definition]{Claim}
\newtheorem{corollary}[definition]{Corollary}
\newtheorem{proposition}[definition]{Proposition}

\theoremstyle{remark}
\newtheorem{remark}[definition]{Remark}
\newtheorem{example}[definition]{Example}

\usepackage{algorithm}        % plávajúce prostredie algorithm (načíta aj float -> [H])
\usepackage{algpseudocode}    % \State, \For, \Require, \Ensure

\usepackage[most]{tcolorbox}  % rámček pre formuláciu problému
\newtcolorbox{problem}[1][]{enhanced, colback=white, colframe=black, boxrule=0.8pt, arc=2pt,
  left=6pt, right=6pt, top=6pt, bottom=6pt, title=\textbf{Problem: #1}}
```

Všetky tvrdenia zdieľajú jedno počítadlo v rámci sekcie (Definition 2.1, Theorem 2.2, …).

Formulácia problému ide do prostredia `problem` s tabuľkou **Input / Question** (rozhodovací) alebo **Input / Output** (optimalizačný).

Balíky `mhchem`, `siunitx`, `longtable`, `tabularx`, `fancyvrb`, `listings`, `subcaption` boli v exporte článku 1 pozostatkom šablóny AIAA
(odstránené); do dokumentu pridávaj len balíky, ktoré naozaj používa.

Dôkazy (`amsthm`):
- dôkaz, ktorý končí zoznamom alebo vysádzaným vzorcom, ukonči `\qedhere` na poslednom riadku – inak štvorček skončí osamotený na novom riadku alebo strane;
- pred `\end{proof}` nenechávaj prázdny riadok;
- dôkaz nezačínaj priamo `\paragraph`, algoritmom ani obrázkom – „Proof.“ by sa prilepilo k prvému nasledujúcemu odseku (aj vnútri algoritmu); začni vetou;
- obrázok ani algoritmus nevkladaj dovnútra prostredia `definition`.

## 4. Notačné makrá

Blok pre texty o Min Cut-Path (článok 1 ho používa):

```latex
\newcommand{\cp}{\operatorname{cp}}                 % cp(u,v): hodnota min. cut-path
\newcommand{\CP}{\operatorname{CP}}                 % CP(u,v): množina cut-paths
\newcommand{\diam}{\operatorname{diam}}
\newcommand{\OPT}{\mathrm{OPT}}
\newcommand{\MinCutPath}{\textsc{Min Cut-Path}}
\newcommand{\SSP}{\textsc{Separating Shortest Path}}
\newcommand{\ThreeSAT}{\textsc{3-SAT}}
```

`\deg` je štandardný operátor – vždy so spätnou lomkou (`\deg(u, J)`, nie `deg(u, J)`).
Význam symbolov: [research/min-cut-path.md](../research/min-cut-path.md), časť 2.

## 5. Labely a odkazy

| Objekt | Prefix | Príklad |
|---|---|---|
| sekcia, podsekcia | `sec:` | `sec:np-completeness` |
| definícia | `def:` | `def:cut-path` |
| veta | `thm:` | `thm:diameter-two` |
| lema | `lem:` | `lem:odd-intersection` |
| claim | `clm:` | `clm:basic-bounds` |
| dôsledok, propozícia | `cor:`, `prop:` | |
| obrázok, tabuľka | `fig:`, `tab:` | `fig:chain-link` |
| algoritmus | `alg:` | `alg:reduction` |
| rovnica | `eq:` | |
| problém | `prob:` | `prob:min-cut-path` |

- Label je malými písmenami s pomlčkami, bez medzier; prefix zodpovedá prostrediu.
- Odkaz vždy s nezlomiteľnou medzerou a veľkým písmenom: `Theorem~\ref{…}`, `Lemma~\ref{…}`, `Section~\ref{…}`, `Figure~\ref{…}`.
- Citácia tiež s `~`: `…graph theory~\cite{GodsilRoyle2001}`.
- Článok 1 pravidlá spĺňa od korektúry 7. 10. 2026 (zoznam labelov je v jeho README).

## 6. Vzorce a obrázky

- Vysádzaný vzorec: `\[ … \]` alebo `equation`/`align`; nie `$$ … $$`.
- V texte `$ … $` (článok 1); v jednom dokumente jeden spôsob.
- Obrázok: `figure` s `\centering`, `\includegraphics[width=…]{img/…}`, `\caption{…}` a `\label{fig:…}` **za** `\caption`. Obrázok bez `\caption` nemá mať `\label`.
- Pomlčky: rozsah a dvojica `u`--`v` cez `--`; vsuvka cez `---` (americká sadzba) – nie spojovník.

## 7. Bibliografia

- Kanonický zdroj záznamov: [bibliography/references.bib](../bibliography/references.bib). Do projektu sa kopíruje len to, čo sa cituje.
- Kľúč nového záznamu: `Priezvisko` + `Rok` + voliteľne kľúčové slovo, napr. `Bollobas2001`, `Cook1971Complexity`. Existujúce kľúče (`henzinger1997faster`, `itai1979maximum`) sa nemenia.
- Kľúč v `\cite` píš presne tak ako v `.bib` vrátane veľkosti písmen (BibTeX rozdiel znesie, biber nie).
- Každý záznam má mať DOI alebo ISBN; údaje sa overujú podľa DOI alebo stránky vydavateľa, nie spamäti.
- ISBN-13 má kontrolnú číslicu: súčet číslic s váhami 1, 3, 1, 3, … musí byť deliteľný 10. V pôvodných `.bib` súboroch bolo viacero ISBN s neplatnou číslicou – každé nové ISBN prepočítaj.
- Pri preberaní záznamu z diplomovej alebo bakalárskej práce ber údaje z `knowledge/bibliography/references.bib`, nie z PDF práce.
- Článok (trieda `new-aiaa`): natbib, číselné citácie, `\bibliography{references}`. CV: biblatex + biber, štýl `ieee`.

## 8. Šablóny

| Šablóna | Na čo | Kde |
|---|---|---|
| `new-aiaa` | článok (trieda z Overleafu, použitá v článku 1) | `templates/new-aiaa/` |
| AltaCV 1.7.3 | životopis | `templates/altacv/` |
| dizertačná práca UPJŠ | – chýba, treba dodať oficiálnu šablónu | – |

Nový projekt vzniká skopírovaním šablóny do `projects/<projekt>/`; šablóny v `templates/` sa neupravujú.
