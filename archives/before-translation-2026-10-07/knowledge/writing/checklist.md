# Kontrolný zoznam

Prechádza sa po každom napísanom alebo upravenom celku a celý pred odovzdaním. Body označené ● zodpovedajú chybe,
ktorá sa v článku 1 alebo v diplomovej práci naozaj vyskytla. Pravidlá za bodmi: [academic-style.md](academic-style.md),
[paper-structure.md](paper-structure.md), [math-writing.md](math-writing.md), [experiments-reporting.md](experiments-reporting.md).

Strojová časť kontroly: `.\scripts\check-text.ps1 -Project <projekt>` (frázy, dĺžka viet, hygiena LaTeXu).

## Stavba

- [ ] Hlavné tvrdenie sa dá povedať jednou vetou a je v abstrakte aj v úvode.
- [ ] ● Abstrakt uvádza výsledky (triedy, hranice, čísla), nie len motiváciu; bez citácií a nedefinovaných symbolov.
- [ ] Každý príspevok v úvode je overiteľné tvrdenie s odkazom na vetu, tabuľku alebo sekciu.
- [ ] ● Úvod porovnáva s najbližšími publikovanými prácami; tvrdenie o novosti je podložené hľadaním.
- [ ] Vzťah k vlastným predchádzajúcim textom (diplomová práca, abstrakt z konferencie) je uvedený a citovaný.
- [ ] ● Nadpis sekcie zodpovedá jej obsahu.
- [ ] Záver neopakuje úvod; otvorené problémy sú konkrétne otázky.

## Stručnosť

- [ ] Prvé vety odsekov dávajú po sebe súvislú líniu článku.
- [ ] ● Žiadna definícia ani tvrdenie nie je v texte dvakrát.
- [ ] ● Žiadna veta len neohlasuje nasledujúcu vetu, definíciu alebo sekciu.
- [ ] Žiadne kulisy na začiatku abstraktu, úvodu a sekcií.
- [ ] Žiadne hodnotiace prídavné mená o vlastnej práci.
- [ ] `check-text.ps1` nemá nález v kategóriách `filler`, `hype`, `ai-tic`, ktorý by nebol vedome ponechaný.

## Pozostatky z iného dokumentu

- [ ] ● V článku nie je *chapter*, *thesis*, *Chapter 3* – len *section*, *paper*.
- [ ] ● Žiadny odsek neodkazuje na obrázok, vetu alebo pojem, ktorý v dokumente nie je (v PDF hľadaj `??`).
- [ ] ● Notácia je všade rovnaká (`CP(u,v)`, nie miestami `cut-path(u,v)`).

## Konzistencia

- [ ] ● Názov prostredia sedí s textom odkazu (lema sa necituje ako *Claim*).
- [ ] ● *Lemma*, *Theorem*, *Section*, *Figure* pred odkazom s veľkým písmenom a nezlomiteľnou medzerou (alebo `\cref`).
- [ ] ● Rovnaký pojem má všade rovnaký názov (*shortest path* vs. *min path*).
- [ ] ● Definícia v texte a formulácia v rámčeku problému hovoria to isté.
- [ ] ● Jedno písmeno neznamená dve veci (`m` = počet hrán aj počet klauzúl).
- [ ] ● Indexy toho istého objektu majú všade rovnaké poradie (`L_{j,k,i}`).
- [ ] Pravopis je jednotne americký.

## Matematika

- [ ] ● Optimalizačný problém je *NP-hard*, rozhodovací *NP-complete*.
- [ ] ● Predpoklady vety sedia s predpokladmi použitých liem (`p = …` vs. `p ≥ …`, `α > 0` vs. `α > 1`).
- [ ] ● Kvantifikátory sa nemiešajú s limitou (*for all n > n₀* a zároveň `lim`).
- [ ] ● Každá veta má dôkaz alebo citáciu.
- [ ] ● V pseudokóde sedia zátvorky a premenné sú tie isté ako v texte.
- [ ] ● Veta prevzatá z literatúry hovorí to isté čo zdroj (pozor na „pre každé `ε`“ pri koncentračných odhadoch).
- [ ] ● Rez v tvrdení je buď „množina hrán, ktorej odstránenie oddelí `u` a `v`“, alebo `δ(A)` – parita a rozklady platia len pre druhý typ.
- [ ] ● Písmeno pre množinu alebo objekt nekoliduje s označením hodnoty (`c(u,v)` je číslo, nie rez).
- [ ] Každá veta sa dá citovať samostatne (obsahuje svoje predpoklady).
- [ ] *With high probability* a asymptotické symboly majú v dokumente jednu definíciu.

