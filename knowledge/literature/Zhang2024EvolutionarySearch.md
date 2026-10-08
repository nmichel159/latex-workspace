# Zhang2024EvolutionarySearch

| | |
|---|---|
| Paper | Zhang, Liu, Lin, Wang, Lu, Zhang: *Understanding the Importance of Evolutionary Search in Automated Heuristic Design with Large Language Models*. PPSN XVIII, LNCS 15149, Springer, 2024, 185-202. DOI 10.1007/978-3-031-70068-2_12; arXiv 2407.10873 |
| Key | `Zhang2024EvolutionarySearch` |
| Reading status | sections 1-5 and Appendices A-B read 2026-10-08 in arXiv v1 HTML; remaining appendices not read |
| Full text | - (arXiv) |
| Topic | [../research/llm-optimization.md](../research/llm-optimization.md), sections 2 and 6 |

## What the paper does

- Names the common paradigm "LLM-based evolutionary program search" (EPS): heuristics as executable code, an evolutionary loop, an LLM as the variation engine (section 1, Fig. 1).
- Identifies three problems in prior evaluation: inconsistent settings (initialization, termination, LLM), inadequate baselines (random search or simple hand-made heuristics), no component analysis (section 1).
- Proposes the baseline (1+1)-EPS: keep one best heuristic, prompt the LLM one-shot with it, accept the child if better (Algorithm 1). Intended as a lower bound for the paradigm.
- Benchmark: FunSearch, EoH, ReEvo and (1+1)-EPS on admissible set A(15,10), online bin packing (OR and Weibull) and TSP100 (as GLS), with nine LLMs and five independent runs (sections 3-4).
- Findings:
  - LLM sampling without search stays far from best-known results even with 100,000 queries; (1+1)-EPS with 500 queries beats it (section 4.1.1, Fig. 2).
  - Larger or code-specialized LLMs alone do not give better heuristics (section 4.1.2, Table 4).
  - No EPS method wins on all problems; (1+1)-EPS is competitive except on bin packing (Weibull); EoH is consistently best on TSP (section 4.2.1, Fig. 4).
  - Results depend strongly on the LLM choice (section 4.2.2, Fig. 5).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| Delta_d: mean relative gap to the best-known value, averaged over problems and LLMs | - | aggregate over different problems; read per-problem plots before citing a number |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| (1+1)-EPS as minimal baseline | Algorithm 1 | experiments-reporting.md, baselines | one-shot prompt, greedy acceptance |
| Cost table: days per run, USD per run | section 4.3, Tables 5-6 | experiments-reporting.md, budgets | 10,000 evaluations; 2024 API prices |

## Difference from our work

The study is an empirical benchmark of search frameworks around LLMs; it measures relative gaps on four problems and makes no
claim about the problems' structure, which is where a graph-theoretic analysis would add explanation.

## Experiments

- Budget: 10,000 heuristic evaluations per run; population 100 for EoH and ReEvo; FunSearch with 10 islands, 4 samples per prompt; 5 runs; time limit per heuristic 50 s (TSP) or 20 s (Table 3).
- LLMs: UniXcoder, StarCoder, CodeLlama 7B/34B, DeepSeek-Coder 6.7B/33B (local, V100 GPUs, float16, temperature 1.0), GPT-3.5, GPT-4, Claude 3 Opus (APIs) (Table 2, section 4.3). Exact API model versions are not stated in the text read.
- Cost: 2-10 days per run depending on task and model; approx. USD 10 (GPT-3.5), 100 (GPT-4), 200 (Claude 3 Opus) per run (Tables 5-6).
- Dispersion: mean and standard deviation over 5 runs in convergence plots (Fig. 4); box plots in Figs. 2-3. No hypothesis tests reported in the parts read.
- Code: https://github.com/zhichao-lu/llm-eps (stated in section 1; not opened).

## Doubts and open questions

- Five runs per configuration are few for the claimed differences between methods; the paper reports no tests.
- Delta_d averages over problems with different scales of difficulty.
