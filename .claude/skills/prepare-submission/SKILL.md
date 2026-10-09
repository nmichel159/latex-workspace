---
name: prepare-submission
description: Get a manuscript ready for a journal, conference or arXiv (venue card, template, checklist, checks, clean build, submission files) without uploading or sending anything.
---

# Prepare a submission

Use this skill when the owner names a venue (or arXiv) and wants a manuscript ready to submit. It prepares files and
tells the owner what to upload; it never uploads, submits or sends anything.

1. **Venue card.** Read `knowledge/venues/<venue>.md`. If it is missing, or its "Checked" date is older than a month
   (a conference: always), open the venue's pages and create or update the card first
   (`knowledge/venues/README.md`). Facts dated, unknowns `TODO(verify)`.
2. **Template.** The manuscript must be in the venue's class; otherwise skill `port-latex-template`.
   Limits, anonymity and mandatory statements come from the card.
3. **Checklist.** `knowledge/writing/checklist.md`, in full. Fix each item or record it under "Known problems".
4. **Checks.** Run both; resolve every finding or justify it. Every cited entry must be `VERIFIED`; repeat the
   searches of `knowledge/literature/searches.md` that support a novelty claim if older than three months.

   ```powershell
   .\scripts\check-text.ps1 -Project <project>
   .\scripts\check-bib.ps1 -Project <project>
   ```

5. **Clean build.** `.\scripts\build-project.ps1 -Project <project>`; criteria in
   `knowledge/writing/latex-conventions.md`, section 2.
6. **Package.** The source package is made only by the packager (`knowledge/writing/latex-conventions.md`,
   section 1.1; `submission.md` 3.2 step 3); `-MaxPages` and `-Flat` come from the venue card:

   ```powershell
   .\scripts\package-project.ps1 -Project <project> -Template <venue> [-MaxPages <n>] [-Flat]
   ```

   Go on only with `Verdict: PASS`; fix findings in `projects/<project>/` and run it again. Never zip by hand and
   never edit the staged copy or the zip. The findings that guard what leaves the workspace:
   - `[trace]` (fails): a workspace trace (`TODO`, `FIXME`, the user name, a Windows or workspace path, a Claude or
     Anthropic address, a commit trailer) or an AI tool name in a packaged file, a file name, image or PDF metadata,
     the `.bbl` or the zip. Remove it in the project. A tool name belongs only in `sections/91-ai-declaration.tex`;
     an AI name that is research content goes into `submission/package-allow.txt` with a reason. Allowed hits are
     printed as notes: read them.
   - `[template-origin]` (fails): the template folder is not a recorded publisher download in
     `templates/SOURCES.tsv`. Never write a venue template by hand; ask the owner to approve the download.
   - `[ai-declaration]` (reminder) and the line `AI declaration:` before the verdict: the manuscript has no AI
     declaration section; the owner decides whether to insert the draft from `submission/ai-declaration.tex`.

   Rules: `knowledge/writing/latex-conventions.md` section 1.1, point 4.
7. **Files** as `knowledge/writing/submission.md` prescribes, by section: 1 AI-use statement (draft in
   `submission/ai-declaration.tex`, inserted by the owner as `sections/91-ai-declaration.tex`); 2 arXiv (when used);
   3 package (procedure 3.2, anonymization 3.3 on the packager's output, frozen copy in `archives/submissions/`);
   4 cover letter; 5 response to reviewers (after reviews; each round gets its own packager run); 6 preprints and
   self-archiving. Form metadata, cover letter and reviews live in `projects/<project>/submission/`.
8. **Report:** card date and open `TODO(verify)` items, checklist result, the packager's command line and its
   `Trace scan:`, `AI declaration:` and `Verdict` lines with the findings that remain, the files the owner uploads (the zip and PDF in
   `outputs/<project>/package/`) and where (submission system from the card), steps only the owner can do
   (accounts, ORCID, licence, fees), and the clickable PDF link. Send the PDF with `SendUserFile` when available.
