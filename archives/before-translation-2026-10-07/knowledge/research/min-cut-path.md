# Min Cut-Path – výskumný prehľad

Zdroje: diplomová práca *Min Cut-Path* (UK Praha, 2025; ďalej **DP**) a rukopis článku 1
(`projects/clanok-1-min-cut-path/main.tex`; ďalej **Č1**). Čísla definícií a viet z DP sa dajú dohľadať
v `knowledge/sources/diplomova-praca-2025-min-cut-path.txt`.

## 1. Problém

Graf `G = (V, E)` je neorientovaný a konečný, `u, v ∈ V` sú dva rôzne vrcholy.

- **Cut-path** medzi `u` a `v`: množina hrán `S ⊆ E`, ktorá obsahuje podmnožiny `P, C ⊆ S` také, že `P` je `u`–`v` cesta a `C` je rez oddeľujúci `u` a `v`.
- **Min Cut-Path (optimalizácia):** nájsť cut-path s najmenším počtom hrán; hodnota je `cp(u, v)`.
- **Min Cut-Path (rozhodovací):** vstup `G, u, v, k`; existuje cut-path `F` s `|F| ≤ k`?
- Motivácia (Č1): komunikácia medzi dôveryhodnými servermi (cesta) a zároveň odrezanie protivníka (rez) – „communication and control“.
- Autor myšlienky: prof. Martin Loebl.

## 2. Notácia

| Symbol | Význam | Poznámka |
|---|---|---|
| `n = \|V\|`, `m = \|E\|` | počet vrcholov, hrán | v sekcii o NP-úplnosti sú `n`, `m` počty premenných a klauzúl; reťaz má `r` článkov |
| `d(u, v)` | vzdialenosť (dĺžka najkratšej cesty) | „min path“ v DP, „shortest path“ v Č1 |
| `c(u, v)` | veľkosť minimálneho `u`–`v` rezu | |
| `cp(u, v)` | hodnota minimálneho cut-path | v Č1 makro `\cp` |
| `CP(u, v)` | množina všetkých cut-paths | v DP `cut-path(u, v)`; v Č1 makro `\CP` |
| `tc(u, v)`, `t(G)` | minimálny tree-cut, veľkosť kostry | len DP |
| `deg(v)`, `deg(v, S)` | stupeň, počet susedov v množine `S` | |
| `δ(S)`, `δ(G)` | rez určený množinou `S`; minimálny stupeň | |
| `G ∖ P` | graf po odstránení hrán cesty `P` | |
| `G(n, p)` | Erdős–Rényiho náhodný graf | |
| `I, J, K, L` | rozklad vrcholov podľa rezu: `I ∪ J = A₁`, `K ∪ L = A₂`; `J, K` majú hranu v reze, `I, L` nie | |
| `G_P` | max independent path graph | len DP, kap. 5 |
| `OPT(x)`, `I(n)`, `I_A^opt(n)` | optimum, množina vstupov veľkosti `n`, vstupy s garanciou | definícia aproximačnej schémy |

Názvy problémov sa sádžu kapitálkami: `\textsc{Min Cut-Path}`, `\textsc{Separating Shortest Path}`, `\textsc{3-SAT}`.

## 3. Mapa výsledkov

