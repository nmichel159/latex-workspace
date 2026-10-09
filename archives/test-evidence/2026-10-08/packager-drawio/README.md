# Packager: hidden text in draw.io figures (2026-10-08)

Test of the change to `scripts/package-project.ps1` made while integrating the trace scan: metadata values of PNG
text chunks are also scanned URL-decoded, and the compressed pages of an embedded draw.io diagram (PNG `tEXt`
chunk `mxfile`, draw.io SVG `content` attribute) are inflated and scanned. Before the change, `%20Claude` in a
URL-encoded chunk was missed (the digit before the word defeats the word boundary) and text inside a compressed
page was not visible at all. The six figures of article 1 carry such a chunk (draw.io exports with "Include a copy
of my diagram").

Repeat from PowerShell in the workspace root, with the packager before the change copied into `scripts/`:

```powershell
Copy-Item archives\test-evidence\2026-10-08\packager-drawio\inputs\package-project-before-drawio.ps1 scripts\zz-before.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File archives\test-evidence\2026-10-08\packager-drawio\run-drawio-test.ps1 -Old scripts\zz-before.ps1
Move-Item scripts\zz-before.ps1 tmp\
```

| Path | Content |
|---|---|
| `run-drawio-test.ps1` | driver: copies `projects/clanok-1-min-cut-path` to `projects/zz-packager-drawio-test`, plants the fixtures, runs `-CheckOnly` with both packagers, moves the copy to `tmp/packager-drawio-test/` |
| `make-drawio-fixtures.ps1` | fixtures: `chain-link.png` with a URL-encoded `mxfile` whose agent string names Claude; `chain.png` with a compressed page whose only label names Anthropic; `img/drawio-test.svg`, a draw.io SVG whose compressed page names ChatGPT |
| `inputs/package-project-before-drawio.ps1` | the packager before the change (SHA-256 `a7bca300...`, the trace-scan version tested in `../packager-trace/`) |
| `outputs/drawio-before.txt`, `outputs/drawio-after.txt`, `results.txt` | the two runs |

## Results

| Case | Expected | Observed |
|---|---|---|
| before the change | the three hidden terms are missed | `Verdict: PASS`, `Trace scan: 21 files, 0 hits` |
| after the change | one `[trace]` FAIL per fixture | `Verdict: FAIL (trace)`, `Trace scan: 21 files, 3 hits`: `Anthropic` in `chain.png`, `Claude` in `chain-link.png`, `ChatGPT` in `drawio-test.svg`, each "decoded" |
| regression: `../packager-trace/run-tests.ps1` with the changed packager as `-New` (run from a copy in `tmp/`) | `results.txt` identical to the one in `../packager-trace/` | identical line by line; the hit lists of `t1`, `t2`, `t5` and `o-template-origin` are identical too |
| article 1, `-Template els-cas -Flat` | `Verdict: PASS`; its six real `mxfile` chunks decoded without a hit | as expected (project `README.md`, "Build") |

## Note (appended 2026-10-09)

Re-run with the packager as changed after the reviews of 2026-10-08 (from a copy in `tmp/`): `results.txt`
identical to the one here. Outputs and the change: [../packager-review/](../packager-review/README.md).
