# Matematický text

Zápis notácie, definícií, viet, dôkazov a algoritmov. Štýl viet: [academic-style.md](academic-style.md);
sadzba v LaTeXe: [latex-conventions.md](latex-conventions.md).

## 1. Notácia

- **Jeden symbol, jeden význam; jeden objekt, jeden symbol** – v celom dokumente. Kolízia sa rieši premenovaním, nie poznámkou *(by abuse of notation)*.
- Symbol sa zavedie tam, kde sa prvý raz použije, a po dlhšej prestávke sa pripomenie slovom (*the cut $C$*).
- Symbol použitý menej než trikrát sa nahradí slovami.
- Viacpísmenový operátor alebo názov problému má makro (`\cp`, `\diam`, `\MinCutPath`); makrá sú v `preamble/macros.tex`.
- Viazané premenné v lemách nesmú kolidovať s globálnymi (ak sú `u, v` pevné vrcholy problému, lema kvantifikuje cez `x, y`).
- Hodnota a objekt majú rôzne symboly (`c(u,v)` je číslo; rez je `C`).

Ustálené písmená v autorových textoch – nové texty ich držia:

| Písmená | Význam |
|---|---|
| `G, H` | grafy; `V, E` množiny vrcholov a hrán; `n = \|V\|`, `m = \|E\|` |
| `u, v` | význačné vrcholy problému; `x, y, w` ostatné vrcholy; `e, f` hrany |
| `P, Q` | cesty; `C` rez; `S, A, B` množiny; `F` riešenie |
| `i, j, k, r, t` | indexy a počty; `d` vzdialenosť; `c` veľkosť rezu |
| `\alpha, \beta` | konštanty modelu; `\varepsilon` malá kladná konštanta; `p` pravdepodobnosť hrany |

Asymptotika a pravdepodobnosť:

- Pri `O`, `\Omega`, `\Theta`, `o` je jasné, ktorá premenná rastie a čo je konštanta (*for fixed $\alpha$, as $n \to \infty$*).
- *With high probability* sa definuje raz v Preliminaries (napr. s pravdepodobnosťou `1 - o(1)` pre `n \to \infty`) a potom sa používa len tento termín – nie striedavo *almost surely*, *a.a.s.*, *w.h.p.*
- Základ logaritmu sa povie raz.
- Kvantifikátor *for all $n \ge n_0$* sa nemieša s limitou v tom istom tvrdení.

## 2. Vzorce vo vete

- Veta sa nezačína symbolom: *$G$ is connected* → *The graph $G$ is connected*.
- Dva vzorce oddeľuje slovo: *for $i < k$, $x_i = 0$* → *we have $x_i = 0$ for all $i < k$*.
- `\forall`, `\exists`, `\Rightarrow`, `\Leftrightarrow` nepatria do súvislého textu; píšu sa slovom.
- Vysádzaný vzorec je súčasťou vety a má jej interpunkciu. Vysádza sa vzorec dlhý, dôležitý alebo neskôr citovaný; číslo dostane len ten, na ktorý sa odkazuje.
- V definícii *if* znamená „práve vtedy“; vo vete sa ekvivalencia píše celá: *if and only if*.
- Prídavné mená so spojovníkom pred podstatným menom (*polynomial-time algorithm*, *$k$-connected graph*), bez neho za slovesom (*runs in polynomial time*). Dvojica vrcholov s pomlčkou: `$u$--$v$ path`.
- Čísla do desať slovom, ak počítajú veci (*two paths*, *diameter two*), číslicou vo vzorci a pri meraní.

## 3. Definície

- Definovaný pojem je zvýraznený (`\emph`) a definuje sa práve raz.
- Všetky premenné definície sú kvantifikované v nej; predpoklady sa neskrývajú do textu pred prostredím.
- Prostredie `definition` pre pojmy, na ktoré sa neskôr odkazuje; jednoduchý pojem stačí zaviesť vo vete.
- Po netriviálnej definícii nasleduje príklad; pri jemnej hranici aj protipríklad.
- Jedna veta intuície pred formálnou definíciou pomáha; odsek intuície ju nahrádzať nesmie.
- Definícia má názov: `\begin{definition}[Cut-path]`.
- Obrázok ani algoritmus sa nevkladajú dovnútra prostredia `definition`.

## 4. Znenia viet

**Veta sa dá citovať samostatne**: obsahuje všetky predpoklady a všetky objekty zavádza sama (*Let $G$ be a connected graph of diameter two and let $u, v$ be distinct vertices. Then …*).

| Prostredie | Použitie |
|---|---|
| Theorem | hlavné výsledky článku (málo) |
| Proposition | menší výsledok, ktorý má význam sám osebe |
| Lemma | nástroj pre dôkaz vety |
| Corollary | bezprostredný dôsledok; dôkaz najviac pár riadkov |
| Claim | tvrdenie vnútri dôkazu, mimo neho sa nepoužíva |
| Observation / Remark | zrejmý fakt, ktorý sa použije / poznámka, na ktorej logika nestojí |
| Conjecture | nedokázané tvrdenie s uvedeným dôvodom |