| Výsledok | DP 2025 | Č1 | Poznámka |
|---|---|---|---|
| Základný prípad: ak `c = 1` alebo `d = 1`, tak `cp = c + d − 1` | Claim 6 | Lemma `lem:basic-bounds` (II.4), druhá časť | |
| Hranice `max(c, d) ≤ cp ≤ c + d − 1` | Claim 7 | Lemma `lem:basic-bounds` (II.4) | do Č1 doplnené 7. 10. 2026 |
| Zjednotenie min. rezu a najkratšej cesty je 2-aproximácia | Claim 8 | – | |
| `min cp(u,v) = min c(u,v)` cez hrany `{u,v} ∈ E` | Theorem 9 | – | |
| Partial Path / Partial Cut Property (známa cesta resp. rez z optima ⇒ polynomiálne riešenie) | Theorem 10, 11 | – | základ algoritmu Path-Cut |
| Tree-cut: `tc(u,v) = t(G)` v neváženom grafe; vo váženom neplatí | Theorem 4, 5 | – | |
| Rozklad `I, J, K, L` podľa rezu | Claim 12 (+ Algorithm 1) | Lemma `lem:cut-decomposition` | |
| Priemer 2 ⇒ `I = ∅` alebo `L = ∅` | Claim 13 | Lemma `lem:empty-i-or-l` | |
| Každá `u`–`v` cesta pretína každý `u`–`v` rez v nepárnom počte hrán | Claim 14 | Lemma `lem:odd-intersection` | platí pre rez tvaru `δ(A₁)` |
| **Priemer 2 ⇒ `cp = c + d − 1`** | Theorem 15 | Theorem `thm:diameter-two` (IV.5) | |
| Priemer 2 ⇒ `c(u,v) = min(deg u, deg v)` | Theorem 16 | – | |
| `c(x,y) ≤ 2` pre všetky páry ⇒ kaktusová štruktúra | Claim 17 | odsek pred vetou V.1 | |
| **`c(x,y) ≤ 2` pre všetky páry ⇒ `cp = c + d − 1`** | Theorem 18 | Theorem `thm:cut-two` (V.1) | dôkaz doplnený 7. 10. 2026 |
| Trieda *diam or cut 2*; vzorec `cp = c + d − 1` v nej neplatí (protipríklady) | Def. 37, obr. 3.3 | len v závere ako ďalší smer | |
| General path, square graph, general square graph, pseudo-square graph | Def. 38–41 | – | |
| Rozklad na general square graph pre `c(u,v) = 2` | Theorem 20 (Alg. 2–5) | – | |
| Polynomiálny výpočet `cp` v *diam or cut 2* pre `c(u,v) = 2` | Theorem 22 (Alg. 6) | – | prípad `d(u,v) = 2` ostáva otvorený |
| Lineárny `O(\|E\|)` výpočet pri danom rozklade | Theorem 23 (Alg. 7) | – | |
| `G(n, 1/α)`, `α > 1`, má takmer iste priemer 2 | Theorem 24 (s dôkazom; v DP `α > 0`) | Theorem `thm:random-diameter-two` (VI.1), citácia Bollobás | |
| Vlastnosti `G(n, α log n / n)`, `α > 1`: súvislosť, priemer | Theorem 25, 26 | `thm:random-connectivity`, `thm:random-diameter` | Theorem 27 (najväčší komponent) je len v DP |
| Stupne vrcholov | Theorem 28: všetky v `(1 ± ε) α log n` – **neplatí** pre pevné `α` | Lemma `lem:degree-bounds` (VI.4): všetky v `[β₁ log n, β₂ log n]` | pozri časť 5a |
| Hranice pre `c(u,v)` | Claim 29 (s `(1 ± ε) α log n`) | Lemma `lem:connectivity-bounds` (VI.5) s `β₁, β₂` | |
| **Average (1+ε)-Approximation Scheme** pre `p ≥ α log n / n` | Theorem 30 | Theorem `thm:approximation-scheme` (VI.6) | v Č1 doplnený argument monotónnosti |
| Almost polynomial average-case algoritmus (Path-Cut) | Theorem 31 (Alg. 8) | – | |
| Pre `α < 1` je `cp(u,v)` definované s pravdepodobnosťou → 0 | Claim 32 | – | |
| Symetrický prípad `c = d = cp`: symmetric cut-path graph, max independent path graph | Def. 47, 48; Claim 33–36 | – | až `2^{O(√n)}` rôznych optím (Claim 35) |
| Filter-BFS, Local-Cut; polynomiálne pre nearly 5-regular grafy | Alg. 9–12; Theorem 37, 38 | – | |
| **NP-úplnosť \textsc{Separating Shortest Path}** (redukcia z 3-SAT, reťaz a vlákna) | – | Theorem `thm:ssp-np-complete` (III.5), `alg:reduction` | nové oproti DP; dôkaz prepísaný 7. 10. 2026 |
| **NP-úplnosť rozhodovacej verzie \textsc{Min Cut-Path}** | – (v DP otvorený problém) | Theorem `thm:mcp-np-complete` (III.6) | redukcia `G' = G`, `k = d_G(u,v)`; optimalizačná verzia je NP-hard |

## 4. Čo je v ktorom texte navyše

**Len v DP** (materiál pre ďalšie články):
- kapitola 2: tree-cut, 2-aproximácia, globálne minimum, partial path/cut property;
- kapitola 3.3: celá teória *diam or cut 2* a rozkladu na general square graph;
- kapitola 4.5: almost polynomial average-case algoritmus pre riedke náhodné grafy;
- kapitola 5: symetrický prípad `c = d = cp`, algoritmy Filter-BFS a Local-Cut.

