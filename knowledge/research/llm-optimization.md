# LLMs for optimization and algorithm design: research map

Scope: the field of the dissertation *Optimisation Algorithms Powered by LLMs* ([../author.md](../author.md)): large language
models (LLMs) that design algorithms, act as optimizers or search operators, formulate optimization models, or search for
mathematical constructions; the critical literature on these methods; and the classical background they build on.

- Web check: 2026-10-08. Every work below has a bibliography entry checked that day on arXiv, Crossref or the proceedings page
  (now in [../bibliography/references.bib](../bibliography/references.bib)); its status line says VERIFIED or PARTIAL and where.
- Every statement about a work is traceable to its key. Reading level in the tables: **N** = reading note in
  [../literature/](../literature/README.md) (text read); **A** = abstract read 2026-10-08 only; **T** = title-level only.
  Take no precise claim into a manuscript from an A or T work without reading it first.
- Search log: [../literature/searches.md](../literature/searches.md). Reporting rules for own experiments:
  [../writing/experiments-reporting.md](../writing/experiments-reporting.md).

## 1. Directions

| Direction | Core idea | Representative works | Typical test problems |
|---|---|---|---|
| Algorithm design by evolutionary program search (EPS) | an LLM proposes code (a heuristic or a whole algorithm); an evaluator scores it on instances; an evolutionary loop keeps the best | `RomeraParedes2024FunSearch`, `Liu2024EoH`, `Ye2024ReEvo`, `VanStein2025LLaMEA`, `Novikov2025AlphaEvolve` | online bin packing, TSP (as guided local search or ant colony component), flow shop, BBOB functions, cap sets |
| LLM as optimizer or search operator | the LLM outputs candidate solutions, or acts as mutation/crossover inside an evolutionary algorithm | `Yang2024OPRO`, `Liu2024LMEA`, `Meyerson2024LMX`, `Lange2024EvoLLM` | small TSP, linear regression, prompt optimization, BBOB |
| Optimization modeling | natural-language problem to LP/MILP formulation and solver code | `Ramamonjison2022NL4Opt`, `Ahmaditeshnizi2024OptiMUS`, `Huang2025ORLM`, `Chen2026OPTEngine` | NL4Opt, NLP4LP, IndustryOR, generated OR problems |
| Constructions and counterexamples | search for objects that improve bounds or refute conjectures, with an exact checker | `Wagner2021Constructions`, `Charton2024PatternBoost`, `Georgiev2026MathDiscovery`, `Nagda2025Hardness`, `Bhan2026Zarankiewicz` | cap sets, Ramsey and Zarankiewicz numbers, spectral graph conjectures, gadget reductions |
| Critical and methodological studies | re-test published claims with stronger baselines, more instances, equal budgets | `Zhang2024EvolutionarySearch`, `Sim2025BeyondHype`, `Herrmann2026BinPacking`, `Gideoni2026SimpleBaselines` | the same problems as the methods they test |
| Surveys, benchmarks, platforms | taxonomies; shared problem suites; reusable code | `Liu2026AlgorithmDesignSurvey`, `DaRos2026COReview`, `Sun2026COBench`, `Feng2026FrontierCO`, `Liu2024LLM4AD` | suites of 8-36 combinatorial problems |
| Classical background | automatic design, selection and configuration of algorithms before LLMs | `Burke2013HyperHeuristics`, `Koza1994GeneticProgramming`, `Rice1976AlgorithmSelection`, `LopezIbanez2016Irace`, `Bengio2021MLforCO`, `Mitzenmacher2022Predictions` | - |

## 2. Algorithm design by evolutionary program search

