# Stavba článku

Čo má byť v ktorej časti, v akom poradí a čo tam nepatrí. Štýl viet: [academic-style.md](academic-style.md).
Limity strán, povinné časti a šablónu určuje cieľové miesto publikovania – jeho karta je v [../venues/](../venues/README.md).

## 1. Pred prvou vetou

Tieto štyri veci sa zapíšu do `projects/<projekt>/README.md` (časť „Zámer“) skôr, než vznikne text. Bez nich sa nepíše.

| Otázka | Tvar odpovede |
|---|---|
| **Hlavné tvrdenie** | jedna veta, ktorú si má čitateľ zapamätať (*Min Cut-Path is NP-complete, but $\cp = c + d - 1$ in graphs of diameter two.*) |
| **Príspevky** | 2 – 4 overiteľné tvrdenia, každé s miestom v texte (veta, tabuľka) |
| **Najbližšia práca** | ktorý publikovaný výsledok je najbližšie a v čom presne sa líšime |
| **Čitateľ a miesto** | komu je text určený, kam sa posiela, limit rozsahu |

Poradie písania: (1) znenia viet, tabuľky a obrázky, (2) jadro – dôkazy a experimenty, (3) úvod, (4) záver, (5) abstrakt, (6) názov. Úvod písaný ako prvý sa po dokončení jadra vždy prepisuje.

## 2. Typy textov

| Typ | Kostra | Na čo sa pozerá recenzent |
|---|---|---|
| **Teoretický článok do časopisu** (teória grafov, zložitosť, algoritmy) | Introduction (problém, výsledky, súvisiace práce) → Preliminaries → sekcia na výsledok → Concluding remarks s otvorenými problémami | správnosť a úplnosť dôkazov, novosť oproti literatúre, čistota formulácií |
| **Konferenčný článok TCS** (LIPIcs, LNCS) | to isté v limite strán; v úvode *Our results* a *Technical overview*; plné dôkazy v dodatku alebo v plnej verzii na arXive | sila výsledku, zrozumiteľný prehľad techniky v hlavnom texte |
| **Experimentálny článok** (LLM pri návrhu algoritmov, heuristiky, ML) | Introduction s príspevkami → Related work → Method → Experimental setup → Results → Limitations → Conclusion; dodatok s promptmi, nastaveniami a ďalšími tabuľkami | poctivé porovnanie, opakovateľnosť, primeranosť záverov k dátam |
| **Výpočtová štúdia** (algorithm engineering, OR) | Introduction → Problem and prior algorithms → Algorithm → Computational study → Conclusion | testovacie inštancie, baseline, čas a kvalita, dostupnosť kódu |
| **Rozšírený abstrakt** (konferencia bez zborníka plných textov) | 1 – 4 strany: problém, definícia, znenia výsledkov, jedna myšlienka dôkazu, literatúra | jasné znenie výsledku |
| **Prehľadový článok** | otázka a rozsah → metóda výberu prác → taxonómia → porovnanie → otvorené problémy | úplnosť, triedenie, vlastný pohľad |
| **Dizertácia** | [thesis.md](thesis.md) | |

Zmiešaný článok (teória + experiment, typické pre tému dizertácie): teoretická časť sa píše podľa prvého riadku, experimentálna podľa tretieho; úvod uvedie oba druhy príspevkov oddelene.

## 3. Názov

- Hovorí, **čo** sa skúma a **čo** sa zistilo; do 12 slov; bez vzorcov a bez neštandardných skratiek.
- Nezačína sa *On*, *A Study of*, *Towards*, *Some Remarks on*; neobsahuje *novel*, *efficient* bez miery, *new approach*.
- Dvojbodka len vtedy, keď druhá časť nesie výsledok: *Min Cut-Path: NP-Completeness and Polynomial Cases* (ukážka tvaru, názov článku určuje autor).
- Kľúčové slová a klasifikácia (MSC 2020, ACM CCS) podľa požiadaviek miesta publikovania; kľúčové slová neopakujú slová z názvu.

## 4. Abstrakt

Jeden odsek, 100 – 200 slov (platí limit miesta publikovania). Bez citácií, bez odkazov na sekcie, bez nedefinovaných symbolov, bez viet o motivácii, ktoré by sedeli pred ľubovoľný článok.

| Veta | Obsah |
|---|---|
| 1 | objekt alebo problém – ak je nový, jeho definícia jednou vetou |
| 2 | hlavný výsledok, presne (trieda, hranica, zložitosť, číslo) |
| 3 – 4 | ďalšie výsledky v poradí dôležitosti |
| 5 (voliteľne) | metóda, ak je sama osebe prínosom |
| 6 (voliteľne) | dôsledok alebo otvorená otázka |

