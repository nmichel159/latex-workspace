# RomeraParedes2024FunSearch

| | |
|---|---|
| Paper | Romera-Paredes, Barekatain, Novikov, Balog, Kumar, Dupont, Ruiz, Ellenberg, Wang, O. Fawzi, Kohli, A. Fawzi: *Mathematical discoveries from program search with large language models*. Nature 625 (2024), 468-475. DOI 10.1038/s41586-023-06924-6 (online 2023-12-14, open access CC BY 4.0) |
| Key | `RomeraParedes2024FunSearch` |
| Reading status | main text, Methods and Related work read 2026-10-08 (Europe PMC copy PMC10794145); Supplementary Information not read |
| Full text | - (open access at the DOI) |
| Topic | [../research/llm-optimization.md](../research/llm-optimization.md), section 2 |

## What the paper does

- Setting: problems with a cheap `evaluate` function that scores a candidate solution. Goal: a `solve` program whose outputs score high, ideally beyond the best known (section "Main").
- Method FunSearch ("searching in the function space"): a frozen pretrained code LLM proposes new versions of one function inside a user-written skeleton; an evaluator runs them on given inputs, discards incorrect or time-out programs, and stores scored programs in a database that seeds the next prompts (Fig. 1).
- Ingredients the authors call essential: best-shot prompting (prompt holds k = 2 sampled programs sorted by score, named `priority_v0`, `priority_v1`, then an empty `priority_v2` header); a skeleton so that only the critical logic (e.g. the greedy priority function) evolves; an island model with periodic reset of the worse half of islands (every 4 h in their runs); clustering by score signature and Boltzmann selection of clusters; preference for shorter programs within a cluster (Methods).
- Results:
  - Cap set: a 512-cap in dimension n = 8, larger than previously known (Fig. 4).
  - Cap set capacity lower bound raised from 2.2180 to 2.2202 via admissible sets; inspection of the found program revealed a symmetry that was then imposed to search a smaller space (Fig. 5).
  - Online bin packing: evolved heuristics beat first fit and best fit on OR-Library OR1-OR4 and on Weibull instances, measured as excess bins over the L2 lower bound (Table 1).
- Discussion: the LLM is viewed as a source of diverse, syntactically correct programs; searching over programs biases towards concise (low Kolmogorov complexity) and interpretable solutions. Works best with (1) an efficient evaluator, (2) a graded score rather than a binary signal, (3) a skeleton with an isolated part to evolve.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| "heuristic" = function returning a priority score per bin | heuristic = algorithm without a guarantee | their usage is a scoring rule inside a fixed greedy skeleton |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| Problem-class conditions (evaluator, graded score, skeleton) | Discussion | candidate framing for graph problems, see llm-optimization.md section 11 | stated by the authors as empirical observation, not as a theorem |

## Difference from our work

FunSearch evolves programs that construct solutions under a fixed evaluator; it gives no guarantee on the quality of the evolved
heuristic beyond the evaluated instances, whereas our results on Min Cut-Path are proved for whole graph classes.

## Experiments

- LLM: Codey (PaLM 2 family, code fine-tuned), accessed through an API, no fine-tuning; on the order of 10^6 samples per reported result. StarCoder comparison only in Supplementary Information (not read).
- Infrastructure: typically 15 samplers and 150 CPU evaluators.
- Training/test split for bin packing: evolved on generated instances of OR1 size, tested on OR1-OR4 (size generalization).
- Robustness (Methods): runs differ; every run improves the baseline for admissible sets and bin packing, but only 4 of 140 runs found the 512-cap in n = 8. Statistical analysis is in Supplementary Information A.3 (not read).
- Baselines for bin packing: first fit and best fit only; no comparison with offline or metaheuristic solvers in the main text. Later critical work examines this choice: `Sim2025BeyondHype`, `Herrmann2026BinPacking`.

## Doubts and open questions

- Cost in money or GPU hours is not stated in the main text; only the sample count. TODO(verify) in Supplementary Information.
- Which results survive with fewer samples or a different LLM: main text only says results were "not too sensitive" to the LLM choice; evidence in Supplementary Information A (not read).
