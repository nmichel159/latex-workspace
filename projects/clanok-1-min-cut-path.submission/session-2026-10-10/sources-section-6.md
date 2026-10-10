# Sources for Section 6 of article 1 and two further citations

Session 2026-10-10. Nothing in `projects/clanok-1-min-cut-path/main.tex`, its `references.bib`, `knowledge/` or
`searches.md` was edited; this report holds ready-to-paste proposals.

## Summary

| Q | What | Verdict | Proposed citation |
|---|---|---|---|
| Q1 | Theorem 6.1, constant p, diameter 2 | no numbered statement for constant p found in either book; FK Exercise 1.4.8 states exactly the claim; Bollobas Theorem 10.10 (p. 259) + monotonicity (p. 262) imply it (read first-hand) | `\cite[Theorem~10.10]{Bollobas2001}` with a 3-line proof, or `\cite[Exercise~1.4.8]{Frieze2016}`; see Q1 |
| Q2 | Theorem 6.2, p = alpha log n / n | VERIFIED first-hand in two authors' PDFs of Chung-Lu: Theorem 4 (p. 15 of 22); journal numbering NOT VERIFIED; Bollobas gives no such bound | `\cite{ChungLu2001}` only; `\cite[Theorem~4]{ChungLu2001}` after the journal PDF is seen |
| Q3 | Theorem 6.3, kappa = lambda = delta | VERIFIED first-hand: Bollobas 2001, Sect. 7.2, p. 169 (remark crediting Bollobas-Thomason 1985, "without any restriction on p"); Theorem 7.6 itself does NOT cover alpha > 1; FK has no such theorem; Bollobas-Thomason NOT read | `\cite[p.~169]{Bollobas2001}` (drop `Frieze2016` there) |
| Q4 | Chernoff, Lemma 6.4 | VERIFIED first-hand (FK printed Eq. (21.19), p. 392); JLR Thm 2.1 not opened | `\cite[Eq.~(21.19)]{Frieze2016}` |
| Q5 | monotone coupling | VERIFIED first-hand (FK printed Sect. 1.1: (1.3) p. 5, (1.6) p. 7) | `\cite[Section~1.1]{Frieze2016}` |
| Q6 | year of FK | VERIFIED first-hand: imprint page says "First published 2016" | keep `year = {2016}` |
| Q7 | NP-completeness of 3-SAT (exactly 3 literals) | Karp 1972 VERIFIED first-hand but states "at most 3" (pp. 94-95, 98); Cook 1971 Thm 2 re-read (Turing "P-reducible", "at most three", no "NP-complete"); Garey-Johnson NOT VERIFIED (no preview) | `\cite[pp.~94--95, 98]{Karp1972Reducibility}` for the at-most-three form; Garey-Johnson only after it is opened |

Conventions: "PDF-2026" = the authors' PDF https://www.math.cmu.edu/~af1p/BOOK.pdf (revised version dated
2026-08-07, 854 pages, 38 chapters); "printed" = the Cambridge University Press book (22 chapters). The numbering of
the two differs, and the article cites the printed book, so all locations below that go into the article are the
printed ones.

## How the sources were opened

- WebFetch of https://www.math.cmu.edu/~af1p/BOOK.pdf saves the binary file; the text was extracted locally with
  `pdftotext -layout` (`tmp/sources-2026-10-10/FK-authors-2026-08-07.txt`). The same was done for the two Chung-Lu
  PDFs, the Riordan-Wormald PDF and the Karp reprint; Karp (scan) and Cook (scan) were rendered to PNG with
  `pdftoppm` and read as images (`tmp/sources-2026-10-10/karp-pages/`, `cook-pages/`). `tmp/` is disposable.
- Printed pagination of Frieze-Karonski: Google Books preview of the e-book edition, id `Bh7QCgAAQBAJ`, opened page
  by page in the browser pane (`https://books.google.com/books?id=Bh7QCgAAQBAJ&pg=PA<page>`); the running heads show
  the printed page numbers and the contents match Cambridge Core (Ch. 7 pp. 110-137, Ch. 21 pp. 386-409). Not every
  page is in the preview (p. 115 is not).
- Bollobas 2001: Google Books preview, id `o9WecWgilzYC` (same URL pattern); pages not in the preview: 252, 255-256,
  260, 263, 268, 170-171, 271, 460-468 (checked pages: 161, 166, 168, 169, 251, 253, 254, 257, 258, 259, 262, 264,
  267, 269, 276, 459).
