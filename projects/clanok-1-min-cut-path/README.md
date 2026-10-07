# Článok 1 – Min Cut-Path Problem

| | |
|---|---|
| Typ | článok do časopisu (rukopis) |
| Jazyk | angličtina (americký pravopis) |
| Hlavný súbor | `main.tex` |
| Trieda | `new-aiaa.cls` (`journal`), bibliografia `new-aiaa.bst` cez natbib – **dočasná**, článok sa neskôr prepíše do šablóny cieľového časopisu (zatiaľ neurčený) |
| Bibliografia | `references.bib` (12 záznamov, všetky citované a overené) |
| Kompilácia | `.\scripts\build-project.ps1 -Project clanok-1-min-cut-path` |
| PDF | [outputs/clanok-1-min-cut-path/main.pdf](../../outputs/clanok-1-min-cut-path/main.pdf) |
| Pôvod | Overleaf export `archives/clanok_1_min_cut_path.zip` (7. 10. 2026) |
| Znalostná báza | [knowledge/research/min-cut-path.md](../../knowledge/research/min-cut-path.md) |

## Stav

Kompiluje sa bez chýb a bez varovaní (7. 10. 2026): 23 strán, žiadne nedefinované odkazy ani citácie, žiadne pretečené riadky,
BibTeX bez varovaní. Text prešiel úplnou korektúrou (formálne chyby, konzistencia, jazyk, zdroje) – pozri „História úprav“.

**Pred odoslaním musí autor skontrolovať obsahové zmeny** z časti „Obsahové zmeny na kontrolu“.

## Obsah článku

| Sekcia | Label | Obsah |
|---|---|---|
| I Introduction | `sec:introduction` | motivácia, príbuzné problémy, príspevky, vzťah k diplomovej práci |
| II Fundamentals | `sec:fundamentals` | cut-path, `CP(u,v)`, `cp(u,v)`, optimalizačná verzia, Lemma *Basic Bounds*, average (1+ε)-approximation scheme |
| III NP-completeness | `sec:np-completeness` | 3-SAT → Separating Shortest Path (`sec:ssp`: reťaz, vlákna, kalibrácia) → Min Cut-Path (`sec:ssp-to-mcp`) |
| IV Graphs of Diameter Two | `sec:diameter-two` | rozklad `I, J, K, L`, nepárny prienik cesty a rezu, `cp = c + d − 1` |
| V Graphs with Cut-Value at Most Two | `sec:cut-two` | kaktusová štruktúra, `cp = c + d − 1` |
| VI Erdős–Rényi Graphs | `sec:random-graphs` | priemer 2 v hustých grafoch, vlastnosti riedkych, aproximačná schéma |
| VII Conclusion | `sec:conclusion` | zhrnutie, ďalšie smery |

Labely tvrdení: `lem:basic-bounds`, `thm:ssp-np-complete`, `alg:reduction`, `thm:mcp-np-complete`, `lem:cut-decomposition`,
`lem:empty-i-or-l`, `lem:odd-intersection`, `thm:diameter-two`, `rem:algorithm`, `thm:cut-two`, `thm:random-diameter-two`, `thm:random-diameter`,
`thm:random-connectivity`, `lem:degree-bounds`, `lem:connectivity-bounds`, `thm:approximation-scheme`.

## Súbory

```
main.tex          celý článok (jeden súbor); notačné makrá \cp, \CP, \OPT, \MinCutPath, \SSP, \ThreeSAT v preambule
references.bib    bibliografia
new-aiaa.cls      trieda dokumentu (Overleaf, v1.2)
new-aiaa.bst      štýl bibliografie
img/              chain.png, chain-link.png, chain-link-types.png, chain-threads.png, threading.png, diameter-two-structure.png
```

Verzia pred korektúrou: `archives/removed-from-projects/clanok-1-min-cut-path/main-before-revision-2026-10-07.tex`
(dá sa porovnať s aktuálnym `main.tex`).

## Obsahové zmeny na kontrolu

Tieto úpravy menia matematický obsah alebo tvrdenia o literatúre. Sú urobené na základe nálezov z korektúry, ale zodpovedá za ne autor.

