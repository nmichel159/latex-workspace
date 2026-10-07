# Štýl odborného textu

Zhrnutie toho, ako sú stavané autorove texty (diplomová práca, článok 1), a kontrolný zoznam chýb, ktoré sa v nich opakujú.
Cieľ: nový text má znieť ako ten istý autor, ale bez týchto chýb.

## 1. Jazyk

- Články a dizertácia: angličtina, americký pravopis (*formalize*, *neighbor*, *behavior*).
- Bakalárska práca a dokumentácia tohto repozitára: slovenčina.
- Autorské „we“ (*we prove*, *we show*, *we introduce*), prítomný čas.
- Názvy problémov kapitálkami (`\textsc{Min Cut-Path}`), nové pojmy pri prvom výskyte kurzívou (`\emph{cut-path}`).

## 2. Stavba článku (podľa článku 1)

1. **Abstract** – motivácia jednou-dvoma vetami, potom čo sa formalizuje a čo sa dokazuje.
2. **Introduction** – (a) motivácia z praxe, (b) grafový model, (c) príbuzné problémy s citáciami, (d) definícia hlavného problému a čo je nové, (e) príspevky ako číslovaný sled (*Firstly … Secondly … Finally …*), (f) odsek o štruktúre článku s odkazmi na sekcie.
3. **Fundamentals** – notácia, definície, formulácia problému v rámčeku.
4. **Výsledky** – jedna sekcia na jeden výsledok; pred každou vetou odsek, ktorý povie, prečo veta platí; potom veta a dôkaz.
5. **Conclusion** – zhrnutie výsledkov, potom smery ďalšieho výskumu (každý smer vlastný odsek).
6. **Acknowledgment**, bibliografia.

## 3. Stavba záverečnej práce (podľa diplomovky)

Introduction (motivácia, ciele ako odrážky, prínos po kapitolách, štruktúra práce) → Foundations (grafy, algoritmy, pravdepodobnosť) →
Fundamentals of the problem → špeciálne triedy grafov → náhodné grafy → špeciálny prípad → Conclusion (zhrnutie v odrážkach, otvorené problémy) →
Bibliography → List of Figures / Tables / Abbreviations → Attachments.

Dôkaz algoritmickej vety má pevnú osnovu: **1. Correctness**, **2. (Minimality)**, **3. Polynomial-Time Complexity** s rozpisom krokov.

## 4. Typické obraty

- Prechod k definícii: *Intuitively, … Formally:* / *More precisely:*
- Uvedenie vety: *We are now ready to state the central theorem of this section:*
- Ilustrácia: *For better understanding, we provide an illustrative example (see Figure~…).*
- Dôkaz sporom: *Assume for contradiction that …*
- Skratky: *w.l.o.g.*, *i.e.*, *e.g.* (s čiarkou za nimi).

## 5. Kontrolný zoznam pred odoslaním

Každý bod zodpovedá chybe, ktorá sa v článku 1 alebo v diplomovej práci naozaj vyskytla (čo sa opravilo, je v `projects/clanok-1-min-cut-path/README.md`).

**Pozostatky z iného dokumentu**
- [ ] V článku nie je *chapter*, *thesis*, *Chapter 3* – len *section*, *paper*.
- [ ] Žiadny odsek neodkazuje na obrázok, vetu alebo pojem, ktorý v dokumente nie je (v PDF hľadaj `??`).
- [ ] Notácia je všade rovnaká (`CP(u,v)`, nie miestami `cut-path(u,v)`).

**Konzistencia**
- [ ] Názov prostredia sedí s textom odkazu (lema sa necituje ako *Claim*).
- [ ] *Lemma*, *Theorem*, *Section*, *Figure* pred `\ref` s veľkým písmenom a s `~`.
- [ ] Rovnaký pojem má všade rovnaký názov (*shortest path* vs. *min path*).
- [ ] Definícia v texte a formulácia v rámčeku problému hovoria to isté.
- [ ] Jedno písmeno neznamená dve veci (`m` = počet hrán aj počet klauzúl).
- [ ] Indexy toho istého objektu majú všade rovnaké poradie (`L_{j,k,i}`).
- [ ] Nadpis sekcie zodpovedá jej obsahu.

**Matematika**
- [ ] Optimalizačný problém je *NP-hard*, rozhodovací *NP-complete*.
- [ ] Predpoklady vety sedia s predpokladmi použitých liem (`p = …` vs. `p ≥ …`, `α > 0` vs. `α > 1`).
- [ ] Kvantifikátory sa nemiešajú s limitou (*for all n > n₀* a zároveň `lim`).
- [ ] Každá veta má dôkaz alebo citáciu.
- [ ] V pseudokóde sedia zátvorky.
- [ ] Veta prevzatá z literatúry hovorí to isté čo zdroj (pozor na „pre každé `ε`“ pri koncentračných odhadoch).
- [ ] Rez v tvrdení je buď „množina hrán, ktorej odstránenie oddelí `u` a `v`“, alebo `δ(A)` – parita a rozklady platia len pre druhý typ.
- [ ] Písmeno pre množinu alebo objekt nekoliduje s označením hodnoty (`c(u,v)` je číslo, nie rez).

**Sadzba**
- [ ] Operátory so spätnou lomkou (`\deg`, `\min`, `\max`, `\log`, `\lim`).
- [ ] `\[ … \]` namiesto `$$ … $$`; žiadne osamotené `\Bigr.`.
- [ ] Premenné v texte v matematickom režime (`$p$`, nie `(p)`).
- [ ] Každý obrázok má `\caption` a je spomenutý v texte.
- [ ] Značka konca dôkazu nie je osamotená na riadku (`\qedhere`) a „Proof.“ nie je prilepené k algoritmu.

**Jazyk**
- [ ] Preklepy a zdvojené slová (*egde*, *prove show*, *the this*).
- [ ] Neurčitý člen (*an average*, nie *a Average*); veľké písmeno len na začiatku vety a vo vlastných menách.
- [ ] Vsuvky oddelené pomlčkami alebo čiarkami (*two objectives – connectivity and control – serve*).
- [ ] Žiadna veta bez podstatného mena na konci (*for large random graphs*).

**Bibliografia**
- [ ] Všetky citované kľúče existujú a v PDF nie je `[?]`.
- [ ] Časopis, ročník a strany sedia s DOI; ISBN má platnú kontrolnú číslicu.
- [ ] Citovaná práca naozaj obsahuje to, čo sa jej pripisuje.
- [ ] Vlastná predchádzajúca práca je citovaná, ak sa na ňu text opiera.
