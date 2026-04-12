# Java Fix Correctness Analysis (Data-Contamination Control)

This document summarizes the **manual correctness analysis** of Java fixes generated under the NO_EXPLANATION baseline. Since the pipeline cannot compile or run Java tests, each fix was manually inspected against the original buggy source code and the known ground-truth bug description.

## Purpose

The Java NO_EXPLANATION experiment serves as a **data-contamination control**: if an LLM can fix original Defects4J bugs in Java at a comparable rate to the translated Python versions, it may indicate that the model has memorized these well-known patches from its training data rather than reasoning about the code.

## Methodology

For each of 12 Java defects × 3 runs × 3 models = **108 total fixes**:

1. Read the raw fix file (`results/<model>/no_explanation_java/runs/java/defectN_java_NO_EXPLANATION_runM_fix_raw.java`)
2. Compared against the original buggy Java source (`failures/java_defects/`)
3. Verified whether the fix addresses the specific known bug for that defect
4. Recorded verdict (TRUE/FALSE) with description and notes

> [!IMPORTANT]
> Unlike the Python pipeline, there is **no automated test validation** for Java fixes.
> Verdicts are based on manual code inspection against known bug descriptions.

## Result Files

| Model | CSV Location | Pass Rate |
|-------|-------------|-----------|
| GPT-5-mini | `results/gpt_5_mini/no_explanation_java/java_fix_correctness.csv` | **28/36 (78%)** |
| Grok 4.1 Fast | `results/grok_4_1_fast/no_explanation_java/java_fix_correctness.csv` | **27/36 (75%)** |
| DeepSeek-V3.2 | `results/deepseek_v3_2/no_explanation_java/java_fix_correctness.csv` | **26/36 (72%)** |

Each CSV contains columns: `defect_id`, `run_id`, `fix_correct`, `known_bug`, `fix_description`, `notes`.

## Per-Defect Breakdown

| Defect | Bug Description | GPT-5-mini | Grok 4.1 | DeepSeek |
|--------|----------------|------------|-----------|----------|
| defect1 | Minutes validation rejects negative offsets | 3/3 | 3/3 | 2/3 |
| defect2 | Grayscale uses unclamped value | 3/3 | 3/3 | 3/3 |
| defect3 | Surrogate pair advancement | 1/3 | 3/3 | 3/3 |
| defect4 | minMiddleIndex / maxMiddleIndex swap | 3/3 | 3/3 | 3/3 |
| defect5 | ClassCastException (copyArrayGrow1) | 3/3 | 1/3 | 2/3 |
| defect6 | Missing negative zero handling | 3/3 | 0/3 | 2/3 |
| defect7 | NullPointerException (null array element) | 3/3 | 0/3 | 3/3 |
| defect8 | fr__POSIX locale double underscore | 3/3 | 3/3 | 0/3 |
| defect9 | Null replacement NPE | 3/3 | 3/3 | 3/3 |
| defect10 | Empty string after type qualifier strip | 0/3 | 3/3 | 0/3 |
| defect11 | start/end bounds validation | 1/3 | 3/3 | 0/3 |
| defect12 | StringIndexOutOfBounds in abbreviate | 3/3 | 3/3 | 3/3 |

## Key Observations

### Model Strengths

- **GPT-5-mini** excels at "obviously missing checks" (null guards, negative zero, type casting) but struggles with edge cases requiring precise string content (defect10, defect11).
- **Grok 4.1 Fast** handles subtle edge cases well (defect10 empty-string guard, defect11 bounds validation) but completely misses null-check bugs (defect6, defect7).
- **DeepSeek-V3.2** shows balanced performance but consistently fails on locale parsing (defect8), empty-string edge cases (defect10), and error message formatting (defect11).

### Universally Solved (all models, all runs)

defect2, defect4, defect9, defect12 — these may be the most "memorizable" or straightforward bugs.

### Universally Difficult

No defect was failed by all three models, but defect10 (empty string after strip) was only solved by Grok.

### Contamination Signal

- **defect5 run 2 (GPT-5-mini)**: The fix references the JIRA issue `LANG-571` by name, which is a strong signal that the model has seen the original Defects4J bug report in its training data.
- High overall pass rates (72–78%) on well-known Defects4J bugs suggest familiarity with these patches.

## Related Documentation

- [fix_process.md](./fix_process.md) — Fix generation pipeline (Python + Java modes)
- [comparison_process.md](./comparison_process.md) — Ground truth comparison (Python only)
- Runner script: `scripts/standalone/run_java_no_explanation.py`
- Java defect definitions: `src/java_data.py`
- Java source files: `failures/java_defects/`