| Key | Year | Venue | Contribution | Read |
|---|---|---|---|---|
| `Lehman2024ELM` | 2024 (arXiv 2022) | book chapter, Springer | code LLM as mutation operator in genetic programming, combined with MAP-Elites (Sodarace walkers) | A |
| `RomeraParedes2024FunSearch` | 2024 | Nature | frozen code LLM + evaluator + island model evolve a function inside a skeleton; new cap-set constructions and bin-packing heuristics | N |
| `Liu2024EoH` | 2024 | ICML | evolve a natural-language "thought" together with code; five prompt operators; about 2,000 queries for bin packing | N |
| `Ye2024ReEvo` | 2024 | NeurIPS | generator + reflector LLMs; short- and long-term reflection; components of GLS, ACO, GA and neural solvers | N |
| `VanStein2025LLaMEA` | 2025 | IEEE TEVC | LLM evolutionary loop generating whole black-box metaheuristics; tested on BBOB in 5D, checked in 10D and 20D | A |
| `Zheng2025MCTSAHD` | 2025 | ICML | Monte Carlo tree search over generated heuristics instead of a fixed-size population | A |
| `Novikov2025AlphaEvolve` | 2025 | arXiv white paper | coding agent editing whole programs with evaluator feedback; 4x4 complex matrix product with 48 multiplications; Google infrastructure uses | A |
| `Surina2025EvoTune` | 2025 | arXiv | fine-tune the LLM by reinforcement learning on signals from the evolutionary search (EvoTune) | A |
| `Lange2026ShinkaEvolve` | 2026 | ICLR | open-source framework; parent sampling, novelty rejection of code, bandit choice among LLMs; circle packing with 150 samples | A |
| `Wang2026ThetaEvolve` | 2026 | ICML | single open model with test-time reinforcement learning inside the evolutionary loop; new bounds with an 8B model | A |
| `Chen2026A2DEPT` | 2026 | ICML | tree-structured evolution of complete solvers rather than components of a fixed template; repair loop for executability | A |
| `Ke2026ASRO` | 2026 | ICML | co-evolution of solvers and instance generators as a two-player zero-sum game, against overfitting to fixed instances | A |
| `Hu2026AutoSND` | 2026 | arXiv | three-stage tree search that turns execution evidence into structural policies; network-dismantling programs on 15 real networks | A |

Established:
- An LLM-in-the-loop search with an exact evaluator produces programs that beat the classical hand-made rules on the instance
  distribution used during search (`RomeraParedes2024FunSearch` Table 1; `Liu2024EoH` Tables 1-3; `Ye2024ReEvo` section 5).
- Search adds value over plain sampling of the same LLM (`Zhang2024EvolutionarySearch` section 4.1; `Ye2024ReEvo` Table 5).
- Novelty argument: a result that beats the best-known value and passes the evaluator was not retrieved from training data
  (`RomeraParedes2024FunSearch`, Main). It covers the object found, not claims about the method.

Disputed:
- Value of elaborate components (thoughts, reflection, tree search, islands): no method wins on all problems and a (1+1) loop
  is competitive (`Zhang2024EvolutionarySearch`); simple sampling baselines match ShinkaEvolve under equal cost
  (`Gideoni2026SimpleBaselines`); hill climbing on the best verified program beats evolution and weight training on three
  bound problems (`Beck2026HillSampling`, preprint); ReEvo's authors expect the reflection effect to shrink with large budgets (`Ye2024ReEvo` section 7).
- Generalization beyond the search distribution: EoH reports good out-of-distribution results on TSPLib (`Liu2024EoH`);
  most evolved bin-packing heuristics do not generalize across instance classes (`Sim2025BeyondHype`); ASRO is motivated by
  overfitting to static instance sets (`Ke2026ASRO`).
- Sample-efficiency claims use different units: LLM queries (`Liu2024EoH`), heuristic evaluations (`Ye2024ReEvo`),
  samples (`Lange2026ShinkaEvolve`), money or wall-clock time (`Gideoni2026SimpleBaselines`). Claims are not comparable across units.
- Effect of the LLM: stronger models help (`Liu2024EoH` section 5.1) versus larger models not necessarily better and strong
  dependence of each method on the model (`Zhang2024EvolutionarySearch` sections 4.1.2, 4.2.2).
