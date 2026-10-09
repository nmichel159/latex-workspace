# Academic style

Target style of every article and of the dissertation: modern, concise technical English without padding.
This file covers **sentences and paragraphs**. Document structure: [paper-structure.md](paper-structure.md); definitions,
theorems and proofs: [math-writing.md](math-writing.md); experiments: [experiments-reporting.md](experiments-reporting.md);
LaTeX mechanics: [latex-guide.md](latex-guide.md); final check: [checklist.md](checklist.md).

## 1. Principle

**Every sentence carries information the reader needs to understand or verify a result.**
Test: delete the sentence. If the reader lost nothing, it stays deleted.

Priority in a conflict: correctness > unambiguity > brevity > polish.
Brevity never removes a hypothesis, a proof step, a definition or a detail needed to repeat an experiment.

### 1.1 Add the minimum (owner's rule, 2026-10-09)

The owner rejects long text. When something is added to a document, add the fewest words that do the job.

- **No elaboration.** Do not explain what a figure, a formula or the previous sentence already shows. Do not add a
  remark, a reading guide or a consequence that nobody asked for.
- **Figure caption: one line.** A title, at most one short clause; never several sentences, never a paragraph.
  ✗ a caption that explains every color, restates the definition and adds an equivalence.
  ✓ *The two 2-synchronization threads of a variable $x_i$*.
- **Introducing a figure: one sentence**, or a bracketed reference in a sentence that is already there.
- **A sentence where a paragraph was planned; nothing where a sentence adds nothing.** When unsure whether to add
  text, do not add it.
- The same holds for notes, reports and replies to the owner: the result first, in a few lines.

## 2. Language

