---
name: port-latex-template
description: Move an existing manuscript into a journal or conference LaTeX template (class from inbox/ or templates/), rebuild it and report with the PDF link.
---

# Port a manuscript to a venue template

Use this skill when the owner names a target journal or conference for an existing project, drops a venue template
into `inbox/`, or asks to switch a project to another class. The full procedure, the class quirks table and the
porting log format are in `knowledge/writing/template-porting.md`; read it first.

1. **Template and card.** The template is the publisher's own download, never hand-made, reconstructed or taken
   from a third-party copy (Overleaf gallery, an old project). Find the link on the venue's guide for authors (or on
   the publisher's LaTeX page that the guide points to); ask the owner before downloading, naming the file, URL and
   size. File it with skill `process-inbox`, section "Venue template": original zip in `archives/`, row in
   `templates/SOURCES.tsv` (URL, linking page, SHA-256, date), pristine folder `templates/<venue>/`, venue card. A
   template the owner drops into `inbox/` goes the same way. If `templates/` already holds a folder for the venue,
   use it only when its `SOURCES.tsv` row is of kind `venue`. Never edit `templates/<venue>/`. Read the card
   `knowledge/venues/<venue>.md` (page limit, anonymity, AI policy, bibliography style, sub-folders allowed).
2. **Missing class.** `kpsewhich --miktex-disable-installer <class>.cls`. If the class is neither in MiKTeX nor in the
   template folder, ask the owner before any install; never run a bare `pdflatex` or `kpsewhich`.
3. **Snapshot.** Build the project once with `.\scripts\build-project.ps1 -Project <project>` and record page count
   and warnings; copy `main.tex` to `archives/removed-from-projects/<project>/main-before-port-<date>.tex`.
4. **Port** (`template-porting.md`, procedure steps 3-8; section 6 lists the quirks of the target class): copy the
   class, `.bst` and support files into the project unmodified and move the old class's files to
   `archives/removed-from-projects/<project>/`; write the new wrapper `main.tex` from the template's sample
   file; map the front matter; adapt `preamble/` (remove only what clashes with the class, keep packages the class
   loads too so that `preamble/` stays portable, rename clashing environments, keep what the old class loaded and
   the text uses, e.g. `microtype`; list labels as `[(a)]`, not `enumitem`: `template-porting.md` sections 3 and
   6.3); undo the venue-only markup that an earlier port's log lists (section 1, step 2) and adapt a class that
   reads standard markup differently in the wrapper, not in `sections/` (cas-sc: key alias `H`); switch the
   bibliography style; fix layout consequences (two columns; a narrower text block). Never edit a venue file and
   never override the venue's layout (conformance: `template-porting.md`, section 1). Do not touch the wording,
   statements or proofs in `sections/`; a reference macro may be changed (`\ref` -> `\cref`) only when the owner
   asked for it, a citation macro only as `template-porting.md` section 4 prescribes for an author-year venue, and
   layout-only edits (column fractions, figure widths, split displays: section 5) only without changing a word;
   log each one.
5. **Build** with `.\scripts\build-project.ps1 -Project <project>` (check first that no `latexmk`/`pdflatex` process
   is running). Fix every error; then check the log for undefined references, multiply defined labels, overfull lines,
   font substitutions and the class's own warnings, and compare `pdftotext -layout` of the old and the new PDF: a
   leaked option (`label=(a)`) or a doubled period (`..`) leaves no warning (`template-porting.md`, section 6.3).
   Run `.\scripts\check-bib.ps1 -Project <project>` and the template's checklist (sample file, author guide, venue
   card).
6. **Package**, the proof that the port conforms (`knowledge/writing/latex-conventions.md`, section 1.1). `-MaxPages`
   and `-Flat` come from the venue card (page limit, left out when the card states none; system that builds from
   one directory):

   ```powershell
   .\scripts\package-project.ps1 -Project <project> -Template <venue> -CheckOnly                 # while fixing
   .\scripts\package-project.ps1 -Project <project> -Template <venue> [-MaxPages <n>] [-Flat]    # done on Verdict: PASS
   ```

   Fix every finding in `projects/<project>/` and run it again; never edit the staged copy or the zip. A page count
   over `-MaxPages` fails the verdict. The `[layout]` list is fixed (font packages and overrides written another way
   are not found): read the wrapper for those. `[template-origin]` fails unless the template folder is a recorded
   download. `[trace]` fails on anything sent that names this workspace or an AI tool (section 1.1, point 4):
   comments or `.bib` notes naming workspace files, `TODO` markers, local paths, tool names, image metadata. Remove
   them in the project. The AI declaration stays a draft in `submission/ai-declaration.tex` until the owner inserts
   it as `sections/91-ai-declaration.tex` (`knowledge/writing/submission.md` §1.3); the packager reminds of it on
   every run (`[ai-declaration]` note, `AI declaration:` line).
7. **Record** the porting log block in the project `README.md` (Change history), the packager's verdict included,
   and list remaining problems under "Known problems".
8. **Report**: venue and class version, what changed (files and places), what was removed from `preamble/` and why,
   page count before and after, remaining warnings, open items from the template checklist, the packager's command
   line and its `Template origin:`, `Trace scan:` and `Verdict` lines with the findings that remain, and the clickable link
   `[outputs/<project>/main.pdf](outputs/<project>/main.pdf)`. Send the PDF with `SendUserFile` when available.
   If the build or the packager failed, say so, quote the error and do not present a stale PDF or zip as current.
9. Submission is next: skill `prepare-submission`.