**Len v Č1:**
- NP-úplnosť cez medziproblém \textsc{Separating Shortest Path};
- gadgety: chain link (cyklus s dvoma rovnako dlhými `p`–`q` cestami, kladná a záporná), chain s `r` článkami, thread, threading, crossing edge;
- typy článkov reťaze: initialization `I_i`, terminal `T_i`, literal `L_{j,k,i}` (`j` = pozícia literálu, `k` = klauzula, `i` = premenná; spolu `3m + 2n`);
- typy vlákien: 2-synchronization, 3-synchronization, clause thread;
- pomocné procedúry `BuildChain(u, v, r)`, `Thread(u, v, [(L, σ), …])` (vytvára aj *connecting paths*) a `Calibrate(G)`;
- pojmy dôkazu: *chain path*, chain path *hits* a thread, *consistent* chain path, *unused path* článku, *dead end*;
- kostra dôkazu korektnosti: (1) po kalibrácii sú najkratšie `u`–`v` cesty práve chain paths, (2) oddeľujúca cesta musí zasiahnuť každé vlákno, (3) synchronizačné vlákna ⇒ konzistentné znamienka ⇒ pravdivostné ohodnotenie, (4) klauzulové vlákno je zasiahnuté ⇔ klauzula je splnená, (5) pre spĺňajúce ohodnotenie je komponent vrcholu `u` v `G ∖ P` bez `v`.

## 5. Rozdiely medzi DP a Č1 (pozor pri preberaní textu)

| Téma | DP | Č1 |
|---|---|---|
| Zložitosť všeobecného prípadu | NP-ťažkosť je otvorený problém | dokázaná NP-úplnosť |
| Množina cut-paths | `cut-path(u, v)` | `CP(u, v)` |
| Pomocné tvrdenia | `Claim` | `Lemma` (labely `lem:…`) |
| Podmnožiny v definícii | `A` (rez), `B` (cesta) | `C` (rez), `P` (cesta) |
| Členenie | kapitoly (`Chapter`) | sekcie |
| Bibliografia | ISO 690, 8 položiek (viaceré s chybami, pozri `knowledge/sources/README.md`) | natbib číselne, 12 overených položiek vrátane DP |
| Definícia cut-path | podmnožiny `A` (rez), `B` (cesta) | podmnožiny `C`, `P`; rámčeky problémov formulované rovnako ako definícia |
| Stupne v `G(n, α log n / n)` | koncentrácia `(1 ± ε) α log n` | konštantné hranice `β₁ log n`, `β₂ log n` |

## 5a. Chyby zistené v DP (dôležité pre článok 2)

Článok 2 sa bude pripravovať z diplomovej práce. Tieto miesta sa nesmú preberať bez opravy:

1. **Theorem 28 (Degree Concentration) a Claim 29**: tvrdenie, že pre `p = α log n / n` s pevným `α > 1` a ľubovoľným pevným `ε > 0` ležia všetky stupne v `(1 ± ε) α log n`, neplatí. Stupeň je binomický so strednou hodnotou `μ ≈ α log n`; `P[deg ≤ aμ] ≈ n^{−α h(a)}`, `h(a) = a ln a − a + 1`, takže po zjednotení cez `n` vrcholov to ide k nule len pre `α h(a) > 1`. Minimálny a maximálny stupeň sú preto `≈ a₁ α log n` a `≈ a₂ α log n` s konštantami `a₁ < 1 < a₂` závislými od `α`. Správna formulácia je v Č1 (`lem:degree-bounds`). Theorem 30 (aproximačná schéma) ostáva v platnosti, lebo potrebuje len `c(u,v) ≥ β₁ log n`.
2. **Theorem 24**: `p = 1/α` vyžaduje `α > 1` (nie `α > 0`).
3. **Theorem 27 (Largest Component)** je formulovaná pre `α > 1`, ale používa sa v Claim 32 pre `α < 1` – `TODO(overiť)` znenie aj zdroj.
4. **Úvod a záver DP** uvádzajú NP-ťažkosť ako otvorený problém – po Č1 už neplatí.
5. **Bibliografia DP**: nesprávne ISBN (Diestel, Cormen, Godsil–Royle, Frieze–Karoński, Roughgarden), Diestel 6. vydanie je z roku 2025, OpenIntro Statistics 4. vydanie je z roku 2019, položka 7 má autorov Blanc, Lange, Qiao, Tan. Opravené záznamy: `knowledge/bibliography/references.bib`.
6. **Definície 44–46** (average-case) merajú vstupy rovnomerne (`|I_opt| / |I|`), kým vety sú o `G(n, p)` – treba formulovať cez pravdepodobnosť.
7. Jazykové a formálne chyby rovnakého typu ako v pôvodnom Č1 (kontrolný zoznam: `knowledge/writing/academic-style.md`).