1. **Dôkaz NP-úplnosti Separating Shortest Path (Theorem III.5) je prepísaný.**
   - Pribudla procedúra `Calibrate` (vyrovnanie dĺžok oboch ciest každého článku reťaze; predĺženie spojovacích ciest vlákien na aspoň `Λ` hrán) a je volaná v algoritme.
   - Dôkaz korektnosti má teraz kroky: najkratšie cesty sú práve cesty reťaze → cesta musí „zasiahnuť“ každé vlákno → synchronizačné vlákna vynútia konzistentné znamienka → klauzulové vlákna zodpovedajú splneniu klauzúl → analýza `G ∖ P` cez „nepoužité cesty“ a slepé konce.
   - Algoritmus používa množiny výskytov `O_i` a indexy `L_{j,k,i}` (pozícia `j`, klauzula `k`, premenná `i`) namiesto `ℓ[0], ℓ[1]`; opravené zátvorky.
   - Do definície vlákna pribudlo, že vlákno neobsahuje jednoduché hrany reťaze; reťaz má `r` článkov (namiesto `m`).
2. **Lemma II.4 (Basic Bounds) je nová** – `max{c, d} ≤ cp ≤ c + d − 1` s dôkazom (v diplomovke Claim 6 a 7). Dôkazy viet IV.5 a V.1 sa na ňu odvolávajú.
3. **Veta V.1 (rez najviac 2) má riadny dôkaz** – prevzatý z diplomovky (Theorem 18) a doplnený o argument s mostom a oblúkmi cyklov.
4. **Stupne vrcholov v `G(n, α log n / n)`**: pôvodná „Degree Concentration“ (všetky stupne v `(1 ± ε) α log n` pre každé pevné `ε`) pre pevné `α` neplatí – minimálny a maximálny stupeň sú od `α log n` vzdialené o konštantný násobok. Nahradené Lemou VI.4 (*Degree Bounds*): existujú konštanty `0 < β₁ < β₂` závislé len od `α`, že všetky stupne sú v `[β₁ log n, β₂ log n]`, s dôkazom cez Chernoffove odhady. Nadväzne upravená Lema VI.5 (hranice pre `c(u,v)`) a dôkaz Vety VI.6. Výsledná veta o aproximačnej schéme sa nemení. **Rovnaká chyba je v diplomovke (Theorem 28, Claim 29).**
5. **Veta VI.6** (aproximačná schéma): predpoklad `p ≥ α log n / n` je zachovaný, v dôkaze je doplnený argument monotónnosti (pridanie hrán nezväčší vzdialenosti a nezmenší `c(u,v)`).
6. **Veta VI.1** (priemer 2 pre konštantné `p`): `α > 1` namiesto `α > 0` a pridaná citácia [Bollobás].
7. **Definícia cut-path v rámčekoch problémov**: „contains subsets `P, C ⊆ S`“ namiesto „can be partitioned into `S = P ∪ C`“ (zhodne s Definíciou II.1).
8. **Optimalizačná verzia je NP-hard** (pôvodne „NP-complete“).
9. **Úvod**: problém je uvedený ako zavedený v diplomovej práci [5]; pribudla veta, že NP-úplnosť je nová a výsledky o triedach grafov a náhodných grafoch pochádzajú z diplomovky. V závere je odkaz na čiastočné výsledky pre triedu „diam or cut 2“.
10. **Úvod, príbuzné práce**: formulácia pri citáciách [1]–[3] je upravená tak, aby zodpovedala obsahu citovaných prác (multi-terminal minimum cuts; representations of all minimum cuts; small cuts and edge connectivity).
11. Menšie spresnenia: `u, v` ležia v tom istom komponente; lema o nepárnom prieniku je formulovaná pre rez `C` s dvoma stranami (pôvodne sa rez volal `c(u,v)`, čo kolidovalo s hodnotou minimálneho rezu); definícia priemeru („at most `k`“); viazané premenné v lemách sú `x, y`, aby nekolidovali s `u, v`.

12. **Doplnené pri štylistickej revízii** (7. 10. 2026, druhé kolo): Remark IV.6 (ak platí `cp = c + d − 1`, zjednotenie ľubovoľného minimálneho rezu a ľubovoľnej najkratšej cesty je minimálny cut-path – tým je podložená veta o „jednoduchom algoritme“); bod 4 v definícii reťaze (časti reťaze zdieľajú vrchol len vtedy, keď susedia); jednovetová definícia `G(n, p)`; veta, že pre husté náhodné grafy sa problém dá riešiť presne v polynomiálnom čase na takmer všetkých vstupoch.

