# Gideoni2026SimpleBaselines

| | |
|---|---|
| Paper | Gideoni, Risi, Gal: *Simple Baselines are Competitive with Code Evolution*. arXiv 2602.16805 (v1, 2026-02-18); no peer-reviewed version found 2026-10-08 |
| Key | `Gideoni2026SimpleBaselines` |
| Reading status | sections 1-7 and Impact Statement read 2026-10-08 in arXiv v1 HTML; appendices not read |
| Full text | - (arXiv) |
| Topic | [../research/llm-optimization.md](../research/llm-optimization.md), section 6 |

## What the paper does

- Proposes two baselines for LLM code evolution (section 3, Fig. 1):
  - IID random sampling (IID RS): sample many programs independently from one prompt, keep the best;
  - sequential conditioned sampling (SCS): each generation conditions on a random subset of programs that ran successfully in the previous one, with optional restarts. Neither uses fitness-based selection.
- Compares them under equal constraints with purpose-built systems in three domains, each with a different binding budget (sections 4-6):
  - mathematical bounds from the AlphaEvolve paper, equal API budget of USD 20 per problem, against ShinkaEvolve;
  - agentic scaffolds for AIME, equal number of scaffold evaluations, against ADAS and ShinkaEvolve;
  - MLE-bench Kaggle tasks, equal wall-clock time of 24 h, against AIDE.
- Findings:
  - SCS matches or exceeds ShinkaEvolve on 6 of 9 bound problems, IID RS on 4 of 9 (Table 1).
  - Reformulating one problem's search space (uncertainty inequality) improved the bound for all methods more than any pipeline did (section 4.1).
  - Scaffolds selected on about 100 validation questions overfit; a hand-made majority vote generalizes better (section 5, Fig. 3).
  - SCS beats AIDE on 6 of 10 competitions (Table 2).
- Recommendations (section 7): compare methods with the same LLMs, prompt knowledge, verifier and budget; name the binding constraint (API cost, evaluations, wall-clock); separate "new search method" claims from "new discovery" claims; always include simple baselines.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| "code evolution": any LLM pipeline that mutates or recombines programs | LLM-based evolutionary program search (`Zhang2024EvolutionarySearch`) | same family of methods |
| equality of results via `numpy.isclose` default tolerances | - | section 3.1 |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| IID RS and SCS as mandatory baselines | section 3 | experiments-reporting.md, baselines | same model and prompts as the method under test |
| Search-space formulation dominates pipeline choice | section 4.1 | llm-optimization.md, section 6 | one problem reformulated; shown for bound-finding tasks |
| Probability of improvement and 95% CIs instead of p-value tests | sections 5, 7; Impact Statement | experiments-reporting.md, statistics | recommendation follows `Agarwal2021Precipice` |

## Difference from our work

The paper evaluates search pipelines, not problems; its finding that problem formulation sets the performance ceiling supports
investing in the mathematical formulation of graph problems before running any LLM search.

## Experiments

- Models: Gemini 2.5 Pro for the baselines; ShinkaEvolve restricted to Gemini 2.5 Pro, Flash and Flash Lite (section 4); GPT-4.1-nano for scaffold evaluation (section 5).
- Runs: a single ShinkaEvolve run per bound problem because of cost (above USD 70 per problem for all methods); baselines oversampled and compared via equal-budget subsets and bootstrap (section 4, Appendix F not read).
- Wall-clock: baselines 1-3 h per problem versus about 10 h for ShinkaEvolve (section 4).
- Hardware for MLE-bench: one RTX 8000 GPU, 12 CPU cores (section 6).
- Code released (section 1; repository not opened).

## Doubts and open questions

- Single run of the reference system per problem; the comparison rests on bootstrap over baseline samples.
- Not peer reviewed as of 2026-10-08.
- Its advice against p-value tests conflicts with the EC tutorials that prescribe nonparametric tests (`Derrac2011Tutorial`, `Arcuri2011Guide`); see experiments-reporting.md for how the author reconciles both.