- Blocked, not bypassed: a Google Books full-text search (`q=`) and ScienceDirect (HTTP 403 for fetches, Cloudflare
  "Are you a robot?" page in the browser pane). The Karp PDF of the University of Athens exceeds the fetch limit
  (10 MB); a reprint on the University of Maryland site was used instead.

---

## Q1. Theorem 6.1: for constant 0 < p < 1, diam G(n,p) = 2 with high probability

Verdict: the exact statement as a numbered theorem or corollary was NOT found in Bollobas 2001 (pp. 255-256 and 263
are not in the preview, so it may be there); first-hand material that states or implies it:

1. Frieze-Karonski, **Exercise 1.4.8** (printed p. 17; PDF-2026 p. 18): "Suppose that 0 < p < 1 is constant. Show
   that w.h.p. G_{n,p} has diameter two." It is an exercise, so a weak citation for a theorem; its text is exactly
   the claim.
2. Frieze-Karonski, **Theorem 7.1** (printed p. 110; PDF-2026 p. 121): d >= 2 fixed, p^d n^{d-1} = log(n^2/c):
   P(diam = d) -> e^{-c/2}, P(diam = d+1) -> 1 - e^{-c/2}. For d = 2 this is the threshold p ~ sqrt(2 log n / n);
   constant p is not stated. (PDF-2026 pp. 323-324 calls "diam <= 2" a property with sharp threshold
   sqrt(2 log n / n), "see Theorem 7.1".)
3. Bollobas 2001, **Theorem 10.10**, p. 259 (Section 10.2, "The Diameter of G_p"): let c > 0 be constant, d = d(n) >= 2,
   p = p(n,c,d) with p^d n^{d-1} = log(n^2/c) and pn/(log n)^3 -> infinity; then lim P(diam G = d) = e^{-c/2} and
   lim P(diam G = d+1) = 1 - e^{-c/2}. The proof on p. 262 finishes with exactly the two ingredients needed for
   constant p: for d = 2, P(diam G_p <= 1) = P(G_p = K_n) = p^{C(n,2)} -> 0; and "since the property of having
   diameter at most k is monotone, by Theorem 2.1 if 0 < p_1 < p_2 < 1 then P(diam G_{p_1} <= k) <= P(diam G_{p_2} <= k)".
   Bollobas does not write out the constant-p case in the pages I could open.
4. Not seen: page 263 (probably the corollary after Theorem 10.10) and pp. 255-256. Do not cite a "Corollary 10.11".

Derivation of Theorem 6.1 from item 3 (all steps use verified statements; a possible proof for the article, the
author's decision): fix constant p_0 in (0,1) and c > 0. For c fixed the d = 2 threshold p_c = sqrt(log(n^2/c)/n)
satisfies p_c n/(log n)^3 -> infinity and p_c < p_0 for large n. By Theorem 10.10, P(diam G(n,p_c) <= 2) >= P(diam = 2)
-> e^{-c/2}; by monotonicity P(diam G(n,p_0) <= 2) >= P(diam G(n,p_c) <= 2). Hence liminf P(diam G(n,p_0) <= 2)
>= e^{-c/2} for every c > 0, so the liminf is 1. Finally P(diam G(n,p_0) <= 1) = p_0^{C(n,2)} -> 0.

Proposed LaTeX (choose one):

- Cite the source of the proof: `\begin{theorem}[\cite[Theorem~10.10]{Bollobas2001}]` is inaccurate as it stands
  (the theorem is for p near sqrt(2 log n/n)); with the proof above the honest form is
  `\begin{theorem}` ... `\end{theorem}` followed by `\begin{proof}` containing the derivation, citing
  `\cite[Theorem~10.10]{Bollobas2001}` and monotonicity (`\cite[Section~1.1]{Frieze2016}` or Theorem 2.1 of
  Bollobas, page not checked).
- Short form without a proof: `have diameter two with high probability~\cite[Exercise~1.4.8]{Frieze2016}`, and
  the header `\begin{theorem}[\cite[Exercise~1.4.8]{Frieze2016}]` (an exercise, as stated above).
- TODO(verify): the place in Bollobas 2001 that states the constant-p case (pp. 255-256, 263, a Chapter 10 exercise
  on pp. 276-281, or an example in Chapter 2); needs a copy of the book.

---

## Q2. Theorem 6.2: p = alpha log n / n, alpha > 1, diam <= log n / log log n w.h.p.

Verdict: authors' PDFs VERIFIED first-hand (Theorem 4); journal numbering and page NOT VERIFIED.

- https://fanchung.ucsd.edu/dia.pdf (22 pages, file dated 2004-02-11, title "The Diameter of Sparse Random Graphs",
  17 references). Section 4 "The main theorems" and **Theorem 4** are on p. 15: "If p >= c log n / n for some
  constant c, then" (ceilings omitted in the extracted text) log(cn/11)/log(np) <= diam(G(n,p)) <=
  log((33c^2/400) n log n)/log(np) + 2 floor(1/c) + 2 almost surely; the diameter is concentrated on at most
  2 floor(1/c) + 4 values. Theorem 5: if log n > np -> infinity, diam = (1+o(1)) log n / log np. Theorems 2, 3:
  concentration on two values for c > 8, on three for c > 2.
