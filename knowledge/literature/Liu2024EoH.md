# Liu2024EoH

| | |
|---|---|
| Paper | Liu, Tong, Yuan, Lin, Luo, Wang, Lu, Zhang: *Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model*. ICML 2024, PMLR 235, 32201-32223. arXiv 2401.02051 |
| Key | `Liu2024EoH` |
| Reading status | main text (sections 1-6) read 2026-10-08 in arXiv v3 HTML; appendices not read |
| Full text | - (open at PMLR and arXiv) |
| Topic | [../research/llm-optimization.md](../research/llm-optimization.md), section 2 |

## What the paper does

- Automatic heuristic design (AHD) with an LLM inside an evolutionary loop. Each individual is a heuristic stored as a natural-language "thought", a Python function, and a fitness value (section 3.3).
- Population of N heuristics; per generation, five prompt strategies are each called N times (section 3.2):
  E1 (as different as possible from p parents), E2 (common idea of p parents, new parts), M1 (modify one), M2 (change parameters), M3 (remove redundant parts). Selection probability proportional to 1/(rank + N); the N best survive.
- Fitness = performance of the heuristic on a set of evaluation instances, so each evaluation is costly.
- Results (section 4.2): online bin packing (score function as in FunSearch), TSP and flow-shop scheduling (both as the landscape-update rule of guided local search, GLS). Claims fewer LLM queries than FunSearch: about 2,000 queries for bin packing versus about 10^6 reported for FunSearch.

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| "heuristic" = the evolved function inside a fixed algorithm (score function, GLS update rule) | heuristic = a whole algorithm | compare like with like when citing their gains |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| Thought + code representation; five prompt operators | sections 3.3-3.4 | llm-optimization.md, section 2 | GPT-3.5-turbo, 20 generations |

## Difference from our work

EoH searches a space of short scoring functions evaluated empirically on fixed instance sets; it gives no performance guarantee
outside those instances, which is the gap a complexity-theoretic analysis of the target problem can address.

## Experiments

- Model: GPT-3.5-turbo (main runs); section 5.1 compares GPT-3.5, Gemini Pro, CodeLlama, Deepseek (3 runs each). Exact model versions, sampling temperature and access dates are not given in the main text.
- Budget: 20 generations; population 20 (bin packing) or 10 (TSP, FSSP); p = 5 parents; single CPU i7-9700.
- Bin packing: evolved on five Weibull 5k instances (capacity 100); tested on Weibull sets of 1k-10k items, capacity 100 and 500, 5 instances each (Table 1). Baselines: first fit, best fit, and the published FunSearch heuristic (not a re-run of FunSearch).
- TSP: evolved on 64 random TSP100 instances; tested on six TSPLib instances (Table 2) against nearest/farthest insertion, OR-Tools (60 s), and neural solvers AM, POMO, LEHD.
- FSSP: evolved on 64 random instances; tested on Taillard instances (Table 3) against GUPTA, CDS, NEH, NEHFF, PFSPNet.
- Runs: most tables report one evolved heuristic; ablations in section 5.1 report three runs without dispersion statistics or tests.
- Ablation (Table 5): code-only variant EoC is far worse than EoH, which the authors read as evidence for the thought representation. `Zhang2024EvolutionarySearch` revisits these comparisons over more runs.

## Doubts and open questions

- Equal-budget comparison with FunSearch is not run; the FunSearch number is taken from its paper.
- Three runs give no basis for significance claims; the TSP and FSSP tables report single heuristics.