## Hodnotenie (7. 10. 2026)

Článok ako celok dáva zmysel: definície → NP-úplnosť → dve polynomiálne triedy → náhodné grafy na seba nadväzujú a v dôkazoch v aktuálnom znení som nenašiel chybu (redukciu z 3-SAT, vetu o priemere 2 aj vetu o reze ≤ 2 som prešiel krok po kroku, vzorec overil na `K_n`, `C_4`, `C_5`, `K_{2,3}` a Petersenovom grafe). Slabé miesta, zoradené podľa dôležitosti:

1. **Príbuzné práce.** Chýba porovnanie s blízkymi problémami. Najbližší je *non-separating st-path* (cesta, po odstránení ktorej hrán ostane graf súvislý) – zrkadlový pojem k Separating Shortest Path; jeho existencia je na všeobecných grafoch NP-ťažká (X. Mao, arXiv:2101.03519). Ďalej interdikcia najkratších ciest / „most vital edges“ a problém Force Path Cut. Recenzent sa na to takmer iste opýta; tvrdenie „not studied elsewhere“ treba podoprieť odsekom o týchto prácach.
2. **Definícia II.5 vs. Veta VI.6** – pozri nižšie; navyše „approximation scheme“ zvyčajne znamená rodinu algoritmov parametrizovanú `ε`. Tu ide o jeden algoritmus, ktorého pomer ide k 1 – výsledok by sa dal povedať jednoduchšie a silnejšie („asymptotically optimal with high probability“).
3. **Abstrakt a názov** – abstrakt neuvádza výsledky, názov je všeobecný.
4. **Veta VI.2** – tvrdenie pre `α > 1` platí, ale presný zdroj je Chung, Lu: *The Diameter of Sparse Random Graphs* (2001): priemer je `(1 + o(1)) log n / log(np)`; odporúčam citovať túto prácu popri [9].
5. **Motivácia** – úvod teraz jednou vetou hovorí, čo rez v modeli zaručuje; článok sa k aplikácii ďalej nevracia (pre teoretický článok v poriadku).

## Ostáva na zváženie (nezmenené)

- **Definícia II.5** meria „takmer všetky vstupy“ podielom `|I_opt(n)| / |I(n)|`, t. j. rovnomerne cez všetky grafy (to zodpovedá `p = 1/2`), kým Veta VI.6 hovorí o `G(n, p)`. Návrh: pridať do bodu 3 vetu, že pri vstupoch z pravdepodobnostného rozdelenia sa podiel nahrádza pravdepodobnosťou.
- **Abstrakt** neuvádza výsledky (NP-úplnosť, vzorec `cp = c + d − 1`, aproximačná schéma) – len motiváciu.
- **Vety VI.2 a VI.3** sú citované podľa [9] a [10]; presné znenie a číslo vety v knihách treba overiť (`TODO(overiť)`), knihy som nemal k dispozícii.
- Citácia [3] pri kaktusovej štruktúre je uvedená ako „cf.“ – práca sa týka kaktusovej reprezentácie 2-rezov, samotné tvrdenie je v článku zdôvodnené priamo.
- Cieľový časopis a jeho šablóna (riešime neskôr).

## História úprav

**7. 10. 2026 – štylistická revízia (druhé kolo)**
- Odstránené opakovania: definícia cut-path už nie je trikrát (rámčeky problémov odkazujú na Definíciu II.1), zdvojené uvádzacie vety pred definíciami a vetami, voľne stojaca veta „Without loss of generality… `L = ∅`“.
- Skrátené rozvláčne formulácie (*It is a well-established result…*, *Building on the structural insights…*, *For a better understanding…*), znenia viet a liem bez „Formally:“ tam, kde vzorec len opakoval text.
- Jednotne: *graphs of diameter two* (slovom), *minimum cut-value*, `G(n, p)` (bez `p(n)`), nadpis *Erdős–Rényi* s pomlčkou, medzititulky v dôkazoch (`\paragraph{…}` s bodkou, rovnaké názvy krokov v oboch dôkazoch NP-úplnosti), popisy obrázkov.
- Parametre procedúry `Thread` premenované na `(K_1, σ_1), …, (K_t, σ_t)`, aby nekolidovali s článkami `L_i`, literálovými článkami `L_{j,k}` a indexom klauzuly `k`.
- Sekcia VI: najprv veta o priemere 2, až potom jej dôsledok pre Min Cut-Path (pôvodne naopak).
- Poďakovanie bez tučného písma.
- Článok má 23 strán.

