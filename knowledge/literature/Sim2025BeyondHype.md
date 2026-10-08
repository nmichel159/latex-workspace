# Sim2025BeyondHype

| | |
|---|---|
| Paper | Sim, Renau, Hart: *Beyond the Hype: Benchmarking LLM-Evolved Heuristics for Bin Packing*. EvoApplications 2025, LNCS 15613, Springer, 2025, 386-402. DOI 10.1007/978-3-031-90065-5_24; arXiv 2501.11411 |
| Key | `Sim2025BeyondHype` |
| Reading status | full text (sections 1-7) read 2026-10-08 in arXiv v1 HTML |
| Full text | - (arXiv) |
| Topic | [../research/llm-optimization.md](../research/llm-optimization.md), section 6 |

## What the paper does

- Re-tests five published LLM-evolved online bin-packing heuristics (three from FunSearch: FS1, FS2, FSW; two from EoH: EoH, EoC) against five classical online heuristics (Next/First/Best/Worst/Almost-Worst Fit) (section 3.1).
- Test bed: 6,064 instances from 12 datasets, mostly from BPPLib, with item order shuffled for the online setting; datasets from the distributions used in training are excluded (section 3.2, Table 1).
- Metrics: average excess bins over the sum-of-sizes lower bound, Falkenauer fitness, share of instances won (section 4).
- Tunes the numeric constants of the evolved heuristics with irace (section 5) and evolves 100 instances won by each heuristic, then maps them with Instance Space Analysis (section 6).
- Findings:
  - Best Fit ranks first overall; FS1 second; FSW worst on every dataset; EoH never best on any dataset (section 4, Fig. 2).
  - Evolved heuristics beat classical ones on their training distribution but mostly do not generalize across distributions (section 7).
  - Re-tuning constants changes little, which the authors read as specialization rather than poor parameters (Table 2).
  - EoC outperforms EoH on this suite, reversing the ranking reported in `Liu2024EoH` (sections 4 and 7).

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| "generalist" vs "specialist" heuristic: spread of performance across datasets | - | judged from interquartile ranges (Fig. 3) |

## What we use from it

| Result | Location in source | Where we use it | Exact assumptions |
|---|---|---|---|
| Evaluation across many instance classes reverses published rankings | sections 4, 7 | experiments-reporting.md, instance sets | online bin packing only |
| Exclusion of training distributions from the test suite | section 3.2 | experiments-reporting.md, train/test separation | - |

## Difference from our work

The paper evaluates evolved heuristics empirically on one problem; it does not explain why particular instance classes favour
particular rules, a question that structural (graph- or instance-class) analysis can address.

## Experiments

- All heuristics are deterministic and run once per instance (section 4).
- Tuning: irace 3.5 default settings, 5,000 evaluations, on 5 instances from the training distribution (section 5).
- Instance generation: evolutionary algorithm over item order, 100 instances per heuristic; ISA on 10 features selected from 209 tsfresh features (section 6).
- Cost argument: cites the FunSearch estimate of the cost of one experiment (footnote 2, section 1) to weigh specialist gains against generation cost.

## Doubts and open questions

- Only online 1D bin packing; whether the conclusion transfers to other domains is untested here (see `Herrmann2026BinPacking`, `Quan2025ThreeDPacking`, `Gideoni2026SimpleBaselines`).
