# Reporting computational experiments

Rules for every experiment the author reports: heuristics, exact algorithms, and especially LLM-based optimization and
algorithm-design methods.
Field practice and its criticism: [../research/llm-optimization.md](../research/llm-optimization.md), section 9.
Tick list before submission: section 9 below, linked from [checklist.md](checklist.md).

Sources opened 2026-10-08: abstracts or text of every key cited here (reading notes in [../literature/](../literature/README.md)
for `RomeraParedes2024FunSearch`, `Liu2024EoH`, `Ye2024ReEvo`, `Zhang2024EvolutionarySearch`, `Sim2025BeyondHype`,
`Gideoni2026SimpleBaselines`); `Derrac2011Tutorial` and `Wilcoxon1945Ranking` are cited at title level only.

## 1. Questions before experiments

| Rule | Reason | Key |
|---|---|---|
| Write the research questions and the claim each experiment tests before running it. | Competitive "who is faster" testing does not explain why; controlled experiments do. | `Hooker1995Testing`, `BartzBeielstein2020Benchmarking` (clearly stated goals) |
| Name the binding constraint: LLM cost, LLM calls, evaluations, or wall-clock time. | Methods rank differently under different budget units. | `Gideoni2026SimpleBaselines` |
| Say whether the paper proposes a method or reports a discovery (a bound, a construction, a heuristic). | A good discovery does not show that the method is good; the two need different evidence. | `Gideoni2026SimpleBaselines` |
| Plan the full design (instances, baselines, runs, measures, analysis) in advance and disclose all of it. | Full disclosure of conditions is the basis of reproducibility of heuristic experiments. | `Barr1995Reporting`, `Rardin2001Tutorial`, `Johnson2002Guide` |

## 2. Instances

| Rule | Reason | Key |
|---|---|---|
| For each instance set give source, generator and parameters, seeds, sizes, number of instances per class. | Others must be able to rebuild the set; instance choice drives conclusions. | `Barr1995Reporting`, `Rardin2001Tutorial`, `McGeoch2012Guide` |
| Test on several instance classes, including public benchmark libraries, not one generator. | Evolved heuristics win on their training class and lose elsewhere. | `Sim2025BeyondHype` |
| Keep search (training), validation and test instances disjoint; exclude the training generator from the generalization test; report in- and out-of-distribution results separately. | Otherwise the test measures fit to the search distribution. | `Sim2025BeyondHype`, `Kapoor2023Leakage` |
| Make validation sets large enough for the noise of the score; re-evaluate the selected program on fresh data. | Small, noisy validation sets select programs by chance. | `Gideoni2026SimpleBaselines` |
| Treat public benchmarks and their best-known solutions as possibly seen by the LLM. Prefer fresh generated instances; hide the problem identity in prompts where possible; state which measures were taken. | Closed models were exposed to millions of benchmark samples; black-box prompting is one guard. | `Balloccu2024Leak`, `Ye2024ReEvo` |
| Before calling an instance set "well studied" or a result "new", check the literature on those instances and log the search in [../literature/searches.md](../literature/searches.md). | A published LLM novelty claim rested on instances that had not been studied before. | `Herrmann2026BinPacking` |
| For graph problems with known exact classes (e.g., Min Cut-Path on diameter-2 graphs), include instances with known optimum. | Gives exact gaps without a solver run. | suggestion, [../research/llm-optimization.md](../research/llm-optimization.md) section 12 |

## 3. Baselines and budgets

| Rule | Reason | Key |
|---|---|---|
| Include the strongest classical method you can run: an exact solver with a time limit, and the best problem-specific heuristic. | Gaps of ML methods to classical solvers grow on large real instances. | `Feng2026FrontierCO`, `Sun2026COBench` |
| Include the simple classical rules the field uses (e.g., first fit, best fit). | They are strong generalists. | `Sim2025BeyondHype` |
| For an LLM search method, include simple LLM baselines with the same model and prompt: independent sampling (IID RS), sequential conditioned sampling, (1+1)-EPS or hill climbing on the best verified program. | Simple baselines match or beat elaborate pipelines at equal budget. | `Gideoni2026SimpleBaselines`, `Zhang2024EvolutionarySearch`, `Beck2026HillSampling` (preprint) |
| Give all methods the same model, prompt knowledge, evaluator (search space) and budget in the binding unit. | Differences in prompt knowledge or formulation can exceed differences between pipelines. | `Gideoni2026SimpleBaselines` |
| Count hyperparameter tuning toward the budget. | Tuning on the target problem inflates sample efficiency. | `Gideoni2026SimpleBaselines` |
| Re-run competitors under your settings; mark any number copied from a paper and its original budget. | Settings differ between papers (initialization, termination, LLM). | `Zhang2024EvolutionarySearch` |
| Report wall-clock time with hardware, LLM calls, input and output tokens, and money per run and in total. | Cost is driven by tokens, not by the number of calls; one benchmark priced a run at about USD 10 to 200 depending on the model. | `Ye2024ReEvo`, `Zhang2024EvolutionarySearch` |