- Frozen versus trained operator: EvoTune and ThetaEvolve report gains from training the LLM during search
  (`Surina2025EvoTune`, `Wang2026ThetaEvolve`); no head-to-head comparison under equal compute found. TODO(verify).

## 3. LLMs as optimizers and search operators

| Key | Year | Venue | Contribution | Read |
|---|---|---|---|---|
| `Yang2024OPRO` | 2024 | ICLR | optimization by prompting: the prompt holds past solutions with scores, the LLM proposes new ones; shown on linear regression and TSP, main use prompt optimization | A |
| `Liu2024LMEA` | 2024 | IEEE CEC | LLM selects parents and performs crossover and mutation on TSP solutions; self-adaptive temperature; competitive up to 20 nodes | A |
| `Meyerson2024LMX` | 2024 | ACM TELO | few-shot prompting with parent genotypes as a crossover operator for any text representation | A |
| `Lange2024EvoLLM` | 2024 | GECCO Companion | LLM as recombination operator of an evolution strategy; beats random search and Gaussian hill climbing on BBOB | A |
| `Huang2024BlackBoxLLM` | 2024 | arXiv | evaluation of LLMs as black-box optimizers: weak on pure numerical tasks, more useful on non-numerical problems | A |

Established: LLMs can act as variation operators for text-encoded individuals (`Meyerson2024LMX`, `Lange2024EvoLLM`).
Disputed: usefulness as direct numerical optimizers (`Huang2024BlackBoxLLM`); reported scales are small (TSP up to 20 nodes in
`Liu2024LMEA`). EoH's authors note that direct solution generation struggles on large search spaces (`Liu2024EoH` section 2.2).

## 4. Optimization modeling

| Key | Year | Venue | Contribution | Read |
|---|---|---|---|---|
| `Ramamonjison2022NL4Opt` | 2022 | NeurIPS 2022 Competition Track (PMLR 220) | LP word-problem dataset; tasks: entity tagging and generation of a logical form for a solver | A |
| `Ahmaditeshnizi2024OptiMUS` | 2024 | ICML | modular LLM agent that formulates MILPs, writes and debugs solver code; NLP4LP dataset | A |
| `Huang2025ORLM` | 2025 | Operations Research | synthetic data (OR-Instruct) to train open 7B models for modeling; IndustryOR benchmark | A |
| `Chen2026OPTEngine` | 2026 | ICML | benchmark with controllable complexity over ten LP/MILP problem types; constraint formulation is the main bottleneck | A |
| `Xiao2025OptModelingSurvey` | 2025 | IJCAI (survey track) | survey; finds high error rates in modeling benchmarks, releases cleaned datasets and a leaderboard | A |

Established: pipelines that call a solver degrade less with problem complexity than pure text reasoning (`Chen2026OPTEngine`).
Disputed: benchmark quality and therefore published accuracies (`Xiao2025OptModelingSurvey`).

## 5. Constructions and counterexamples in combinatorics and complexity

| Key | Year | Venue | Contribution | Read |
|---|---|---|---|---|
| `Wagner2021Constructions` | 2021 | arXiv | reinforcement learning (deep cross-entropy method), not an LLM, refutes conjectures on graph eigenvalues and permanents | A |
| `Charton2024PatternBoost` | 2024 | arXiv | alternate local search with a transformer trained on the best constructions; counterexample to a 30-year-old conjecture | A |
| `Georgiev2026MathDiscovery` | 2026 | PNAS | AlphaEvolve on 67 problems in analysis, combinatorics, geometry, number theory; mostly rediscovers, sometimes improves best known | A |
| `Nagda2025Hardness` | 2025 | arXiv | AlphaEvolve finds gadget reductions: NP-hardness of approximating MAX-4-CUT (0.987), MAX-3-CUT (0.9649), metric TSP (111/110); evolved faster verifiers | A |
| `Nagda2026Ramsey` | 2026 | arXiv | AlphaEvolve improves lower bounds for nine classical Ramsey numbers | A |
| `Bhan2026Zarankiewicz` | 2026 | arXiv | OpenEvolve-based search; three exact Zarankiewicz numbers, 41 new lower bounds; under USD 30 per parameter set | A |
| `Pastorek2026AutoGraphForge` | 2026 | arXiv (submitted to ITAT 2026) | conjecture-refute-formalize pipeline for graph invariants: counterexample filtering on about 348,000 graphs, Lean 4 proofs with neural provers; work in progress | A |
| `Thakkar2026Conway99` | 2026 | arXiv | Conway's 99-graph (srg(99,14,1,2)): structural reduction to a constrained 12-regular graph on 84 vertices, CP-SAT encoding; an evolutionary program-search system produced a tabu move that beat 14 human-designed searches on a partial score; existence still open | A |

