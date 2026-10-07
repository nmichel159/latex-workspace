# Šablóny

Východiská pre nové projekty. Šablóny sa neupravujú – nový projekt vznikne skopírovaním do `projects/<projekt>/`.

| Priečinok | Na čo | Pôvod | Hlavný súbor |
|---|---|---|---|
| `new-aiaa/` | článok | trieda a štýl bibliografie z článku 1 (Overleaf, `new-aiaa.cls` v1.2); `main.tex` je kostra s autorovou preambulou | `main.tex` |
| `altacv/` | životopis | čistý obsah `archives/CV.zip` (AltaCV 1.7.x, vzorové CV `sample.tex`) | `sample.tex` |

## Nový projekt zo šablóny

```powershell
Copy-Item -Recurse templates\new-aiaa projects\clanok-2-<tema>
.\scripts\build-project.ps1 -Project clanok-2-<tema>
```

Potom v projekte vytvor `README.md` (vzor: `projects/clanok-1-min-cut-path/README.md`) a doplň riadok do tabuľky projektov v koreňovom `README.md` a `CLAUDE.md`.

## Stav

- `new-aiaa/main.tex` sa kompiluje (overené 7. 10. 2026). Kým kostra neobsahuje žiadnu citáciu, BibTeX hlási
  „I found no \citation commands“ – po prvom `\cite` to zmizne.
- Šablóna pre dizertačnú prácu UPJŠ chýba. Oficiálnu šablónu (zip alebo priečinok) vlož do `inbox/`.