## 4. LLM specifics

Record for every model used:

| Item | Record | Reason / source |
|---|---|---|
| Model identifier | exact API snapshot string (`claude-sonnet-4-5-20250929`, not "Claude Sonnet"), provider, platform, access dates | providers retire models; requests to retired models fail. Anthropic: https://platform.claude.com/docs/en/about-claude/model-deprecations; OpenAI: https://developers.openai.com/api/docs/deprecations (both checked 2026-10-08) |
| Local weights | repository and revision of the weights, quantization, inference library and version, GPU | needed to rerun; `Zhang2024EvolutionarySearch` section 4.3 reports precision, library and GPU |
| Sampling | temperature, top-p, max tokens, samples per prompt, stop rules; note parameters the API ignores or rejects | some current APIs reject non-default sampling parameters (Anthropic page above: `temperature`, `top_p`, `top_k` deprecated for Claude Opus 4.7 and later, checked 2026-10-08) |
| Prompts | every template verbatim (system prompt, task text, skeleton code, few-shot examples) in an appendix or the repository | prompt knowledge changes results (`Gideoni2026SimpleBaselines`); EoH and ReEvo publish prompts in appendices (`Liu2024EoH`, `Ye2024ReEvo`) |
| Volume and cost | LLM calls, input and output tokens, money; per run and total | `Ye2024ReEvo` section 7 |
| Nondeterminism | number of independent runs; seeds of everything you control | outputs vary even in settings configured as deterministic (`Atil2024NonDeterminism`) |
| Logs | store every prompt and response, every generated program with its score | runs must stay checkable after the model is retired; logs also allow replay without API calls |
| Failures | share of generated programs that fail to parse, crash, time out, or are infeasible | invalid outputs are part of the method's cost (`RomeraParedes2024FunSearch` discards them; report how many) |

## 5. Runs and statistics

| Rule | Reason | Key |
|---|---|---|
| Run each randomized method many times independently; if runs are few, give the reason and the total time of the study. | Few runs give no statistical power; the guideline for cheap randomized algorithms is 1,000 runs per instance or a justification. | `Arcuri2011Guide` (section 9) |
| Know the floor of your test: with 5 paired observations the two-sided Wilcoxon signed-rank test cannot give p < 0.05 (smallest p = 2/2^5 = 0.0625). | Field practice is 3-5 runs (`Liu2024EoH`, `Ye2024ReEvo`, `Zhang2024EvolutionarySearch`). | arithmetic |
| Report the distribution: median and interquartile range or mean and standard deviation, min and max; box plots. | Means alone hide spread; mean and SD allow later meta-analysis. | `Arcuri2011Guide` |
| Give interval estimates: bootstrap confidence intervals for aggregates, probability of improvement for pairwise comparisons. | Point estimates from few runs mislead. | `Agarwal2021Precipice`, `Gideoni2026SimpleBaselines` |
| Two randomized methods on one instance: Mann-Whitney U (Wilcoxon rank-sum) test plus Vargha-Delaney A12 effect size. | Nonparametric; A12 is the probability that one method beats the other. | `Arcuri2011Guide`, `Vargha2000Effect` |
| Two methods over many instances (paired by instance): Wilcoxon signed-rank test. More than two methods: Friedman test with post-hoc tests, critical-difference diagram. | Recommended tests for comparisons over multiple data sets. | `Demsar2006Statistical`, `Wilcoxon1945Ranking`; EC tutorial `Derrac2011Tutorial` (title level) |
| Success or failure outcomes (bound reached or not): report k of n runs and use Fisher's exact test with the odds ratio. | Dichotomous data need their own test. | `Arcuri2011Guide`; example "4 of 140 runs" in `RomeraParedes2024FunSearch` |
| Correct for multiple comparisons and name the procedure, e.g., Benjamini-Hochberg false discovery rate. | Many tests inflate false positives. | `Benjamini1995FDR` |
| Report exact p-values and effect sizes, never "significant" alone. | Binary significance hides magnitude. | `Arcuri2011Guide`, `Gideoni2026SimpleBaselines` |
| For many solvers on many instances, add performance profiles. | Performance profiles are distribution functions of a performance metric over the instance set; they summarize many comparisons in one plot. | `Dolan2002Profiles` |
| For anytime methods, plot best-so-far quality against budget (evaluations, calls, dollars) with dispersion bands. | Rankings change with budget. | `Zhang2024EvolutionarySearch` (Fig. 4), `Hansen2021COCO` (runtime in function evaluations) |

