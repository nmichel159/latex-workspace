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
   never edit the staged copy or the zip.
7. **Files** as `knowledge/writing/submission.md` prescribes, by section: 1 AI-use statement; 2 arXiv (when used);
   3 package (procedure 3.2, anonymization 3.3 on the packager's output, frozen copy in `archives/submissions/`);
   4 cover letter; 5 response to reviewers (after reviews; each round gets its own packager run); 6 preprints and
   self-archiving. Form metadata, cover letter and reviews live in `projects/<project>/submission/`.
8. **Report:** card date and open `TODO(verify)` items, checklist result, the packager's command line and its
   `Verdict` line with the findings that remain, the files the owner uploads (the zip and PDF in
   `outputs/<project>/package/`) and where (submission system from the card), steps only the owner can do
   (accounts, ORCID, licence, fees), and the clickable PDF link. Send the PDF with `SendUserFile` when available.