## 5b. Príbuzné problémy v literatúre

V Č1 ani v DP nie sú spomenuté; pri ďalšej úprave Č1 a v článku 2 ich treba uviesť (záznamy sú v `knowledge/bibliography/references.bib`).

| Problém | Vzťah k Min Cut-Path | Zdroj |
|---|---|---|
| *Non-separating st-path*: `s`–`t` cesta, po odstránení ktorej hrán ostane graf súvislý; existencia NP-ťažká na všeobecných grafoch, polynomiálna na chordálnych | zrkadlový pojem k Separating Shortest Path (tam odstránenie cesty musí `u` a `v` oddeliť) | Mao, arXiv:2101.03519 (overené) |
| Priemer riedkych náhodných grafov: `(1 + o(1)) log n / log(np)` | presný zdroj pre Theorem VI.2 v Č1 (Theorem 26 v DP) | Chung, Lu 2001 (čiastočne overené) |
| Interdikcia najkratších ciest, „most vital edges“, Force Path Cut (odstraňovanie hrán tak, aby sa zmenila najkratšia cesta) | iná kombinácia rezov a najkratších ciest; treba dohľadať a overiť konkrétne práce | `TODO(overiť)` – zatiaľ len z výsledkov vyhľadávania |

Poznámka pre texty: ak platí `cp = c + d − 1`, zjednotenie ľubovoľného minimálneho rezu a ľubovoľnej najkratšej cesty je minimálny cut-path (Č1, Remark IV.6).

## 6. Otvorené problémy a smery

Z DP a zo záveru Č1:
1. Trieda *diam or cut 2*: prípad `d(u, v) = 2` (DP rieši len `c(u, v) = 2`); v Č1 formulované ako zlúčenie dvoch polynomiálnych „ostrovov“.
2. Rovinné grafy (dualita rez ↔ cyklus), grafy s ohraničenou stromovou šírkou.
3. Aproximačné algoritmy s garanciou pre všeobecné grafy (známa je len triviálna 2-aproximácia).
4. Vážené a orientované varianty.
5. Experimentálne vyhodnotenie na reálnych a náhodných sieťach.
6. Štruktúra grafov s pevnou hodnotou `cp(u, v)`.
7. Ďalšie „islands of polynomial-time solvability“.

## 7. Plánované rukopisy

Rozhodnutie autora (7. 10. 2026): **článok 2 sa bude vyrábať z diplomovej práce** (projekt `projects/clanok-2-min-cut-path/`, zatiaľ prázdny). LaTeX zdroj DP v repozitári nie je – treba ho dodať do `inbox/`, inak sa text prepisuje z PDF. Článok 1 sa neskôr prepíše do šablóny cieľového časopisu (zatiaľ neurčený).

| Názov v CV | Pravdepodobný zdroj v DP (odhad, treba potvrdiť) |
|---|---|
| *Polynomial-Time Solutions for Island Structures in the Min Cut-Path Problem* | kapitola 3 (prípadne aj 5) |
| *Random Graph Models for the Min Cut-Path Problem* | kapitola 4 |

## 8. Slovník

Anglické termíny sú z DP a Č1, české z českého abstraktu DP. Slovenské ekvivalenty sú návrh – ustálená slovenská terminológia pre tento problém neexistuje.

| EN | CZ (abstrakt DP) | SK (návrh) |
|---|---|---|
| cut-path | řezo-cesta | rez-cesta |
| Min Cut-Path | minimální řez-cesta | minimálna rez-cesta |
| edge cut | hranový řez | hranový rez |
| shortest path / min path | nejkratší cesta | najkratšia cesta |
| general path | obecná cesta | všeobecná cesta |
| square graph | čtvercový graf | štvorcový graf |
| general square graph | obecný čtvercový graf | všeobecný štvorcový graf |
| diam or cut 2 graph | graf s průměrem nebo řezem nejvýše dva | graf s priemerom alebo rezom najviac dva |
| nearly k-regular graph | téměř k-regulární graf | takmer k-regulárny graf |
| symmetric cut-path | symetrická řezo-cesta | symetrická rez-cesta |
| tree-cut | – | strom-rez |
| separating shortest path | – | oddeľujúca najkratšia cesta |
| chain, chain link, thread, threading | – | reťaz, článok reťaze, vlákno, navliekanie |
| average (1+ε)-approximation scheme | aproximační schéma s průměrnou zárukou | aproximačná schéma v priemernom prípade |
| almost polynomial algorithm | téměř polynomiální algoritmus | takmer polynomiálny algoritmus |
