# Štýl odborného textu

Cieľový štýl všetkých článkov a dizertácie: moderná, stručná odborná angličtina bez výplne.
Tento súbor hovorí, **ako písať vety a odseky**. Stavba dokumentu je v [paper-structure.md](paper-structure.md),
definície, vety a dôkazy v [math-writing.md](math-writing.md), experimenty v [experiments-reporting.md](experiments-reporting.md),
kontrola pred odovzdaním v [checklist.md](checklist.md).

## 1. Zásada

**Každá veta nesie informáciu, ktorú čitateľ potrebuje na pochopenie alebo overenie výsledku.**
Test: vetu škrtni. Ak čitateľ o nič neprišiel, ostane škrtnutá.

Poradie pri konflikte: správnosť > jednoznačnosť > stručnosť > uhladenosť.
Stručnosť nikdy neodstraňuje predpoklad vety, krok dôkazu, definíciu ani údaj potrebný na zopakovanie experimentu.
Škrtá sa výplň, nie obsah.

## 2. Jazyk

| Vec | Pravidlo |
|---|---|
| Jazyk dokumentov | angličtina, ak autor nepovie inak; s autorom sa komunikuje po slovensky |
| Pravopis | americký (*formalize*, *neighbor*, *behavior*, *modeling*, *labeled*) |
| Osoba | autorské *we*, aj pri jednom autorovi; nie *the author*, nie *one* |
| Rod | činný (*we prove*, *the algorithm returns*); trpný len keď na činiteľovi nezáleží (*the graph is drawn in Figure 2*) |
| Čas: čo článok robí, čo platí | prítomný (*we prove*, *Lemma 3 implies*, *Table 2 shows*) |
| Čas: čo sme urobili v experimente | minulý (*we ran each configuration 30 times*) |
| Čas: cudzia práca | minulý pre udalosť (*Cook proved*), prítomný pre platný výsledok (*3-SAT is NP-complete*) |
| Budúci čas | nepoužíva sa (*we will show* → *we show*) |
| Skrátené tvary | nie (*don't* → *do not*) |
| Nový pojem | pri prvom výskyte `\emph{…}`, potom už nie; úvodzovky sa na pojmy nepoužívajú |
| Názvy problémov | kapitálky cez makro (`\MinCutPath`), všade rovnako |
| Skratky | zavedené raz, pri prvom výskyte; v názve a abstrakte len všeobecne známe (NP, SAT, LLM) |
| *i.e.*, *e.g.* | s čiarkou za nimi; nie na začiatku vety; *cf.* znamená „porovnaj“, nie „pozri“ |

## 3. Desať pravidiel stručnosti

Príklady „pred“ sú z článku 1 (stav 7. 10. 2026).

**1. Výsledok najprv.** Abstrakt, úvod, sekcia aj odsek sa začínajú tým, čo tvrdia; zdôvodnenie nasleduje.

**2. Žiadne kulisy.** Text sa nezačína stavom sveta, ale problémom.

> ✗ *In modern distributed systems, data exchange between servers must often balance two opposing objectives: enabling communication within a trusted domain and preventing communication by potential adversaries.*
> ✓ *A cut-path between vertices $u$ and $v$ is an edge set that contains both a $u$–$v$ path and a $u$–$v$ cut.*

**3. Konkrétne namiesto všeobecného.** Trieda, hranica, číslo, názov – nie ich opis.

> ✗ *we identify two graph classes in which the problem becomes tractable*
> ✓ *we prove $\cp(u,v) = c(u,v) + d(u,v) - 1$ for graphs of diameter two and for graphs in which a minimum cut between any two vertices has at most two edges*

**4. Jedna myšlienka raz.** Definícia je na jednom mieste; ostatné miesta na ňu odkazujú. Príspevky sú v úvode raz – abstrakt ich podáva kratšie, záver ich neopakuje tými istými vetami. Veta, ktorá inými slovami opakuje predchádzajúcu, sa škrtá.

> ✗ *This hybrid structure, which captures both connection and disconnection properties at the same time, will be formally introduced as a cut-path.* (predchádzajúca veta to už povedala)

**5. Sloveso namiesto podstatného mena.** *perform an analysis of* → *analyze*; *give a proof of* → *prove*; *is in agreement with* → *agrees with*.

> ✗ *The interplay between these two objectives---connectivity and control---serves as the conceptual foundation of the present work.*
> ✓ (škrtnúť; veta nič netvrdí)

**6. Žiadna samochvála.** *novel*, *elegant*, *powerful*, *comprehensive*, *extensive*, *state-of-the-art*, *significant* (bez testu) sa nepíšu. Čo je nové, sa povie vecne: tvrdenie, hranica, metóda, porovnanie s citovaným výsledkom.

> ✗ *Graph theory provides an elegant formal framework for representing such systems.*
> ✓ *Vertices are servers and edges are communication links.*

**7. Žiadny text o texte.** *In this section we discuss…*, *We are now ready to state…*, *As mentioned above…*, *It is worth noting that…* sa škrtajú. Ostáva: jeden odsek o stavbe článku na konci úvodu (najviac štyri vety, len ak členenie nie je zrejmé z príspevkov), jedna veta o stratégii pred dlhým dôkazom, odkaz dopredu s číslom (*see Section 5*).

> ✗ *Section 2 introduces the formal definitions, notation, and fundamental concepts used throughout the paper, including the definition of cut-paths and their basic properties.*
> ✓ *Section 2 defines cut-paths and proves $\max\{c,d\} \le \cp \le c+d-1$.*

**8. Neistota len tam, kde je, a len raz.** Dokázané sa tvrdí bez zmäkčenia. Nedokázané sa označí presným slovesom (tabuľka v časti 6). *may possibly suggest* → *suggests*.

**9. Jeden pojem, jedno slovo.** Synonymá pre pestrosť sú v odbornom texte chyba: čitateľ za iným slovom hľadá iný objekt (*shortest path* / *min path* / *geodesic*; *vertex* / *node*; *instance* / *input*). Zvolený termín je v slovníku projektu (`knowledge/research/<tema>.md`).

**10. Číslo namiesto prídavného mena.** *much faster* → *4.2 times faster*; *on many instances* → *on 37 of 50 instances*; *large graphs* → *graphs with $10^6$ edges*.

## 4. Veta

- **Podmet a prísudok pri sebe**, blízko začiatku vety. Dlhá vsuvka medzi nimi sa presunie do samostatnej vety.
- **Známe na začiatok, nové na koniec.** Koniec vety je miesto dôrazu; nasledujúca veta začína tým, čím predchádzajúca skončila. Takto text drží pokope bez spojok.
- **Jedna myšlienka na vetu.** Orientačne 15 – 25 slov; nad 35 sa veta delí. Krátka veta po dlhej je v poriadku; tri dlhé za sebou nie.
- **Kladný tvar:** *does not contain any* → *contains no*; *is not connected* → *is disconnected*, ak je to presné.
- **Paralelná stavba** pre paralelný obsah: položky zoznamu a prípady dôkazu majú rovnaký gramatický tvar.
- **`that` vymedzuje, `which` dopĺňa** (s čiarkou): *the cut that separates $u$ from $v$* vs. *the cut $C$, which has two edges*.
- **Zámeno má jednoznačný odkaz.** *This* na začiatku vety vždy s podstatným menom: *This bound…*, nie *This shows…*, ak nie je jasné, čo.
- **Jeden zdroj, jedno tvrdenie:** citácia stojí pri tvrdení, ktoré podopiera, nie na konci odseku za tromi tvrdeniami.
- **Citácia nie je podstatné meno:** nie *[3] shows* ani *In [3], the authors show*, ale *Gomory and Hu [3] show*. Veta musí dávať zmysel aj po vynechaní zátvorky s citáciou – potom funguje v číselnom aj menno-rokovom štýle každej šablóny.
- **Trojice a dvojice synoným** (*definitions, notation, and fundamental concepts*; *isolate or restrict*) sa krátia na jedno slovo, ktoré platí.

## 5. Odsek

- Prvá veta hovorí, o čom odsek je a čo tvrdí; kto číta len prvé vety odsekov, pochopí líniu článku.
- Jeden odsek, jedna pointa. Odsek s dvoma pointami sa delí; odsek bez pointy sa škrtá.
- Posledná veta odsek nezhŕňa. Ak pointu treba zopakovať, odsek je zle postavený.
- Spojka (*however*, *therefore*, *moreover*, *in contrast*) sa píše len tam, kde medzi vetami je práve ten logický vzťah. *Moreover* a *Furthermore* na začiatku každej druhej vety sú výplň.
- Zoznam s odrážkami len pre položky, ktoré sú naozaj paralelné (príspevky, prípady, kroky). Argument sa píše vetami.
- Odsek o jednej vete je výnimka (prechod medzi veľkými celkami, zvýraznené tvrdenie), nie štýl.

## 6. Sila tvrdenia

Sloveso hovorí, čím je tvrdenie podložené. Silnejšie sloveso bez dôkazu je chyba, slabšie pri dokázanej vete je zbytočná skromnosť.

| Sloveso | Podklad |
|---|---|
| *prove*, *show* | dôkaz je v texte (alebo citovaný) |
| *observe*, *note* | bezprostredný dôsledok definície alebo predchádzajúceho kroku |
| *obtain*, *derive* | výpočet alebo odvodenie |
| *measure*, *find*, *report* | experimentálny výsledok s uvedenými podmienkami |
| *suggest*, *indicate* | dáta podporujú záver, ale nedokazujú ho |
| *conjecture* | veríme tomu, dôkaz nemáme; uvedie sa, na čom sa domnienka zakladá |
| *demonstrate* | len pre experiment alebo príklad, nie pre dôkaz |
| *claim* | v matematike názov prostredia; v texte o cudzej práci znie ako spochybnenie – nepoužívať |

Tvrdenie o novosti (*first*, *has not been studied*) sa píše najviac raz a len po skutočnom prehľadaní literatúry; presnejšie je povedať, čo konkrétne je nové oproti ktorej práci.

## 7. Text, ktorý znie ako písaný LLM

Recenzenti tieto znaky poznajú a text s nimi čítajú s nedôverou, aj keď je obsah správny. Nepíšu sa:

- úvody o stave sveta (*In recent years…*, *With the rapid development of…*, *In modern distributed systems…*);
- slovník: *delve*, *leverage*, *harness*, *underscore*, *showcase*, *pivotal*, *crucial*, *intricate*, *landscape*, *realm*, *seamless*, *comprehensive*, *robust* (mimo technického významu), *notably*, *shed light on*, *pave the way*;
- vety, ktoré len hodnotia (*This highlights the importance of…*, *This dual requirement leads naturally to…*);
- zhrnutie na konci každého odseku (*Overall, …*, *In summary, …*);
- *not only … but also*, trojice prívlastkov, symetrické dvojice (*both connectivity and disconnection*) použité pre rytmus;
- pomlčky ako hlavný spôsob stavby vety – najviac jedna vsuvka s pomlčkami na odsek;
- abstraktné podmety (*the interplay*, *the tension*, *this perspective*) so slovesami *serves as*, *embodies*, *captures*, *reflects*;
- záver, ktorý sľubuje *promising avenues for future research* namiesto konkrétnych otvorených problémov.

Strojová kontrola: `.\scripts\check-text.ps1 -Project <projekt>` hľadá tieto obraty podľa [phrase-list.tsv](phrase-list.tsv).
O povinnosti priznať použitie AI pri písaní: [submission.md](submission.md).

## 8. Úsporné prechody (namiesto ohlasovania)

| Namiesto | Píš |
|---|---|
| *We are now ready to state the main theorem of this section.* | (nič – nasleduje veta) |
| *For better understanding, we provide an illustrative example (see Figure 3).* | *Figure 3 shows a chain with three links.* |
| *Intuitively speaking, one can think of…* | *Intuitively, …* (jedna veta pred formálnou definíciou) |
| *Let us now turn our attention to the case…* | *Case 2: …* / *Suppose now that…* |
| *It is easy to see that $x \le y$.* | *By (3), $x \le y$.* |
| *As we have already mentioned in the introduction, …* | (škrtnúť) alebo *Recall that…*, ak definícia bola dávno |
| *In order to prove the theorem, we will need the following lemma.* | (nič – nasleduje lema) alebo jedna veta, načo lema slúži |
| *The following theorem is the main result of this paper.* | názov vety v hranatej zátvorke: `\begin{theorem}[Diameter two]` |

Povolené a užitočné: *Intuitively,* · *Formally,* · *Recall that* · *Assume for contradiction that* · *Without loss of generality* (len keď je to naozaj bez ujmy a je povedané prečo) · *Conversely,* · *In particular,* · *Suppose first that*.

## 9. Návyky autora

Zistené auditom diplomovej práce a článku 1 (7. 10. 2026). Pri písaní aj korektúre sa hľadajú ako prvé.

<!-- AUDIT:HABITS -->

## 10. Angličtina slovenského autora

<!-- AUDIT:INTERFERENCE -->

## 11. Postup revízie

Text sa kráti zhora nadol; nemá zmysel ladiť vety v odseku, ktorý sa škrtne.

1. **Tvrdenie.** Dá sa hlavný výsledok povedať jednou vetou? Ak nie, problém nie je v štýle.
2. **Sekcie.** Slúži každá sekcia hlavnému tvrdeniu? Čo neslúži, ide do dodatku alebo von.
3. **Odseky.** Prečítaj len prvé vety odsekov: dávajú súvislú líniu? Odsek bez pointy škrtni.
4. **Vety.** Pri každej vete test zo sekcie 1. Potom pravidlá 2 – 10.
5. **Slová.** `.\scripts\check-text.ps1 -Project <projekt>`; každý nález posúď, neopravuj mechanicky.
6. **Kontrolný zoznam.** [checklist.md](checklist.md).
7. **Počty.** Porovnaj počet slov abstraktu, úvodu a celku pred a po; uveď ich v správe autorovi.

Revízia nemení matematický obsah. Ak sa pri krátení ukáže, že tvrdenie je nejasné alebo nesprávne, patrí to do správy autorovi, nie do tichej opravy.

## 12. Zdroje

Pravidlá vychádzajú z týchto príručiek (záznamy sú v `knowledge/bibliography/references.bib`, časť „Písanie“):

<!-- SOURCES -->