- https://www.math.cmu.edu/~af1p/Teaching/WWW2004/diameter.pdf (22 pages, dated 2000-08-29, earlier draft titled
  "The Diameter of Random Sparse Graphs"): identical Theorems 2-4; Theorem 5 there says "np -> infinity" without
  the bound log n > np.
- Journal: Crossref record of 10.1006/aama.2001.0720 (https://api.crossref.org/works/10.1006/aama.2001.0720): vol. 26,
  issue 4, pp. 257-279, May 2001, PII S0196885801907201, 17 references (the same number as in dia.pdf), Elsevier
  open-access licence from 2013-07-17. The PDF itself could not be opened (see "Blocked"). I could not determine
  the journal page of Theorem 4; do not guess it.
- Conclusion on numbering: "Theorem 4" in both authors' PDFs; the journal numbering is probably the same but is
  not verified.

Does Theorem 4 give the article's bound? Re-derived: for c = alpha > 1, floor(1/alpha) = 0 and
diam <= log((33 alpha^2/400) n log n)/log(alpha log n) + 2 = log n/(log log n + log alpha) + O(1). Since
log n/log log n - log n/(log log n + log alpha) = log n log alpha/(log log n (log log n + log alpha)) -> infinity,
diam <= log n/log log n for all large n. The article's theorem is a corollary of Theorem 4 (case p = alpha log n/n),
not Theorem 4's text.

Bollobas 2001: Theorem 10.10 (p. 259) requires pn/(log n)^3 -> infinity, so it does not cover p = alpha log n / n.
Section 10.4 "Graph processes" (from p. 267) concerns the diameter at the hitting time of connectedness
(p ~ log n / n); its main theorem is on p. 268 (not in the preview). The only statement I saw about
pn - log n -> infinity is secondary: Chung-Lu's introduction credits Bollobas 1984 ("The evolution of sparse
graphs") with at most four values and refers to "[8] exercise 2, chapter 10" (first edition) for np/log n -> infinity.
So there is no verified location in Bollobas 2001: cite Chung-Lu only. Frieze-Karonski Theorem 7.2 (printed p. 114;
PDF-2026 p. 125; p = omega log n / n, omega -> infinity, diam ~ log n / log np) needs omega -> infinity, so it does not
cover constant alpha either.

Proposed LaTeX:

- Header: `\begin{theorem}[Diameter~\cite{ChungLu2001}]` (remove `Bollobas2001`); the sentence before it:
  `...on the diameter and on the edge connectivity~\cite{ChungLu2001,Bollobas2001}` (Bollobas for connectivity, Q3).
- With a location once the journal PDF has been seen: `\cite[Theorem~4]{ChungLu2001}`. Until then I recommend
  the citation without a location (a wrong number is worse than none).

---

## Q3. Theorem 6.3: p = alpha log n / n, alpha > 1, edge connectivity = minimum degree w.h.p.

Verdict: the article's citation `Frieze2016` is wrong. First-hand source found: Bollobas 2001, Section 7.2; the
statement for this regime is a remark crediting Bollobas and Thomason 1985, whose chapter was NOT read.

Bollobas, *Random Graphs*, 2nd ed., Section 7.2 "The k-Connectedness of Random Graphs" (printed pages read):

- p. 166: kappa(G) vertex connectivity, lambda(G) edge connectivity; hitting times; "Trivially tau{delta(G) >= k}
  <= tau{kappa(G) >= k}"; the equality for almost every graph process "was proved by Bollobas and Thomason (1985) for
  every function k = k(n), 1 <= k <= n-1, but here we prove it only in the case when k is constant". **Theorem 7.4**
  (p. 166): for k fixed, a.e. process has tau(delta >= k) = tau(kappa >= k).
- p. 168: **Theorem 7.6**: "If p(n) <= (log n + k log log n)/n for some fixed k, then
  P{kappa(G_p) = lambda(G_p) = delta(G_p)} -> 1." This does NOT cover p = alpha log n / n with alpha > 1, because
  alpha log n > log n + k log log n for large n.
- p. 169, directly after Theorem 7.6: "In fact, Theorem 7.6 holds without any restriction on p, as shown by Bollobas
  and Thomason (1985)." This is the statement that covers p = alpha log n/n with alpha > 1 (and includes the edge
  connectivity lambda). It is a remark in a textbook that attributes the proof to the 1985 paper. Theorem 7.8 (p. 169,
  Bollobas 1981) concerns fixed p.
