# Poznámky k literatúre

Čo sme z cudzích prác naozaj prečítali a čo z nich používame. Účel: každé tvrdenie o literatúre v rukopise
sa dá vystopovať k poznámke s miestom v zdroji, a porovnanie so súvisiacimi prácami sa nepíše spamäti.

## Čo kde je

| Súbor | Obsah |
|---|---|
| `<Kluc>.md` | poznámka k jednej práci; názov súboru je kľúč z `knowledge/bibliography/references.bib` |
| [searches.md](searches.md) | záznam hľadaní v literatúre: dátum, kde, dopyt, čo sa našlo |
| [_template.md](_template.md) | vzor poznámky |
| `../sources/papers/<Kluc>.pdf` | plný text práce, ak ho autor dodal (+ `.txt` z `pdftotext`) |
| `../research/<tema>.md` | mapa témy: triedenie prác, čo je známe, čo otvorené |

Poznámka patrí práci, o ktorú sa niektorý text opiera (používa jej vetu, porovnáva sa s ňou, preberá definíciu).
Práca citovaná len pre štandardný pojem poznámku nepotrebuje.

## Pravidlá

- Poznámka sa píše vlastnými slovami; doslovný citát najviac jeden a krátky, s číslom strany.
- Pri každom výsledku je **miesto v zdroji** (Theorem 3.2, s. 14) a **stav čítania** (celé / časť / len abstrakt).
  Z práce, z ktorej je prečítaný len abstrakt, sa do rukopisu nepreberá žiadne presné tvrdenie.
- Odlišná notácia alebo definícia oproti našim textom sa zapíše výslovne – pri preberaní výsledku je to najčastejší zdroj chýb.
- Časť „Rozdiel oproti našej práci“ je jedna až dve vety po anglicky, použiteľné v sekcii Related work.
- Tvrdenie o novosti (*has not been studied*) v rukopise vyžaduje záznam v `searches.md` nie starší než tri mesiace pred odoslaním.
- Neoverený údaj má značku `TODO(overiť)`.

## Postup pri novej práci

1. Záznam do `references.bib` podľa [../bibliography/README.md](../bibliography/README.md).
2. Ak je k dispozícii PDF: `knowledge/sources/papers/<Kluc>.pdf` a text `pdftotext -layout -enc UTF-8`.
3. Poznámka `<Kluc>.md` podľa vzoru.
4. Doplnenie mapy témy v `knowledge/research/<tema>.md` (kam práca patrí, čo mení).