Established: with an exact, cheap checker, LLM-guided search improves best-known bounds on extremal and Ramsey-type problems
(`RomeraParedes2024FunSearch`, `Nagda2026Ramsey`, `Bhan2026Zarankiewicz`, `Georgiev2026MathDiscovery`); on graph existence
problems it can improve partial constructions without settling existence (`Thakkar2026Conway99`).
Disputed: how much of the gain is due to the pipeline rather than the human-chosen formulation and prompt knowledge;
reformulating the search space moved one bound more than any pipeline (`Gideoni2026SimpleBaselines` section 4.1).
Expensive verification is a bottleneck (`Nagda2025Hardness`).

## 6. Critical and methodological studies

| Key | Year | Venue | Finding | Read |
|---|---|---|---|---|
| `Zhang2024EvolutionarySearch` | 2024 | PPSN | unified benchmark: 4 EPS methods, 4 problems, 9 LLMs, 5 runs; search needed, no method dominates, (1+1)-EPS competitive | N |
| `Sim2025BeyondHype` | 2025 | EvoApplications | 6,064 bin-packing instances from 12 datasets: Best Fit ranks first; evolved heuristics specialize to their training class | N |
| `Herrmann2026BinPacking` | 2026 | ACM TELO | LLM-evolved bin-packing heuristics stay opaque to experts; hand-derived algorithms for the same instances are simpler, more efficient and more general; the instances are simple and had not been studied before, contrary to the novelty claim | A |
| `Gideoni2026SimpleBaselines` | 2026 | arXiv | IID sampling and sequential conditioned sampling match code-evolution systems at equal budget in three domains | N |
| `Quan2025ThreeDPacking` | 2025 | arXiv | asked to build a full 3D-packing solver, the LLM concentrates on the scoring function; result comparable to a human greedy | A |
| `VanStein2025CEG` | 2025 | GECCO | code evolution graphs: generated code grows more complex over iterations, which can hurt; LLMs differ in coding style | A |
| `Beck2026HillSampling` | 2026 | arXiv | hill climbing with a frozen open-weight LLM (always condition on the best verified program) beats repeated sampling, evolution strategies on weights, and reported results on circle packing and Erdős' minimum overlap | A |

Recurring criticisms: weak or missing baselines; few instances from one distribution; unequal budgets and prompt knowledge;
single runs; novelty claims without checking prior literature on the instances (`Herrmann2026BinPacking`).

## 7. Surveys, benchmarks and platforms