- Reference of "Bollobas and Thomason (1985)" in the book's list: not seen (pp. 460-468 not in the preview).

Frieze-Karonski (PDF-2026 text searched for "edge connectivity", "vertex connectivity", kappa, lambda): no theorem
states kappa = lambda = delta (or lambda = delta) for G(n,p). Theorem 4.3 (PDF-2026 p. 71) is k-connectivity at
m = n/2 (log n + (k-1) log log n + c_n) with k fixed; Exercise 4.3.1 is the hitting-time equality for k fixed;
Theorem 22.2 (kappa = lambda = delta = k) is for the k-out model G_{k-out}; the book never cites "Random graphs of
small order". So `Frieze2016` does not support Theorem 6.3 and must be removed from it.

Bollobas-Thomason 1985, "Random graphs of small order", in *Random Graphs '83*, North-Holland Mathematics Studies 118,
pp. 47-97, Elsevier, DOI 10.1016/S0304-0208(08)73612-0: records opened = Crossref (chapter; ISBN 9780444878212;
editors not listed) and the University of Memphis repository (https://digitalcommons.memphis.edu/facpubs/5564; abstract:
results on random graphs with few vertices, "a large number of tables"; link to ScienceDirect only). Full text not
reachable. Whether the connectivity theorem is in this chapter is known only from Bollobas p. 169 (and secondary
papers); mark TODO(verify) and read the chapter before citing it.

Proposed LaTeX:

- `\begin{theorem}[Connectivity~\cite[p.~169]{Bollobas2001}]` and `...on the diameter and on the edge connectivity~\cite{ChungLu2001,Bollobas2001}`.
  A page is used because the statement is a remark, not a numbered theorem. Do not cite Theorem 7.6 (it does
  not cover alpha > 1).
- Adding `BollobasThomason1985` to the citation (the original source, per `knowledge/bibliography/README.md` section 8)
  waits until the entry is VERIFIED; a PARTIAL entry may not go into a submitted manuscript.

---

## Q4. Chernoff bound of Lemma 6.4: P(X <= a mu) <= exp(-mu h(a)), h(a) = a log a - a + 1

Verdict: VERIFIED first-hand in Frieze-Karonski. Janson-Luczak-Rucinski Theorem 2.1: NOT opened.

- Printed (Google Books preview, Section 21.4 "Sums of independent bounded random variables", pp. 391-392): setting on
  p. 391 (S_n = X_1 + ... + X_n independent, 0 <= X_i <= 1, mu = E S_n); on p. 392, phi(x) = (1+x) log(1+x) - x for
  x >= -1; (21.17) P(S_n >= mu + t) <= e^{-mu phi(t/mu)}; (21.18); **(21.19)** `P(S_n <= mu - t) <= e^{-mu phi(-t/mu)}`
  (the sentence before (21.18) says "for 0 <= t <= mu"); (21.20); Theorem 21.6 (Chernoff/Hoeffding) with the weaker
  exp{-t^2/(2(mu - t/3))} as (21.22).
- PDF-2026: (34.17) and **(34.19)** p. 707, Theorem 34.6 p. 708 (Section 34.4).
- Why it is the article's bound: t = (1-a) mu with 0 < a < 1 gives phi(-t/mu) = phi(a-1) = a log a - a + 1 = h(a), hence
  P(S_n <= a mu) <= exp(-mu h(a)); a binomial variable is such an S_n. Theorem 21.6 gives only the quadratic bound.
- Proposed LaTeX: `By the Chernoff bound (see, e.g.,~\cite[Eq.~(21.19)]{Frieze2016}),`.

---

## Q5. Monotone coupling of G(n,p1), G(n,p2), p1 <= p2 (proof of Theorem 6.6)

Verdict: VERIFIED first-hand in Frieze-Karonski.

- Printed, Section 1.1 "Models and Relationships": p. 5, the coupling: for p_1 < p define p_2 by
  1 - p = (1 - p_1)(1 - p_2), **(1.3)**; then G(n,p) = G(n,p_1) union G(n,p_2) with the two graphs independent, and
  G(n,p_1) subseteq G(n,p) means "the two graphs are coupled". p. 7: "From the coupling argument it follows that if P is
  a monotone increasing property then, whenever p < p' or m < m'", P(G(n,p) in P) <= P(G(n,p') in P) as **(1.6)**
  (and (1.7) for G(n,m)). The definition of a monotone increasing property (closed under adding an edge) is in the
  same section, p. 6 or 7 (p. 6 not opened).