Ukážka pre článok 1 (návrh tvaru; zdroj článku sa ním nemení):

> A cut-path between two vertices $u$ and $v$ of a graph is a set of edges that contains both a $u$–$v$ path and a $u$–$v$ cut. We study Min Cut-Path, the problem of finding a cut-path with the fewest edges; its size is denoted $\mathrm{cp}(u,v)$. We prove that the decision version is NP-complete by a reduction from 3-SAT through an intermediate problem, Separating Shortest Path. In contrast, $\mathrm{cp}(u,v) = c(u,v) + d(u,v) - 1$ in graphs of diameter two and in graphs in which a minimum cut between any two vertices has at most two edges, where $c$ is the minimum cut size and $d$ the distance; in both classes the union of any minimum cut and any shortest path is optimal. As a consequence, Min Cut-Path is solvable in polynomial time on almost all dense Erdős–Rényi graphs, and for $p \ge \alpha \log n / n$ with $\alpha > 1$ the same union is asymptotically optimal with high probability.

Súčasný abstrakt článku 1 má podobný rozsah a neuvádza ani jeden výsledok.

## 5. Úvod

Úvod odpovedá na päť otázok, v tomto poradí. Každá má vlastný odsek alebo podsekciu; nič iné v úvode nie je.

| # | Otázka | Rozsah | Poznámka |
|---|---|---|---|
| 1 | **Aký je problém?** | 1 odsek | presná, hoci neformálna definícia; malý príklad alebo obrázok; žiadne kulisy |
| 2 | **Prečo na ňom záleží a čo je o ňom známe?** | 1 – 2 odseky | konkrétna motivácia a najbližšie známe výsledky s citáciami; čo ostáva otvorené |
| 3 | **Čo dokazujeme alebo ukazujeme?** | zoznam alebo podsekcia *Our results* | každý príspevok je overiteľné tvrdenie s odkazom na vetu, tabuľku alebo sekciu |
| 4 | **Ako?** | 1 – 3 odseky, voliteľne *Technical overview* | hlavná myšlienka najťažšieho dôkazu alebo metódy; čo je na nej iné než v predchádzajúcich prácach |
| 5 | **Ako článok súvisí s ostatnými prácami?** | odsek alebo sekcia *Related work* | vrátane vlastných predchádzajúcich textov (diplomová práca, konferenčný abstrakt) a vyhlásenia, čo je oproti nim nové |

Odsek o členení článku (*The paper is organized as follows*) je voliteľný: najviac štyri vety a každá hovorí, čo sekcia **dokazuje**, nie že existuje. Ak príspevky v bode 3 odkazujú na sekcie, odsek sa vynecháva.

**Zoznam príspevkov.** Položka začína slovesom podloženým textom (*We prove*, *We give an $O(m)$ algorithm*, *We evaluate on 50 instances*). Nepatria doň *we study*, *we discuss*, *we provide insights*. V teoretickom článku môžu byť hlavné vety v úvode uvedené celým znením (*Theorem 1.1*) a v jadre sa zopakujú s tým istým číslom (`thm-restate`) alebo sa na ne odkáže.

**Vzťah k diplomovej práci.** Ak článok preberá výsledky z diplomovky, úvod to povie jednou vetou a prácu cituje; nové výsledky sú označené ako nové. Tvrdenia prevzaté z DP sa preberajú až po kontrole proti zoznamu chýb v `knowledge/research/min-cut-path.md`, časť 5a.

## 6. Súvisiace práce

- Triedi sa **podľa myšlienky alebo otázky**, nie práca po práci a nie chronologicky.
- Každá skupina prác končí vetou o rozdiele: čo oni, čo my.
- Cituje sa pôvodný zdroj výsledku, nie učebnica, ktorá ho opakuje; učebnica sa cituje pre štandardné pojmy a notáciu.
- Publikovaná verzia má prednosť pred preprintom ([../bibliography/README.md](../bibliography/README.md)).
- Tvrdenie „doteraz neskúmané“ sa opiera o zapísané hľadanie: kľúčové slová, databázy a dátum sú v `knowledge/literature/`.
- Cudzia práca sa opisuje presne a vecne; kritika mieri na výsledok, nie na autorov.
- Umiestnenie: v teoretickom článku v úvode; v experimentálnom ako sekcia 2 alebo pred záverom, podľa zvyku miesta publikovania.

## 7. Preliminaries