| Key | Year | Venue | Content | Read |
|---|---|---|---|---|
| `Liu2026AlgorithmDesignSurvey` | 2026 | ACM Computing Surveys | systematic survey; taxonomy of LLM roles: optimizer, predictor, extractor, designer | A |
| `DaRos2026COReview` | 2026 | ACM Computing Surveys | PRISMA review of LLMs for combinatorial optimization, 103 studies selected from over 2,000 | A |
| `Xiao2025OptModelingSurvey` | 2025 | IJCAI | survey of LLM optimization modeling (section 4) | A |
| `Liu2024LLM4AD` | 2024 | arXiv | Python platform: modular search methods, tasks, LLM interface, evaluation sandbox | A |
| `VanStein2025BLADE` | 2025 | GECCO Companion | benchmark suite for LLM-designed continuous black-box optimizers; logging and IOHanalyzer integration | A |
| `Sun2026COBench` | 2026 | AAAI | 36 real-world combinatorial problems for LLM agents, compared with human-designed algorithms | A |
| `Chen2026HeuriGym` | 2026 | ICLR | 9 problems, agentic loop with execution feedback; Quality-Yield Index; best models around 0.6 against expert 1 | A |
| `Feng2026FrontierCO` | 2026 | ICLR | 8 problems with competition and industrial instances up to millions of nodes; 16 ML solvers vs classical solvers; gap grows with size | A |
| `Imajuku2025ALEBench` | 2025 | NeurIPS Datasets and Benchmarks | AtCoder Heuristic Contest tasks; long-horizon score-based algorithm engineering | A |
| `Tang2025GraphArena` | 2025 | ICLR | LLMs solving 4 polynomial and 6 NP-complete graph tasks directly; outputs classed as correct, suboptimal, hallucinatory, missing | A |

## 8. Classical background

| Key | Year | Venue | Anchor for | Read |
|---|---|---|---|---|
| `Burke2013HyperHeuristics` | 2013 | J. Oper. Res. Soc. | hyper-heuristics: search over heuristics (selection or generation), not over solutions | A |
| `Koza1994GeneticProgramming` | 1994 | Statistics and Computing | genetic programming: evolving programs by selection and crossover | A |
| `Rice1976AlgorithmSelection` | 1976 | Advances in Computers | the algorithm selection problem | T |
| `LopezIbanez2016Irace` | 2016 | Oper. Res. Perspectives | automatic algorithm configuration by iterated racing (irace) | A |
| `Bengio2021MLforCO` | 2021 | EJOR | machine learning inside combinatorial optimization; problems as samples from a distribution | A |
| `Mitzenmacher2022Predictions` | 2022 | Communications of the ACM | algorithms with predictions (learning-augmented algorithms), beyond worst-case analysis | T |

Relation used by the LLM papers themselves: EPS is genetic programming with an LLM as the variation operator and free-form code
as representation (`Zhang2024EvolutionarySearch` Appendix A.1; `Ye2024ReEvo` section 4); ReEvo defines its method as a
hyper-heuristic (`Ye2024ReEvo` Definitions 3.1-3.2).

## 9. How the field evaluates