- PDF-2026: (1.3) p. 5; the monotonicity statement is (1.7) on p. 7. Note the number shift (1.6)/(1.7).
- Use in the article: "diam <= log n/log log n" and "c(u,v) >= beta_1 log n for all pairs" are preserved by adding
  edges, i.e. monotone increasing in the book's sense, so a w.h.p. statement at p = alpha log n/n holds for every larger p.
- Proposed LaTeX: `(see, e.g.,~\cite[Section~1.1]{Frieze2016})` (the section number is the same in print and in
  the authors' PDF), or with equations `\cite[Eqs.~(1.3) and~(1.6)]{Frieze2016}` (printed numbering).

---

## Q6. Year of the printed Frieze-Karonski book

Verdict: VERIFIED first-hand.

- Imprint page of the printed hardback (Google Books preview, id `OVC2CgAAQBAJ`, page iv,
  https://books.google.com/books?id=OVC2CgAAQBAJ&pg=PR4): "(c) Alan Frieze and Michal Karonski 2016", "First
  published 2016", "Printed in the United Kingdom by Clays, St Ives plc", "Information on this title:
  www.cambridge.org/9781107118508".
- Other records (secondary): Cambridge Core (https://www.cambridge.org/core/product/identifier/9781316339831/type/book)
  lists 26 October 2015 (hardback) and 5 November 2015 (online) and "Print publication year 2015"; Open Library
  (record OL28577829M, from the Library of Congress MARC batch of 2016): publish_date 2015, LCCN 2015022579, call numbers
  `QA166.17 .F75 2015` and `.F75 2016`; Palacky University Olomouc and Santa Clara University catalogues and the
  Mathematical Gazette review: 2016. The Library of Congress catalogue page itself could not be rendered.
- Conclusion: the book's own imprint says 2016 (copyright and first publication); the publisher's metadata dates the
  release to late 2015 (my inference: a book released in late October carries the next year on its imprint).
- Proposal: keep `year = {2016}`; replace the 2026-10-08 note (see (b) below).

---

## Q7. NP-completeness of 3-SAT with exactly three literals per clause (line 308 of `main.tex`)

Verdict: Karp VERIFIED first-hand but for "at most three"; Cook re-read; Garey-Johnson NOT VERIFIED.

- **Cook 1971** (scan on https://www.cs.toronto.edu/~sacook/homepage/1971.pdf, re-read p. 153): Theorem 2: "The following
  sets are P-reducible to each other in pairs (and hence each has the same polynomial degree of difficulty):
  {tautologies}, {DNF tautologies}, D_3, {subgraph pairs}." D_3 is the set of DNF tautologies with at most three
  conjuncts per disjunct (the proof reduces a DNF formula until "at most three conjuncts per disjunct"). P-reducible is
  the query-machine (Turing) reducibility of the paper, not many-one; "NP-complete" does not occur. So Cook alone does
  not state "3-SAT is NP-complete", and his clauses have at most three literals.
- **Karp 1972**, read in the reprint (Springer, *50 Years of Integer Programming 1958-2008*, 2010, ch. 8, authors' copy
  https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf; the page images carry the original pagination 85-103):
  reducibility (many-one, polynomial time) p. 86; Definition 5 "(polynomial) complete", p. 93; **Main Theorem**
  "All the problems on the following list are complete", p. 94; item 11 on p. 95: "SATISFIABILITY WITH AT MOST 3
  LITERALS PER CLAUSE. INPUT: Clauses D_1,...,D_r, each consisting of at most 3 literals ... PROPERTY: The set {D_1,...,D_r}
  is satisfiable"; Figure 1 (p. 96) reduces SATISFIABILITY to it; the reduction (splitting a clause with m > 3 literals
  with a new variable, repeated) on p. 98. So Karp proves NP-completeness (his "complete") for at most three, not
  exactly three. The Springer chapter (DOI 10.1007/978-1-4684-2001-2_9) was not needed.
- **Garey-Johnson 1979**: not verified; Google Books (id `fjxGAQAAIAAJ`) has no preview. A secondary page (a review
  blog) names p. 46 for the definition with "exactly 3 elements" per clause and pp. 48-49 for the conversion of larger
  clauses; this is secondary and must not be used. `Section 3.1.1 / Theorem 3.1` remains TODO(verify).
- CLRS (`Cormen2022`) 3-CNF-SAT: the Google Books preview of the 4th edition does not show pp. 1100-1101; not verified.
- Proposed line 308 (decision for the author; "exactly three" is part of the article's problem statement, so I changed
  nothing):
  - verified now, at-most-three form: `\ThreeSAT{} is NP-complete~\cite[pp.~94--95 and~98]{Karp1972Reducibility}.`
    This is accurate for "at most three" only; the article's definition says "exactly three". The step from at most
    three to exactly three is a one-line padding argument that the author may add, or Garey-Johnson may be cited for
    it once opened.
  - after Garey-Johnson is verified: `\cite{Karp1972Reducibility,GareyJohnson1979}` (entry proposed in (b)).
  - weakest, as now: `\cite{Cook1971Complexity}` (see Cook above).

---

## (a) Search log rows (column format of `knowledge/literature/searches.md`; to be pasted by the owner)

| Date | Question | Source | Queries exactly as entered | Found (keys) | Conclusion |
|---|---|---|---|---|---|
| 2026-10-10 | Year of the printed Frieze-Karonski book | web search; Cambridge Core; Open Library; Google Books preview | *Frieze Karoński "Introduction to Random Graphs" Cambridge University Press 2016 publication date copyright*; *"Frieze" "Karoński" "Introduction to Random Graphs" "First published" Cambridge University Press "Printed in" "Library of Congress"*; cambridge.org/core/product/identifier/9781316339831/type/book; openlibrary.org/isbn/9781107118508.json; books.google.com/books?id=OVC2CgAAQBAJ&pg=PR4 | `Frieze2016` | Imprint page of the hardback: (c) 2016, First published 2016. Release date in Cambridge metadata: 26 October 2015. Keep 2016. |
| 2026-10-10 | Frieze-Karonski printed numbering: coupling, Chernoff, diameter | Google Books preview of the e-book edition `Bh7QCgAAQBAJ`; authors' PDF 2026-08-07 | pages pg=PA5, PA7, PA17, PA110, PA111, PA114, PA386, PA391, PA392 | `Frieze2016` | Printed: (1.3) p. 5, (1.6) p. 7, Exercise 1.4.8 p. 17, Theorem 7.1 p. 110, Theorem 7.2 p. 114, (21.17)-(21.19) and Theorem 21.6 p. 392. PDF-2026 numbers differ. No theorem kappa = lambda = delta for G(n,p). A Google Books text search (`q=`) triggered Google's traffic check and was not repeated. |
| 2026-10-10 | Bollobas 2001: diameter of G(n,p), constant p; sparse range; edge connectivity | Google Books preview `o9WecWgilzYC`; cambridge.org contents | *books.google Bollobás "Random Graphs" Cambridge Studies in Advanced Mathematics 73 second edition 2001 Chapter 10 The Diameter*; *Bollobás Random Graphs "Corollary 10.11" diameter "a.e." G_p fixed p diameter 2*; pages pg=PA161, PA166, PA168, PA169, PA251, PA254, PA257-PA259, PA262, PA264, PA267, PA269, PA276, PA459 | `Bollobas2001` | Theorem 10.10 (p. 259) + monotonicity (p. 262) imply diameter 2 for constant p; no explicit constant-p theorem in the visible pages. Theorem 7.6 (p. 168) covers p <= (log n + k log log n)/n only; p. 169 remark: holds for every p by Bollobas-Thomason 1985. No bound for p = alpha log n / n in Chapter 10. |
| 2026-10-10 | Journal numbering of Chung-Lu Theorem 4 | authors' PDFs; Crossref; ScienceDirect; web search | *"The Diameter of Sparse Random Graphs" Chung Lu Advances in Applied Mathematics 26 257-279 core.ac.uk pdf*; fanchung.ucsd.edu/dia.pdf; math.cmu.edu/~af1p/Teaching/WWW2004/diameter.pdf; api.crossref.org/works/10.1006/aama.2001.0720; sciencedirect.com/science/article/pii/S0196885801907201 | `ChungLu2001` | Theorem 4 (p. 15 of 22) in both authors' PDFs. ScienceDirect: HTTP 403 and a robot check (not bypassed). Journal numbering unverified. Repeat from a browser of the owner. |
| 2026-10-10 | Source for kappa = lambda = delta for all p | web search; Crossref; Memphis repository | *Bollobás Thomason "Random graphs of small order" Random Graphs '83 Annals of Discrete Mathematics 28 1985 pdf connectivity minimum degree*; api.crossref.org/works/10.1016/S0304-0208(08)73612-0; digitalcommons.memphis.edu/facpubs/5564 | `Bollobas2001` (p. 169); `BollobasThomason1985` (proposed) | Chapter not reachable (ScienceDirect only). Record verified in Crossref. Series volume 118 from the Memphis record. |
| 2026-10-10 | NP-completeness of 3-SAT: Karp, Cook, Garey-Johnson | web search; Karp reprint (cs.umd.edu); Cook scan (cs.toronto.edu); Google Books | *Karp "Reducibility Among Combinatorial Problems" 1972 pdf "SATISFIABILITY WITH AT MOST 3 LITERALS PER CLAUSE" 3-SAT*; *Karp 1972 "Reducibility Among Combinatorial Problems" full text pdf "Theorem 1" "SATISFIABILITY" "CLIQUE" "satisfiability with at most 3 literals per clause" "chromatic number" Section 3 list of problems* (extended); *"Garey and Johnson" "Computers and Intractability" 3-SATISFIABILITY 3SAT "NP-complete" "Theorem 3.1" Section 3.1.1 exactly three literals each clause*; cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf; cs.toronto.edu/~sacook/homepage/1971.pdf; books.google (ISBN 0716710447; id fjxGAQAAIAAJ pg=PA48; id drZNEAAAQBAJ pg=PA1100) | `Karp1972Reducibility`, `Cook1971Complexity`, `GareyJohnson1979` (proposed) | Karp: Main Theorem p. 94, item 11 p. 95 (at most 3 literals), reduction p. 98. Cook p. 153: P-reducible, at most three. Garey-Johnson and CLRS: no preview, not verified. |

## (b) Proposed changes to the canonical `knowledge/bibliography/references.bib` (not applied)

ASCII only; status lines in the format of `knowledge/bibliography/README.md` section 3.

1. `Frieze2016`: replace the two "Note" lines by the following (the status line and the ISBN line stay). The `url` field
   (authors' PDF) now has other numbering than the printed book; either keep it with this note or drop it.

```bibtex
% Year 2026-10-10: the imprint page of the printed hardback (Google Books preview, id OVC2CgAAQBAJ, p. iv) reads "(c) Alan Frieze and
% Michal Karonski 2016" and "First published 2016"; Cambridge Core and Crossref date the release 26 October 2015. The entry keeps 2016.
% Numbering 2026-10-10: the PDF at the url field is a revised version dated 2026-08-07 (854 pages, 38 chapters) with numbers that differ from
% the printed book (22 chapters). Locations in the PRINTED edition (Google Books preview, id Bh7QCgAAQBAJ, running heads read): coupling (1.3), p. 5,
% and monotone increasing properties (1.6), p. 7, both Sec. 1.1; Exercise 1.4.8 (G(n,p), p constant, diameter two), p. 17; Theorem 7.1 (diameter d),
% p. 110; Theorem 7.2 (p = omega log n / n, omega to infinity), p. 114; Chernoff bounds (21.17)-(21.19) and Theorem 21.6, Sec. 21.4, pp. 391-392.
% The same results in the 2026 PDF: (1.3) p. 5, (1.7) p. 7, Exercise 1.4.8 p. 18, Theorem 7.1 p. 121, Theorem 7.2 p. 125, (34.17)-(34.19) p. 707,
% Theorem 34.6 p. 708. The book has no theorem kappa = lambda = delta for G(n,p) (2026 PDF searched; Theorem 4.3 is k-connectivity for fixed k).
```

2. `Bollobas2001`: add to the comment block (status line unchanged):

```bibtex
% Locations read 2026-10-10 (Google Books preview, id o9WecWgilzYC): Sec. 7.2, p. 166 (hitting times; Bollobas-Thomason 1985 for every k(n)),
% Theorem 7.4 p. 166 (k fixed), Theorem 7.6 p. 168 (p <= (log n + k log log n)/n: kappa = lambda = delta), remark on p. 169 (Theorem 7.6 holds
% without any restriction on p, credited to Bollobas and Thomason 1985); Theorem 10.10 p. 259 (diameter d or d+1 for p^d n^(d-1) = log(n^2/c),
% pn/(log n)^3 to infinity), monotonicity of "diam <= k" p. 262. Constant p, diameter two: no numbered statement found (pp. 255-256, 263 not visible).
```

3. `ChungLu2001`: replace the line "The journal numbering was not compared ..." by:

```bibtex
% Compared 2026-10-10: Theorem 4 is identical in two authors' PDFs, fanchung.ucsd.edu/dia.pdf (2004, 22 pp., 17 references as in the Crossref record
% of the journal version; Theorem 4 on p. 15) and math.cmu.edu/~af1p/Teaching/WWW2004/diameter.pdf (draft of 2000-08-29). The journal pagination was not
% seen (ScienceDirect: HTTP 403 and a robot check). Cite "Theorem 4" only after the journal PDF confirms the number.
```

4. `Karp1972Reducibility`: replace the "Content not read ..." lines by:

```bibtex
% Content read 2026-10-10 in the reprint of the 1972 text (Springer, 50 Years of Integer Programming 1958-2008, 2010, ch. 8; authors' copy
% www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf, page images with the original pages 85-103). Reducibility = polynomial-time many-one, p. 86; Definition 5
% (polynomial) complete, p. 93; Main Theorem, p. 94: all 21 listed problems are complete; item 11, p. 95: SATISFIABILITY WITH AT MOST 3 LITERALS PER
% CLAUSE (at most three, not exactly three); reduction from SATISFIABILITY by splitting long clauses with a new variable, p. 98; Figure 1, p. 96.
```

5. New entry `BollobasThomason1985` (cite only after the chapter is read):

```bibtex
% PARTIAL 2026-10-10: authors, title, volume title, pages, year, publisher and DOI from the Crossref record of the chapter and the University of
% Memphis repository record (https://digitalcommons.memphis.edu/facpubs/5564); series volume 118 from the Memphis record; ISBN 9780444878212 in Crossref
% (check digit recomputed, valid). Editors are not in Crossref and were not verified, so they are left out. Content not read (ScienceDirect not
% reachable). Bollobas2001, p. 169, credits this paper (1985) with kappa = lambda = delta w.h.p. for every p. Confirm the theorem in the chapter.
@incollection{BollobasThomason1985,
  author    = {Bollob{\'a}s, B{\'e}la and Thomason, Andrew},
  title     = {Random Graphs of Small Order},
  booktitle = {Random Graphs '83},
  series    = {North-Holland Mathematics Studies},
  number    = {118},
  pages     = {47--97},
  publisher = {Elsevier},
  year      = {1985},
  doi       = {10.1016/S0304-0208(08)73612-0}
}
```

6. New entry `GareyJohnson1979` (only if the author wants the "exactly three" citation; not citable yet):

```bibtex
% TODO: not verified against a primary record. Authors, title, publisher and year from the Google Books record (id fjxGAQAAIAAJ: W. H. Freeman, 1979,
% 338 pages; no preview). The location of 3SAT (Section 3.1.1) and the theorem number are not verified. Check the Library of Congress record and a copy.
@book{GareyJohnson1979,
  author    = {Garey, Michael R. and Johnson, David S.},
  title     = {Computers and Intractability: A Guide to the Theory of {NP}-Completeness},
  publisher = {W. H. Freeman},
  year      = {1979}
}
```

## (c) What remains TODO(verify)

1. Q1: the place in Bollobas 2001 that states "constant p, diameter two" (pp. 255-256, 263, Chapter 10 exercises
   pp. 276-281, or Chapter 2 examples); alternatively adopt the derivation from Theorem 10.10 given in Q1.
2. Q2: the number and page of Chung-Lu's Theorem 4 in the journal version (Adv. Appl. Math. 26, pp. 257-279;
   Elsevier open archive, https://www.sciencedirect.com/science/article/pii/S0196885801907201, needs a human browser:
   a robot check blocked this session). Also update `knowledge/literature/ChungLu2001.md`, "Doubts".
3. Q3: read the chapter of Bollobas and Thomason (DOI 10.1016/S0304-0208(08)73612-0) and confirm that it contains
   kappa = lambda = delta for every p; its editors; whether "Bollobas and Thomason (1985)" in the reference list of
   Bollobas 2001 is this chapter (book pp. 460-468 were not in the preview).
4. Q4: Janson-Luczak-Rucinski Theorem 2.1 not opened (optional; not needed).
5. Q5: printed p. 6 of Frieze-Karonski (the definition of "monotone increasing") not opened.
6. Q7: Garey-Johnson Section 3.1.1 / Theorem number and the "exactly three literals" form; CLRS 4th edition
   Section 34.4 as an alternative; the padding step from at most three to exactly three.
7. `Frieze2016`: the `url` field points to a version with other numbering than the printed book; decide whether to keep it.
8. Article text: Theorem 6.3 currently cites `Frieze2016` (wrong, see Q3); Theorem 6.2 cites `Bollobas2001` for a
   bound that the book does not state in the pages seen (Q2); Theorem 6.1 cites `Bollobas2001` without a location (Q1).