| Item | Rule |
|---|---|
| Language of documents | English unless the author decides otherwise; conversation with the author in Slovak |
| Spelling | American (*formalize*, *neighbor*, *behavior*, *modeling*, *labeled*) |
| Person | authorial *we*, also for a single author; not *the author*, not *one* |
| Voice | active (*we prove*, *the algorithm returns*); passive only when the agent does not matter (*the graph is drawn in Figure 2*) |
| Tense: what the paper does, what holds | present (*we prove*, *Lemma 3 implies*, *Table 2 shows*) |
| Tense: what we did in an experiment | past (*we ran each configuration 30 times*) |
| Tense: other people's work | past for the event (*Cook proved*), present for the valid result (*3-SAT is NP-complete*) |
| Future tense | not used for the text itself (*we will show* → *we show*) |
| Contractions | none (*don't* → *do not*) |
| New term | `\emph{...}` at its first occurrence only; no quotation marks around terms |
| Problem names | small caps through a macro, identical everywhere ([latex-conventions.md](latex-conventions.md) §6) |
| Abbreviations | introduced once, at first use; in the title and abstract only widely known ones (NP, SAT, LLM) |
| *i.e.*, *e.g.* | followed by a comma; never at the start of a sentence; *cf.* means "compare", not "see" (en.wiktionary.org/wiki/cf., checked 2026-10-08) |

## 3. Ten rules of concision

The "before" examples come from article 1 (state on 2026-10-07).

**3.1 Result first.** The abstract, the introduction, each section and each paragraph open with what they claim; the
justification follows.

**3.2 No scene-setting.** A text opens with the problem, not with the state of the world.

> ✗ *In modern distributed systems, data exchange between servers must often balance two opposing objectives: enabling communication within a trusted domain and preventing communication by potential adversaries.*
> ✓ *A cut-path between vertices $u$ and $v$ is an edge set that contains both a $u$–$v$ path and a $u$–$v$ cut.*

**3.3 Specific, not general.** Name the class, the bound, the number, the name, not a description of them.

> ✗ *we identify two graph classes in which the problem becomes tractable*
> ✓ *we prove $\cp(u,v) = c(u,v) + d(u,v) - 1$ for graphs of diameter two and for graphs in which a minimum cut between any two vertices has at most two edges*

**3.4 One idea, once.** A definition lives in one place; other places refer to it. The contributions appear once, in
the introduction; the abstract gives them shorter, the conclusion does not repeat them in the same sentences. A sentence
that rephrases the previous one goes.

> ✗ *This hybrid structure, which captures both connection and disconnection properties at the same time, will be formally introduced as a cut-path.* (the previous sentence already said it)

**3.5 Verb, not noun.** *perform an analysis of* → *analyze*; *give a proof of* → *prove*; *is in agreement with* →
*agrees with*.

> ✗ *The interplay between these two objectives---connectivity and control---serves as the conceptual foundation of the present work.*
> ✓ (delete; the sentence claims nothing)

**3.6 No self-praise.** Do not write *novel*, *elegant*, *powerful*, *comprehensive*, *extensive*, *state-of-the-art*,
*significant* (without a test). Say what is new in plain terms: the statement, the bound, the method, the comparison
with a cited result.

> ✗ *Graph theory provides an elegant formal framework for representing such systems.*
> ✓ *Vertices are servers and edges are communication links.*

**3.7 No text about the text.** Delete *In this section we discuss...*, *We are now ready to state...*, *As mentioned
above...*, *It is worth noting that...*. Allowed: one paragraph on the paper's structure at the end of the introduction
(conditions: [paper-structure.md](paper-structure.md) §5), one sentence of strategy before a long proof
([math-writing.md](math-writing.md) §5), a forward reference with a number (*see Section 5*).

> ✗ *Section 2 introduces the formal definitions, notation, and fundamental concepts used throughout the paper, including the definition of cut-paths and their basic properties.*
> ✓ *Section 2 defines cut-paths and proves $\max\{c,d\} \le \cp \le c+d-1$.*

**3.8 Hedge only where the uncertainty is, and once.** State proved results without softening. Mark unproved ones
with the exact verb (table in §6). *may possibly suggest* → *suggests*.

**3.9 One concept, one word.** Synonyms for variety are an error in technical text: a different word makes the reader
look for a different object (*shortest path* / *min path* / *geodesic*; *vertex* / *node*; *instance* / *input*).
The chosen term is in the project glossary (`knowledge/research/<topic>.md`).

**3.10 Numbers, not adjectives.** *much faster* → *4.2 times faster*; *on many instances* → *on 37 of 50 instances*;
*large graphs* → *graphs with $10^6$ edges*.

## 4. Sentence

- **Subject and verb together**, near the start. A long insertion between them becomes its own sentence.
- **Known first, new last.** The end of a sentence carries the emphasis; the next sentence starts with what the previous
  one ended with. This holds a text together without connectives.
- **One idea per sentence.** About 15–25 words; split above 40, the `[long]` limit of `check-text.ps1` (`-MaxWords`).
  A short sentence after a long one is fine; three long ones in a row are not.
- **Positive form:** *does not contain any* → *contains no*; *is not connected* → *is disconnected*, when exact.
- **Parallel form** for parallel content: list items and proof cases share the grammatical shape.
- **`that` restricts, `which` adds** (with a comma): *the cut that separates $u$ from $v$* vs. *the cut $C$, which has
  two edges*.
- **A pronoun has one referent.** *This* at the start of a sentence takes a noun: *This bound...*, not *This shows...*
  when the referent is unclear.
- **One source, one claim; a citation is not a noun:** the citation stands next to the claim it supports, and the
  sentence reads correctly with the bracket removed (*Gomory and Hu [3] showed*, not *[3] shows* or *In [3], the
  authors show*). Rules and commands: [../bibliography/README.md](../bibliography/README.md) §8.
- **Triads and paired synonyms** (*definitions, notation, and fundamental concepts*; *isolate or restrict*) shrink to the
  one word that is true.

## 5. Paragraph

- The first sentence says what the paragraph is about and what it claims; a reader of first sentences alone follows the
  line of the paper.
- One paragraph, one point. Split a paragraph with two points; delete one with none.
- The last sentence does not summarize the paragraph. If the point needs repeating, the paragraph is badly built.
- Use a connective (*however*, *therefore*, *moreover*, *in contrast*) only where that logical relation holds.
  *Moreover* and *Furthermore* opening every other sentence are padding.
- Bullet lists only for items that are truly parallel (contributions, cases, steps). An argument is written in sentences.
- A one-sentence paragraph is an exception (a transition between major parts, a highlighted claim), not a style.

## 6. Strength of a claim

The verb tells the reader what backs the claim. A stronger verb without proof is an error; a weaker verb for a proved
theorem is false modesty.

| Verb | Backing |
|---|---|
| *prove*, *show* | the proof is in the text (or cited) |
| *observe*, *note* | immediate consequence of a definition or of the previous step |
| *obtain*, *derive* | computation or derivation |
| *measure*, *find*, *report* | experimental result with its conditions stated |
| *suggest*, *indicate* | the data support the conclusion but do not prove it |
| *conjecture* | we believe it, without proof; state what the belief rests on |
| *demonstrate* | only for an experiment or an example, not for a proof |
| *claim* | in mathematics the name of an environment; about other people's work it sounds like doubt: do not use |

A novelty claim (*first*, *has not been studied*) appears at most once, and only after a real literature search logged
in [../literature/searches.md](../literature/searches.md); more precise: say what exactly is new compared with which work.

## 7. Text that reads as LLM-written

House rule (no external source; derived from the author's drafts, §9). Do not write:

- openings about the state of the world (*In recent years...*, *With the rapid development of...*, *In modern
  distributed systems...*);
- the vocabulary *delve*, *leverage*, *harness*, *underscore*, *showcase*, *pivotal*, *crucial*, *intricate*,
  *landscape*, *realm*, *seamless*, *comprehensive*, *robust* (outside its technical meaning), *notably*,
  *shed light on*, *pave the way*;
- sentences that only evaluate (*This highlights the importance of...*, *This dual requirement leads naturally to...*);
- a summary at the end of every paragraph (*Overall, ...*, *In summary, ...*);
- *not only ... but also*, triads of adjectives, symmetric pairs (*both connectivity and disconnection*) used for rhythm;
- dashes as the main way to build a sentence: at most one dash parenthesis per paragraph;
- abstract subjects (*the interplay*, *the tension*, *this perspective*) with *serves as*, *embodies*, *captures*,
  *reflects*;
- a conclusion that promises *promising avenues for future research* instead of specific open problems;
- captions and lead-ins that explain: several sentences under a figure, or a paragraph that tells the reader how to
  read it (§1.1).

Machine check: `.\scripts\check-text.ps1 -Project <project>` finds these patterns from [phrase-list.tsv](phrase-list.tsv).
Disclosure of AI use: [submission.md](submission.md) §1.

## 8. Economical transitions (instead of announcements)

| Instead of | Write |
|---|---|
| *We are now ready to state the main theorem of this section.* | (nothing; the theorem follows) |
| *For better understanding, we provide an illustrative example (see Figure 3).* | *Figure 3 shows a chain with three links.* |
| *Intuitively speaking, one can think of...* | *Intuitively, ...* (one sentence before the formal definition) |
| *Let us now turn our attention to the case...* | *Case 2: ...* / *Suppose now that...* |
| *It is easy to see that $x \le y$.* | *By (3), $x \le y$.* |
| *As we have already mentioned in the introduction, ...* | (delete), or *Recall that...* if the definition is far back |
| *In order to prove the theorem, we will need the following lemma.* | (nothing; the lemma follows), or one sentence on what the lemma is for |
| *The following theorem is the main result of this paper.* | a name in brackets: `\begin{theorem}[Diameter two]` |

Allowed and useful: *Intuitively,* · *Formally,* · *Recall that* · *Assume for contradiction that* · *Without loss of
generality* (only when it truly loses nothing and the text says why) · *Conversely,* · *In particular,* · *Suppose first
that*.

## 9. The author's habits

Found by the audit of 2026-10-08. Check these first, when writing and when revising.
Sources: **draft** = `archives/removed-from-projects/clanok-1-min-cut-path/main-before-revision-2026-10-07.tex`
(article 1 as the author wrote it); **MT** = `knowledge/sources/diplomova-praca-2025-min-cut-path.txt` (master's thesis,
line numbers of the text extraction). The draft copies whole paragraphs from MT (draft:648 = MT:1075), so these are
habits, not slips.

| Pattern | Real example | Fix |
|---|---|---|
| Scene-setting opener | draft:96 "In distributed communication systems, a central challenge lies in maintaining a secure but controlled flow of information"; MT:181 "Many fundamental graph problems are related to connectivity or separation" | open with the definition (§3.2) |
| Announcing instead of stating | draft:224 "In this section, we show that the \textsc{Min Cut-Path} problem is NP-complete."; draft:720 "We are now ready to state the central theorem of this section:" | delete; the statement follows (§3.7) |
| Recap transition (4× in draft, 6× in MT) | draft:648 "Having established the general complexities of the Min Cut-Path problem, we now turn our attention to specific graph classes"; MT:691 | delete; the heading is the transition |
| "Formally:" after an informal paraphrase (10× in draft, 11× in MT) | draft:686 "Consequently, one of these sets must be empty. Formally:" + the lemma | one sentence of intuition, then the environment ([math-writing.md](math-writing.md) §3) |
| Sentence restating the previous one | draft:104 "This hybrid structure, which captures both connection and disconnection properties at the same time, will be formally introduced as a \emph{cut-path}." | delete (§3.4) |
| Praise words (*crucial* 14× in MT) | draft:101 "an elegant formal framework"; draft:848 "a powerful tool"; draft:965 "a novel combinatorial structure"; MT:693 "This chapter serves as a crucial stepping stone" | name the result (§3.6) |
| Glue adverbs | draft:98 "naturally motivates"; draft:111 "which inherently embodies both connectivity and disconnection"; draft:85 "simultaneously contains" (9× in draft) | delete unless the word carries a fact |
| Obviousness instead of a reason | draft:738 "It is straightforward to observe that"; draft:745 "From a simple observation, we can see that"; draft:944 "It is easy to see that"; draft:639 "clearly in NP" | cite the lemma or give the reason in one clause ([math-writing.md](math-writing.md) §5) |
| Stacked hedges in future work | draft:975 "another potential avenue ... could provide valuable insight ... could reveal ... could guide" | a numbered open question (§3.8) |
| Nominalization | draft:308 "a detailed presentation of the individual gadgets"; draft:968 "the identification of additional islands of polynomial-time solvability" | put the action in the verb (§3.5) |
| Lead-in that only says a result follows | draft:663 "The following observation follows directly from the definition of a cut."; draft:898 "The following lemma establishes bounds on the value of \( c(u,v) \):" | delete, or say what is used |
| Triads and paired synonyms | draft:248 "a well-established and widely recognized result"; draft:659 "a straightforward and efficient algorithm" | keep one word (§4) |
| Abstract subject + *serves as / reflects* | draft:99 "The interplay between these two objectives ... serves as the conceptual foundation for the present work."; draft:115 "This dual optimization objective reflects the balance" | the subject is an object of the paper, or delete |
| Signposting a figure | draft:756 "For a better understanding, we provide an illustrative example"; MT:408, 437, 830 | "Figure 4 shows ..." (§8) |
| Contributions repeated four times | draft:120, 125, 251, 965 all describe the "two-step reduction from 3-SAT through ... Separating Shortest Path" | contributions once, with locations ([paper-structure.md](paper-structure.md) §5) |
| Imagery and vague future work | draft:968 "numerous promising directions for future research", "islands of polynomial-time solvability" | name the class, ask the question ([paper-structure.md](paper-structure.md) §10) |

Numbers for the current article 1 (2026-10-08): the abstract (141 words) states no result; 11 of 31 introduction
sentences carry a checkable statement (definition, result, cited fact); the roadmap repeats the contributions in
6 sentences; 147 of the 518 conclusion words restate the contributions.

## 10. English of a Slovak author

Errors that occur in the author's texts (sources as in §9).

| Error | Real example | Correct |
|---|---|---|
| Missing article | draft:137 "the length of shortest \(u\)–\(v\) path" | "the length of a shortest $u$--$v$ path" |
| *a/an* before a vowel sound; adjective used as a noun | draft:958 "achieves a Average $(1+\epsilon)$-Approximation Scheme"; draft:211 "is an average-case in the sense that" | "is an average $(1+\varepsilon)$-approximation scheme"; "is average-case in the sense that" |
| Article before a numbered reference | MT:1808 "due to the Claim 19"; MT:2185 "According to the Claim 21" | "by Claim 19" |
| Lower-case reference name | draft:756 "By lemma~\ref{...}"; draft:720 "the lemmas~\ref{...} and~\ref{...}" | "By Lemma~\ref{...}"; "Lemmas~\ref{...} and~\ref{...}" |
| Uncountable plural, number agreement | draft:862 "in the literatures", "pairs of vertex" | "in the literature", "pairs of vertices" |
| *Thanks to* (SK *vďaka*) | draft:550 "Thanks to the synchronization threads"; draft:720 | "By Lemma X", "because of" |
| *It holds that* (SK *platí, že*) | draft:891 "for any fixed \( \epsilon > 0 \), it holds that" | "for every fixed $\varepsilon > 0$," + formula |
| *For (a) better understanding* (SK *pre lepšie pochopenie*) | draft:756; MT:408 | "Figure X shows ..." |
| Future tense for the text (SK *budeme*) | draft:170 "In this paper, we will refer to"; MT:352 "In this thesis, we will refer to" | "We call ..." |
| Comma before a subordinate clause (Slovak comma rule) | draft:146 "such that, there exist subsets" | "such that there exist subsets" |
| Comma splice | draft:910 "First, we fix the values of \(k\) and \(\epsilon\) as in the proofs of Theorems~..., we know that" | two sentences |
| Preposition calque (SK *prechádzať cez*) | draft:397 "paths that traverse through the chain links" | "paths that traverse the chain links" |
| Capitals inside a sentence | draft:143 "More Formally:"; draft:932 "is an Average \( (1+\epsilon) \)-Approximation Scheme" | lower case except names and numbered references |
| Section title calque (SK *Základné pojmy*) | draft:132 "\section{Fundamentals}" | "Preliminaries" |
| Typos, doubled words | draft:343 "egde-disjoint"; draft:418 "the  this elementary operations"; draft:572 "It remains to prove show" | spell-check before every hand-over |

Not found in the author's texts, still checked by the `grammar` entries of [phrase-list.tsv](phrase-list.tsv):
*allows to* + verb, *informations*, *depend from*, *consist from*, *different than*, *on the other side*,
*eventually* / *actual* as false friends, *resp.*, *cca*.

## 11. Revision procedure

**Owner's rule (2026-10-09): revising the owner's manuscript means tidying, not compressing.** Every Definition,
Lemma, Theorem, Remark, algorithm, auxiliary procedure, proof step and figure stays; a formal definition is never
turned into a sentence of prose; an argument is never replaced by a shorter one. Allowed: English, clarity, order
inside a section, consistent notation, implicit steps made explicit, a proof environment for an argument already in
the text. Deletions, restructurings and mathematical corrections are listed in a report with a precise proposal and
applied only after the owner approves. (The owner rejected a compressed revision of article 1 that removed
Algorithm 1, its procedures and several definitions.) The cutting order below applies to the author's own new
drafts and to text the owner asks to shorten.

Cut from the top down; polishing sentences in a paragraph that will be deleted is wasted work.

1. **Claim.** Can the main result be said in one sentence? If not, the problem is not style.
2. **Sections.** Does every section serve the main claim? What does not goes to an appendix or out.
3. **Paragraphs.** Read only the first sentences: do they form a continuous line? Delete a paragraph without a point.
4. **Sentences.** Apply the test of §1 to each sentence, then rules §3.2–§3.10.
5. **Words.** `.\scripts\check-text.ps1 -Project <project>`; judge every hit, never fix mechanically.
6. **Checklist.** [checklist.md](checklist.md).
7. **Counts.** Compare word counts of the abstract, the introduction and the whole before and after; report them to the
   author.

Revision does not change mathematical content. If cutting reveals that a statement is unclear or wrong, it goes into the
report to the author, not into a silent fix.

## 12. Sources

Rules draw on these guides (entries in [../bibliography/references.bib](../bibliography/references.bib), section
"Writing and publishing"). §7 and §9–§10 are house rules from the author's own texts.

| Key | Work (authors, short title, year) | Covers |
|---|---|---|
| `Knuth1989MathWriting` | Knuth, Larrabee, Roberts, *Mathematical Writing*, 1989 | mathematical exposition |
| `Higham2020Handbook` | Higham, *Handbook of Writing for the Mathematical Sciences*, 3rd ed., 2020 | writing and publishing in the mathematical sciences |
| `WilliamsBizup2022Style` | Williams, Bizup, *Style: Lessons in Clarity and Grace*, 13th ed., 2022 | sentence-level clarity and style |
| `Zobel2014Writing` | Zobel, *Writing for Computer Science*, 3rd ed., 2014 | technical writing in computer science (papers, theses, reports) |
| `Heard2026Guide` | Heard, *The Scientist's Guide to Writing*, 3rd ed., 2026 | scientific writing: structure and style |
| `Sword2012Stylish` | Sword, *Stylish Academic Writing*, 2012 | style of academic prose |
| `Pinker2015Sense` | Pinker, *The Sense of Style*, 2015 | clear prose, sentence-level style |
| `Schimel2011Writing` | Schimel, *Writing Science*, 2011 | story structure of scientific papers and proposals |
| `Halmos1970HowToWrite` | Halmos, *How to Write Mathematics*, 1970 | mathematical exposition |
| `GopenSwan1990Science` | Gopen, Swan, *The Science of Scientific Writing*, 1990 | reader expectations, structure of sentences and paragraphs |
| `LiptonSteinhardt2019Troubling` | Lipton, Steinhardt, *Troubling Trends in Machine Learning Scholarship*, 2019 | writing and reporting problems in ML papers (explanation vs. speculation, terminology, mathiness) |
| `MenshKording2017TenRules` | Mensh, Kording, *Ten Simple Rules for Structuring Papers*, 2017 | paper structure (context, content, conclusion) |
| `Widom2006Tips` | Widom, *Tips for Writing Technical Papers*, 2006 | technical papers: structure and style tips |
| `PeytonJones2016GreatPaper` | Peyton Jones, *How to Write a Great Research Paper*, 2016 | research-paper writing (talk slides) |
| `Lipton2018Heuristics` | Lipton, *Heuristics for Scientific Writing (a Machine Learning Perspective)*, 2018 | scientific writing heuristics for ML papers |
| `Poonen2026Suggestions` | Poonen, *Practical Suggestions for Mathematical Writing*, 2026 | mathematical writing |
| `TaoOnWriting` | Tao, *On Writing*, undated | advice on writing papers |
| `Goldreich2004HowToWrite` | Goldreich, *How to Write a Paper*, 2004 | structure of a research paper |
| `Bertsekas2002TenRules` | Bertsekas, *Ten Simple Rules for Mathematical Writing*, 2002 | mathematical writing |
| `LeeGuideMath` | Lee, *A Guide to Writing Mathematics*, undated | mathematical writing |
| `Nanda2025MLPapers` | Nanda, *Highly Opinionated Advice on How to Write ML Papers*, 2025 | ML paper structure and writing |
| `Farquhar2024MLPapers` | Farquhar, *How to Write ML Papers*, 2024 | ML paper structure and writing |