**7. 10. 2026 – korektúra**
- Formálne: odstránený odsek z diplomovky s odkazom na neexistujúci obrázok; popis k obrázku typov článkov reťaze + odkaz naň v texte; obrázky vyňaté z vnútra definícií; `\deg`, `\[ … \]`, odstránené `\Bigr.`; `c(v,v)` → `c(u,v)`; „Chapter/This chapter“ → sekcie; QED značky na konci dôkazov (`\qedhere`); úvodná veta dôkazu, aby „Proof.“ neskočilo do algoritmu.
- Konzistencia: notácia cez makrá (`\cp`, `\CP`), `CP(u,v)` všade; „Lemma~\ref“; labely podľa konvencie (`sec:`, `def:`, `lem:`, `thm:`, `fig:`); nadpis sekcie IV; jednotné `$…$`.
- Jazyk: preklepy a gramatika v celom texte (napr. *egde*, *prove show*, *a Average*, *for large random.*, *More Formally*, *Firstly/Secondly* → *First/Second*, chýbajúce pomlčky a členy), odstránené zdvojené vety.
- Preambula: odstránené nepoužité balíky šablóny (`textcomp`, `mhchem`, `siunitx`, `longtable`, `tabularx`, `fancyvrb`, `listings`, `subcaption`).
- Obrázky premenované: `chain_threads` → `chain-threads`, `chain_link` → `chain-link`, `Chain_link_example` → `chain-link-types`, `Threading` → `threading`, `2_diam_2` → `diameter-two-structure`.
- Bibliografia (všetko overené podľa DOI / stránky vydavateľa):
  | Záznam | Oprava |
  |---|---|
  | Mehlhorn, Neumann, Schmidt | časopis *Algorithmica* 77(2), 309–335, 2017 (pôvodne ACM TALG 12(1), 2016); kľúč `Mehlhorn2017Certifying` |
  | Gomory, Hu | DOI `10.1137/0109047` (pôvodne `…045`) |
  | Cormen a kol. | ISBN 978-0-262-04630-5 (pôvodné malo neplatnú kontrolnú číslicu) |
  | Diestel | 6. vydanie vyšlo 2025, ISBN 978-3-662-70106-5 (pôvodne 2023 a neplatné ISBN); kľúč `Diestel2025` |
  | Frieze, Karoński | ISBN 978-1-107-11850-8 |
  | Godsil, Royle | ISBN 978-0-387-95220-8 |
  | Bollobás | doplnená séria Cambridge Studies in Advanced Mathematics 73 |
  | Cook | typ `@inproceedings`, kľúč v `\cite` zhodný s `.bib` |
  | Micheľ 2025 | nový záznam – diplomová práca |
  | Itai–Shiloach, Henzinger a kol., Nagamochi–Kameda | overené, bez zmeny údajov |

**7. 10. 2026 – import z Overleafu**
- `sample.bib` → `references.bib` (odstránené vzorové AIAA záznamy); `graph.jpg` (vzorový obrázok šablóny) do archívu.
- Do preambuly `\let\openbox\relax` a `\let\Bbbk\relax` (konflikt `newtxmath` s `amsthm`/`amssymb`, ktorý Overleaf preskakuje).
- Doinštalovaných 25 balíkov MiKTeX: `newtx`, `xpatch`, `xstring`, `carlisle`, `binhex`, `footmisc`, `setspace`, `abstract`, `preprint`,
  `titlesec`, `lettrine`, `caption`, `quoting`, `natbib`, `mhchem`, `chemgreek`, `siunitx`, `translations`, `amscls`, `algorithmicx`,
  `algorithms`, `float`, `fancyvrb`, `txfonts`, `tex-gyre`. Na inom počítači ich treba doinštalovať znova (`-InstallMissing`).