- Len pojmy a označenia, ktoré sa naozaj použijú; štandardné veci odkazom na jednu učebnicu.
- Dohody na začiatku (*All graphs are finite, simple, and undirected*).
- Nový pojem sa definuje tam, kde ho čitateľ prvý raz potrebuje; do Preliminaries patrí len to, čo používajú aspoň dve sekcie.
- Formulácia problému v rámčeku (`problem`): *Input / Question* pre rozhodovaciu verziu, *Input / Output* pre optimalizačnú.
- Pri viac než približne 15 symboloch tabuľka označení (v článku v dodatku, v dizertácii vpredu).

## 8. Jadro

Jedna sekcia na jeden výsledok. Sekcia sa začína výsledkom alebo jednou vetou o ňom; nezačína sa ohlásením.

| Druh výsledku | Osnova sekcie |
|---|---|
| Štrukturálna veta | myšlienka (1 odsek) → pomocné lemy tesne pred použitím → veta → dôkaz → poznámka o tesnosti alebo protipríklad |
| Ťažkosť (NP-úplnosť) | problém, z ktorého redukujeme → konštrukcia s obrázkom → veľkosť a čas konštrukcie → oba smery ekvivalencie → príslušnosť do NP |
| Algoritmus | myšlienka → pseudokód → korektnosť → zložitosť → (príklad behu) |
| Pravdepodobnostný výsledok | model a parametre → použité nerovnosti s citáciou → veta s presným významom „with high probability“ → dôkaz |
| Experiment | [experiments-reporting.md](experiments-reporting.md) |

Podrobnosti zápisu: [math-writing.md](math-writing.md).

Čo do hlavného textu nepatrí: rutinné výpočty, ďalšie prípady analogické s ukázaným, plné tabuľky, prompty – idú do dodatku s odkazom.

## 9. Diskusia a obmedzenia

V experimentálnom článku samostatná časť *Limitations*: na akých inštanciách a pri akom rozpočte výsledky platia, čo sa netestovalo, čo môže byť dôsledkom úniku dát alebo voľby modelu. V teoretickom článku sú obmedzenia súčasťou znení viet (predpoklady) a záveru (čo ostáva otvorené).

## 10. Záver

- Jeden až tri odseky. Nie je to abstrakt v minulom čase a neopakuje zoznam príspevkov.
- Hovorí, čo je teraz známe, čo nie a prečo; ak výsledky niečo spája, patrí to sem.
- **Otvorené problémy sú konkrétne**, v teoretickom článku číslované a formulované ako otázky alebo domnienky (*Is Min Cut-Path polynomial on planar graphs?*), nie *several interesting directions remain*.
- Žiadny nový výsledok, žiadna nová citácia okrem tých pri otvorených problémoch.

## 11. Koniec dokumentu

| Časť | Obsah |
|---|---|
| Acknowledgments | osoby (za čo), grant s číslom presne podľa požiadaviek poskytovateľa; bez tučného písma |
| Vyhlásenia | podľa miesta publikovania: dostupnosť kódu a dát, konflikt záujmov, príspevok autorov, použitie generatívnej AI ([submission.md](submission.md)) |
| Dodatky | vynechané dôkazy, plné tabuľky, prompty, nastavenia; každý dodatok je spomenutý v hlavnom texte |
| Literatúra | len citované práce; pravidlá v [../bibliography/README.md](../bibliography/README.md) |

## 12. Rozdelenie rozsahu

Orientačne pre článok bez limitu strán; pri limite sa kráti jadro presunom dôkazov do dodatku, nie úvod pod zrozumiteľnosť.

| Časť | Podiel |
|---|---|
| Úvod vrátane súvisiacich prác | 10 – 15 % |
| Preliminaries | 5 – 10 % |
| Jadro | 65 – 80 % |
| Záver | do 5 % |

Úvod dlhší než pätina článku takmer vždy obsahuje kulisy alebo opakovanie.

## 13. Z diplomovej práce do článku

1. Vyber výsledok a jeho závislosti (mapa výsledkov v `knowledge/research/<tema>.md`); článok nie je skrátená práca, ale jeden príbeh.
2. Skontroluj tvrdenia proti zoznamu známych chýb práce.
3. Prepíš, neskracuj: úvod a motivácia sa píšu nanovo podľa časti 5; výklad známych základov sa nahradí odkazom.
4. Zjednoť terminológiu a notáciu s článkom (*chapter* → *section*, *Claim* → *Lemma*, makrá).
5. Cituj prácu a v úvode uveď, čo je prevzaté a čo nové.
6. Over si pravidlá miesta publikovania o texte založenom na záverečnej práci.

Opačný smer (články → dizertácia): [thesis.md](thesis.md).