- Tvar: *Let … . If … , then … .* alebo *For every … , … .* Poradie kvantifikátorov je jednoznačné.
- Konštanty sú výslovné alebo je povedané, od čoho závisia (*there exist constants $0 < \beta_1 < \beta_2$ depending only on $\alpha$*).
- Algoritmická veta: *There is an algorithm that, given …, computes … in time $O(\dots)$.*
- Rozhodovací problém je *NP-complete*, optimalizačný *NP-hard*; príslušnosť do NP sa dokazuje alebo výslovne konštatuje.
- Pravdepodobnostná veta menuje model, režim parametrov a zmysel pravdepodobnosti (*Let $\alpha > 1$ and $p \ge \alpha \log n / n$. Then with high probability $G(n,p)$ …*).
- Prevzatá veta hovorí to isté čo zdroj a cituje sa s miestom: `\cite[Theorem~7.3]{Bollobas2001}`. Znenie sa overí v zdroji, nie v druhotnej literatúre.
- Čo sa nedokazuje ani necituje, sa netvrdí.
- Predpoklady vety sedia s predpokladmi použitých liem (`p = …` vs. `p \ge …`, `\alpha > 0` vs. `\alpha > 1`).

## 5. Dôkazy

- **Stratégia jednou vetou** pred dôkazom dlhším než pol strany (*We reduce from 3-SAT: the chain encodes a truth assignment and each thread encodes a clause.*).
- **Členenie**: kroky alebo tvrdenia s názvami; prípady sú pomenované, úplné a je povedané prečo (*Case 1: $d(u,v) = 1$.*).
- **Každý krok má dôvod**: *by Lemma 3*, *since $G$ is connected*, *by the choice of $P$*. Slová *clearly*, *obviously*, *trivially*, *it is easy to see* dôvod nenahrádzajú.
- Priamy dôkaz alebo obmena má prednosť pred sporom. Dôkaz sporom výslovne uvedie predpoklad a na konci povie, s čím je v spore.
- *Without loss of generality* len so symetriou, ktorá ho oprávňuje.
- Indukcia: povie sa, podľa čoho, báza a indukčný predpoklad.
- Výpočet je reťaz zarovnaných vzťahov; neštandardný krok má zdôvodnenie hneď za ním.
- Miera podrobnosti: čitateľ z odboru overí každý krok bez papiera. Rutinné overenia idú v konferenčnej verzii do dodatku.
- Obrázok dôkaz podporuje, nenahrádza.
- Dôkaz sa nezačína algoritmom, obrázkom ani `\paragraph`; končí sa `\qedhere`, ak je posledným riadkom vzorec alebo zoznam.

Pevné osnovy:

| Typ dôkazu | Osnova |
|---|---|
| Algoritmická veta | 1. Correctness → 2. Optimality (ak sa tvrdí) → 3. Running time s rozpisom krokov |
| NP-úplnosť | zdrojový problém a jeho presný tvar → konštrukcia (obrázok ku každému gadgetu) → veľkosť a čas → smer ⇒ → smer ⇐ → príslušnosť do NP |
| Pravdepodobnostný odhad | udalosť a jej pravdepodobnosť → použitá nerovnosť s citáciou a presným tvarom → zjednotenie cez koľko udalostí → výsledná pravdepodobnosť |
| Štrukturálna veta | dolný odhad → horný odhad (alebo konštrukcia → optimalita) |

## 6. Algoritmy

- Pseudokód je pre čitateľa: matematická notácia, žiadna syntax programovacieho jazyka, rovnaké symboly ako v texte.
- Hlavička: názov, **Input**, **Output**. Riadky sú číslované, ak sa na ne text odvoláva. Viac než približne 25 riadkov sa delí na procedúry.
- Popis (`\caption`) hovorí, čo algoritmus počíta, a prípadne zložitosť.
- Text vysvetľuje myšlienku a invariant, neprerozpráva pseudokód riadok po riadku.
- Dátové štruktúry sa uvedú tam, kde od nich závisí zložitosť.
- Zložitosť je vo vete s parametrami (`n`, `m`) a s výpočtovým modelom, ak na ňom záleží.

## 7. Obrázky ku konštrukciám

- Jeden obrázok na jednu konštrukciu alebo gadget; označenia v obrázku sú tie isté symboly ako v texte.
- Popis hovorí, čo má čitateľ vidieť (*A chain link: the two $p$–$q$ paths have equal length.*), nie len čo to je.
- Vektorová grafika (TikZ alebo PDF) má prednosť pred rastrovou; písmo v obrázku je písmo dokumentu.
- Každý obrázok je spomenutý v texte pred miestom, kde sa objaví.