| Aspect | Observed practice | Pitfall raised | Keys |
|---|---|---|---|
| Instances | a few generated instances for search (5 Weibull instances, 64 random TSP100), tests on related sets (OR-Library, TSPLib, Taillard) | narrow classes; few instances per class; test sets from the search distribution | `Liu2024EoH`, `Ye2024ReEvo`, `Sim2025BeyondHype` |
| Train/test | evolve on one distribution, test on other sizes or real instances | exclude training distributions from tests; instance classes may be easy | `Sim2025BeyondHype`, `Herrmann2026BinPacking` |
| Baselines | hand-made rules (first/best fit, insertion), neural solvers, OR-Tools, published heuristics of rival methods | random or naive baselines only; rival methods not re-run at equal budget; simple LLM baselines missing | `Zhang2024EvolutionarySearch`, `Gideoni2026SimpleBaselines`, `Liu2024EoH` |
| Strong classical solvers | rarely in EPS papers; central in benchmarks | gap to classical solvers widens on large real instances | `Feng2026FrontierCO`, `Sun2026COBench` |
| Budget | LLM queries, heuristic evaluations, samples, USD, wall-clock, days per run | units differ between papers; tuning budgets not counted | `Liu2024EoH`, `Ye2024ReEvo`, `Zhang2024EvolutionarySearch`, `Gideoni2026SimpleBaselines` |
| Cost reporting | USD per run (about 10 to 200 for 10,000 evaluations with 2024 API models; about 0.06 for ReEvo's 100 evaluations); FunSearch reports about 10^6 samples | cost dominated by tokens, not query count | `Zhang2024EvolutionarySearch`, `Ye2024ReEvo`, `RomeraParedes2024FunSearch` |
| Runs | 1-5 runs per configuration; FunSearch reports success frequency (4 of 140 runs for the 512-cap) | single runs of expensive systems; few runs for many comparisons | `RomeraParedes2024FunSearch`, `Zhang2024EvolutionarySearch`, `Gideoni2026SimpleBaselines` |
| Statistics | mean and standard deviation, box plots; bootstrap CIs and probability of improvement in recent work | no tests; validation noise selects overfit programs | `Gideoni2026SimpleBaselines`, `Agarwal2021Precipice` |
| Models | GPT-3.5-turbo, GPT-4, Claude 3 Opus, Gemini 2.5, CodeLlama, DeepSeek-Coder, small open models with RL | family names without snapshot or access date; outputs vary even in "deterministic" settings; API models are retired and requests then fail | `Zhang2024EvolutionarySearch`, `Wang2026ThetaEvolve`, `Atil2024NonDeterminism`; provider deprecation pages (URLs in experiments-reporting.md, checked 2026-10-08) |
| Contamination | "black-box" prompts that hide the problem identity; novelty via beating best-known values | public benchmarks leak into closed models | `Ye2024ReEvo`, `RomeraParedes2024FunSearch`, `Balloccu2024Leak` |

## 10. Where it is published

Observed from the verified entries above (not a venue ranking; venue rules: [../venues/README.md](../venues/README.md)):

| Community | Venues with entries here |
|---|---|
| Machine learning | ICML (`Liu2024EoH`, `Zheng2025MCTSAHD`, `Wang2026ThetaEvolve`, `Chen2026A2DEPT`, `Ke2026ASRO`, `Ahmaditeshnizi2024OptiMUS`, `Chen2026OPTEngine`), NeurIPS (`Ye2024ReEvo`, `Imajuku2025ALEBench`), ICLR (`Yang2024OPRO`, `Tang2025GraphArena`, `Lange2026ShinkaEvolve`, `Chen2026HeuriGym`, `Feng2026FrontierCO`) |
| Evolutionary computation | IEEE TEVC (`VanStein2025LLaMEA`), ACM TELO (`Meyerson2024LMX`, `Herrmann2026BinPacking`), GECCO and companion (`Lange2024EvoLLM`, `VanStein2025CEG`, `VanStein2025BLADE`), PPSN (`Zhang2024EvolutionarySearch`), EvoApplications (`Sim2025BeyondHype`), CEC (`Liu2024LMEA`) |
| AI general | AAAI (`Sun2026COBench`), IJCAI (`Xiao2025OptModelingSurvey`) |
| Operations research | Operations Research (`Huang2025ORLM`), EJOR (`Bengio2021MLforCO`) |
| Surveys | ACM Computing Surveys (`Liu2026AlgorithmDesignSurvey`, `DaRos2026COReview`) |
| Multidisciplinary | Nature (`RomeraParedes2024FunSearch`), PNAS (`Georgiev2026MathDiscovery`) |
| Preprint only (2026-10-08) | `Novikov2025AlphaEvolve`, `Surina2025EvoTune`, `Liu2024LLM4AD`, `Gideoni2026SimpleBaselines`, `Beck2026HillSampling`, `Hu2026AutoSND`, `Thakkar2026Conway99`, `Quan2025ThreeDPacking`, `Nagda2025Hardness`, `Nagda2026Ramsey`, `Bhan2026Zarankiewicz`, `Pastorek2026AutoGraphForge`, `Charton2024PatternBoost`, `Wagner2021Constructions`, `Huang2024BlackBoxLLM` |

## 11. Terminology

| Term | Meaning |
|---|---|
| automatic heuristic design (AHD) | selecting, tuning or constructing heuristics automatically for a problem class (`Liu2024EoH`) |
| hyper-heuristic | search method over a space of heuristics; selection or generation type (`Burke2013HyperHeuristics`) |
| language hyper-heuristic (LHH) | hyper-heuristic whose heuristics are generated by an LLM (`Ye2024ReEvo`) |
| evolutionary program search (EPS) | code as individuals, evolutionary loop, LLM as variation engine (`Zhang2024EvolutionarySearch`) |
| code evolution | same family of methods, term used by `Gideoni2026SimpleBaselines` |
| searching in function space | FunSearch's framing: evolve a program that builds the solution, not the solution (`RomeraParedes2024FunSearch`) |
| skeleton / template | fixed program around the evolved function, e.g. a greedy loop calling a priority function |
| priority (score) function | the evolved part: assigns a score to each choice inside the skeleton |
| evaluator | code that runs a candidate on instances and returns a score; rejects invalid or time-out programs |
| meta-objective | performance of a heuristic averaged over a set of instances (`Ye2024ReEvo`) |
| best-shot prompting | prompt built from k high-scoring programs ordered by score (`RomeraParedes2024FunSearch`) |
| island model | several sub-populations evolved separately, with periodic reset of the worst ones |
| thought | natural-language description of a heuristic evolved with its code (`Liu2024EoH`) |
| reflection | LLM-written comparison of parents used as a hint for the next generation (`Ye2024ReEvo`) |
| white-box / black-box prompting | prompt reveals or hides the identity of the problem (`Ye2024ReEvo`) |
| LLM as optimizer | LLM proposes candidate solutions directly from a scored history (`Yang2024OPRO`) |
| LLM crossover / mutation | LLM used as variation operator on text-encoded individuals (`Meyerson2024LMX`) |
| optimization modeling | turning a natural-language problem into a mathematical program and solver code |
| solver-integrated reasoning | LLM writes the model, an external solver solves it (`Chen2026OPTEngine`) |
| test-time training / RL in the loop | updating the LLM's weights with search feedback (`Surina2025EvoTune`, `Wang2026ThetaEvolve`) |
| sample efficiency | quality reached per sample, query, evaluation or dollar; state the unit |
| query budget / evaluation budget | cap on LLM calls / on heuristic evaluations |
| data contamination (leakage) | test data or solutions present in the model's training data (`Balloccu2024Leak`) |
| in- / out-of-distribution | test instances from the same / a different generator than the search instances |
| instance space analysis | projection of instances to 2D to show where each algorithm wins (`Sim2025BeyondHype`) |
| algorithm selection | choosing the best algorithm per instance (`Rice1976AlgorithmSelection`) |
| algorithm configuration | tuning parameters of an algorithm over an instance distribution (`LopezIbanez2016Irace`) |
| algorithms with predictions | algorithms using possibly wrong learned advice, analysed beyond worst case (`Mitzenmacher2022Predictions`) |
| gadget reduction | hardness proof built from small finite gadgets; searchable by computer (`Nagda2025Hardness`) |
| probability of improvement | chance that one run of A beats one run of B (`Agarwal2021Precipice`, `Gideoni2026SimpleBaselines`) |

## 12. Possible links to the author's earlier work (suggestions)

Suggestions for discussion with the supervisor, not decisions. Min Cut-Path facts: [min-cut-path.md](min-cut-path.md).

| Earlier work | Possible link | Why it could fit |
|---|---|---|
| Min Cut-Path is NP-complete (article 1) and has polynomial classes (diameter 2; all cuts at most 2) where `cp = c + d - 1` | use Min Cut-Path as an EPS test problem with exact ground truth on the polynomial classes and on small graphs | evaluator is cheap and exact; the EPS papers read here (N) test bin packing, routing, scheduling and cap sets, none a graph problem with exactly solvable classes; `Tang2025GraphArena` evaluates LLMs solving graph problems directly, without evolutionary search |
| formula `cp = c + d - 1` fails in the class *diam or cut 2* (thesis, counterexamples) | LLM-guided construction search for graphs maximizing `cp - max(c, d)` or violating the formula in new classes | construction search with an exact checker is the setting where LLM search has improved bounds (`Bhan2026Zarankiewicz`, `Nagda2026Ramsey`) |
| only a trivial 2-approximation is known (thesis Claim 8) | gadget search for inapproximability of Min Cut-Path, following the method of `Nagda2025Hardness` | the hardness proof of article 1 is itself a gadget reduction from 3-SAT |
| random graphs: `G(n, 1/α)` has diameter 2 a.a.s.; average-case (1+ε)-approximation scheme for `p ≥ α log n / n` | generators with known structure for clean train/test splits and contamination-free instances | addresses the instance-class criticism of `Sim2025BeyondHype` |
| complexity background | analyse evolved heuristics: worst-case examples, classes where they are exact | the literature reports instance averages only (section 9) |
| cuts and connectivity (Min Cut-Path combines a cut with a path) | evolve heuristics for related graph-cut problems such as network dismantling, where LLM search has been applied (`Hu2026AutoSND`) | a graph problem with an existing LLM baseline to compare against |

## 13. Questions for the author

1. Which direction is the core of the dissertation: designing heuristics (section 2), LLMs as optimizers (3), modeling (4), or discovery of constructions (5)?
2. Which problems: graph problems close to Min Cut-Path, classical combinatorial benchmarks, or an application domain?
3. Compute: API budget per month, access to local GPUs at UPJŠ, and whether closed models are acceptable for the main results.
4. Is a theoretical component expected (complexity of the target problems, guarantees for evolved heuristics)?
5. Target community: evolutionary computation (GECCO, PPSN, TELO), machine learning (ICML, NeurIPS, ICLR), or operations research?
6. Build on an existing platform (`Liu2024LLM4AD`, OpenEvolve, `Lange2026ShinkaEvolve`) or write a minimal own loop as baseline?
7. What does the supervisor expect for the written part of the dissertation exam (see [../writing/thesis.md](../writing/thesis.md))?

## 14. Unverified leads

Cited by the works above or seen in search results; not verified, not in the bibliography.

- OpenEvolve (open-source AlphaEvolve-style framework used by `Bhan2026Zarankiewicz`, cited as "Sharma, 2025" by `Gideoni2026SimpleBaselines`). TODO(verify) repository and citation.
- ADAS (automated design of agentic systems, "Hu et al., 2024"), AIDE and MLE-bench ("Chan et al., 2024"), all cited by `Gideoni2026SimpleBaselines`. TODO(verify).
- Eureka (LLM-evolved reward functions), cited by `Zhang2024EvolutionarySearch`. TODO(verify).
- DeepACO (Ye et al.), the neural ACO baseline of `Ye2024ReEvo`. TODO(verify).
- Instance Space Analysis methodology (reference [28] of `Sim2025BeyondHype`). TODO(verify).
- Stützle and López-Ibáñez (2019) on automated algorithm design, cited by `Liu2024EoH`. TODO(verify).
- AlphaResearch (arXiv 2511.08522) and ResearchEVO (arXiv 2604.05587), seen in a web search 2026-10-08. TODO(verify) content and status.
- Kunisky and Yu, the certification result improved by `Nagda2025Hardness`. TODO(verify).
- Recent preprints listed by the arXiv searches of 2026-10-08 but not assessed (SimpleEvol, MOSAIC, FrugalEvo, AlphaEvolve and the matrix-multiplication exponent, HSEvo): identifiers in [../literature/searches.md](../literature/searches.md). TODO(verify).
- Published versions of `Novikov2025AlphaEvolve`, `Surina2025EvoTune` (ICLR 2025 workshop listing seen), `Gideoni2026SimpleBaselines`, `Liu2024LLM4AD`: none found 2026-10-08; re-check before citing.

## Maintenance

- Add a work: verify the entry ([../bibliography/README.md](../bibliography/README.md)), add a row to the right table with its read level, log the search in [../literature/searches.md](../literature/searches.md).
- Upgrade A to N only after writing a reading note.
- Re-run the searches in [../literature/searches.md](../literature/searches.md) before any related-work section is submitted; this field moves monthly.