Disputed: `Gideoni2026SimpleBaselines`, following `Agarwal2021Precipice`, advises against p-value tests with binary outcomes; the EC and
software-engineering tutorials prescribe nonparametric tests (`Derrac2011Tutorial`, `Arcuri2011Guide`), and `Arcuri2011Guide`
questions multiple-comparison adjustments when a decision must be made anyway. House rule: lead with effect sizes and intervals,
add tests with exact p-values and a named correction.

## 6. Tables and figures

- Generate every number in a table and every plot by a script from the raw result files; never type results by hand. Keep the script and a hash of the data in the repository. Reason: hand-copied numbers break silently when results change.
- Each table states instance class, number of instances, runs per instance, metric with its direction, and budget. Bold only differences that the statistics in section 5 support.
- Define the metric exactly and say when it differs from the compared paper: `RomeraParedes2024FunSearch` measures excess bins over the L2 lower bound, `Sim2025BeyondHype` over the sum-of-sizes bound.
- Typesetting (booktabs, siunitx, figure formats): [latex-guide.md](latex-guide.md) §8–§9.

## 7. Reproducibility package

In the project: code, configurations, instance lists, prompts and logs in `experiments/`, result tables in `data/`
([latex-conventions.md](latex-conventions.md) §1).

| Include | Reason / source |
|---|---|
| code of the method and of all baselines; configuration files; scripts that produce every table and figure | reproducibility types and obstacles in EC: `LopezIbanez2021Reproducibility`; code submission in ML: `Pineau2021Reproducibility` |
| instances or generators with seeds; train/validation/test split | `Kapoor2024REFORMS` (reporting checklist for ML-based science) |
| prompts, all LLM responses, all generated programs with scores | section 4; results remain checkable after model retirement |
| environment: language and library versions (lock file or container), OS, hardware | needed to rerun the evaluator |
| a license for code and data | reuse requires one; choice of license: [submission.md](submission.md) |
| archive with a DOI, cite the version DOI | Zenodo registers a DOI for every published upload and lets you reserve it before publishing (https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/); a version DOI identifies one release, the concept DOI resolves to the latest (https://zenodo.org/help/versioning); both checked 2026-10-08 |
| for a discovered construction: the object itself and an independent checker | the claim must not depend on the search code |

## 8. What to claim

- Claim results only for the instance classes, sizes, models and budgets tested. Reason: evolved heuristics specialize (`Sim2025BeyondHype`); method rankings change with the LLM (`Zhang2024EvolutionarySearch`).
- Separate "the found program is better on these instances" from "the method is better". (`Gideoni2026SimpleBaselines`)
- Credit the formulation and the domain knowledge put into prompts and skeletons; describe every human intervention in the loop. Reason: the formulation set the ceiling in `Gideoni2026SimpleBaselines`; FunSearch's best admissible-set result came after humans imposed a symmetry seen in an evolved program (`RomeraParedes2024FunSearch`).
- Write a limitations section: untested instance classes, model access and retirement, cost, number of runs, contamination risk, nondeterminism.
- Never write that an LLM "understands" or "discovers" without the evidence that the result is new (literature check) and correct (independent checker).

## 9. Reporting checklist

- [ ] Research questions and the binding budget unit stated before the results.
- [ ] Method claim and discovery claim kept apart.
- [ ] Instance sets: source, generator, parameters, seeds, sizes, counts; several classes; public sets included.
- [ ] Search, validation and test instances disjoint; in- and out-of-distribution reported separately.
- [ ] Contamination measures stated (fresh instances, hidden problem identity, or none).
- [ ] Strong classical baseline and simple classical rules included.
- [ ] Simple LLM baselines (IID sampling, sequential sampling, (1+1)-EPS or hill climbing) with the same model and prompts.
- [ ] Equal budgets in the binding unit; tuning counted; copied numbers marked.
- [ ] Model snapshot identifiers, provider, access dates; local weights revision if any.
- [ ] Sampling parameters, including those the API ignores.
- [ ] Prompts verbatim in appendix or repository.
- [ ] LLM calls, tokens, money, wall-clock, hardware per run and in total.
- [ ] Share of invalid generated programs.
- [ ] Number of independent runs with justification; seeds.
- [ ] Distributions (median and IQR or mean and SD), intervals, effect sizes, exact p-values, named multiple-comparison correction.
- [ ] Tables and figures generated by scripts from raw data; metrics defined with direction.
- [ ] Reproducibility package: code, instances, configs, prompts, logs, environment, license, version DOI.
- [ ] Claims limited to tested classes, models and budgets; limitations section present.
- [ ] Novelty of instances and results checked and logged in `knowledge/literature/searches.md`.