## Experimenty

- [ ] Každý experiment odpovedá na otázku uvedenú v texte.
- [ ] Sú uvedené: inštancie a ich zdroj, baseline s rovnakým rozpočtom, počet behov, rozptyl, hardvér, čas.
- [ ] Pri LLM: presný identifikátor modelu a dátum prístupu, parametre vzorkovania, prompty (v dodatku), počet volaní a tokenov, cena.
- [ ] Tabuľka alebo graf sa dá pochopiť z popisu bez čítania textu; osi majú názvy a jednotky.
- [ ] Záver z experimentu netvrdí viac, než dáta ukazujú; obmedzenia sú pomenované.
- [ ] Kód a dáta sú dostupné alebo je povedané, prečo nie.

## Sadzba

- [ ] ● Operátory so spätnou lomkou (`\deg`, `\min`, `\max`, `\log`, `\lim`).
- [ ] ● `\[ … \]` namiesto `$$ … $$`; žiadne osamotené `\Bigr.`.
- [ ] ● Premenné v texte v matematickom režime (`$p$`, nie `(p)`).
- [ ] ● Každý obrázok má `\caption` a je spomenutý v texte.
- [ ] ● Značka konca dôkazu nie je osamotená na riadku (`\qedhere`) a „Proof.“ nie je prilepené k algoritmu.
- [ ] Tabuľky bez zvislých čiar (`booktabs`); čísla zarovnané na desatinnú čiarku.
- [ ] V PDF nie je `??`, `[?]` ani riadok pretečený do okraja.

## Jazyk

- [ ] ● Preklepy a zdvojené slová (*egde*, *prove show*, *the this*).
- [ ] ● Neurčitý člen (*an average*, nie *a Average*); veľké písmeno len na začiatku vety a vo vlastných menách.
- [ ] ● Vsuvky oddelené pomlčkami alebo čiarkami (*two objectives – connectivity and control – serve*).
- [ ] ● Žiadna veta bez podstatného mena na konci (*for large random graphs*).
- [ ] Členy pred podstatnými menami v jednotnom čísle (*the graph*, *a path*); nepočítateľné podstatné mená bez množného čísla (*information*, *research*, *work*).

## Bibliografia

- [ ] ● Všetky citované kľúče existujú a v PDF nie je `[?]`.
- [ ] ● Časopis, ročník a strany sedia s DOI; ISBN má platnú kontrolnú číslicu.
- [ ] ● Citovaná práca naozaj obsahuje to, čo sa jej pripisuje.
- [ ] ● Vlastná predchádzajúca práca je citovaná, ak sa na ňu text opiera.
- [ ] Preprint je nahradený publikovanou verziou, ak existuje.
- [ ] Každý záznam v projekte pochádza z `knowledge/bibliography/references.bib` a má tam stav `OVERENE`.

## Pred odoslaním

- [ ] Šablóna, rozsah, štýl citácií a povinné vyhlásenia zodpovedajú karte miesta publikovania (`knowledge/venues/`).
- [ ] Projekt sa skompiluje z čistého priečinka bez varovaní o odkazoch a citáciách.
- [ ] Autor skontroloval body z časti „Obsahové zmeny na kontrolu“ v `README.md` projektu.
- [ ] Vyhlásenie o použití AI je pripravené podľa pravidiel vydavateľa ([submission.md](submission.md)).
- [ ] V zdroji neostal `TODO`, `\fillin`, zakomentovaný starý text ani poznámky pre spoluautorov.
