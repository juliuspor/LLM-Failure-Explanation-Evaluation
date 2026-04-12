import json
import os
import glob
import argparse
from collections import defaultdict
from statistics import mean, stdev

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def evaluate_consistency(directory, pattern, output_path=None):
    file_paths = sorted(glob.glob(os.path.join(directory, pattern)))
    if not file_paths:
        print(f"No files found matching {pattern} in {directory}")
        return

    print(f"Comparing {len(file_paths)} runs: {[os.path.basename(p) for p in file_paths]}")

    # Map: (defect_id, levels) -> [list of scores from each run]
    combined_results = defaultdict(list)
    
    for path in file_paths:
        data = load_json(path)
        for item in data:
            scores = item.get('scores')
            if scores is None:
                continue  # Skip entries without explanation scores
            key = (item['defect_id'], item['levels'])
            combined_results[key].append(scores)

    criteria = ["C1_Readability", "C2_Problem_Identification", "C3_Explanation_Clarity", 
                "C4_Actionability", "C5_Contextual_Adequacy", "C6_Brevity"]

    # Statistics per level
    levels_stats = defaultdict(lambda: {
        "total": 0, 
        "criterion_matches": {c: 0 for c in criteria}, 
        "all_match": 0
    })

    total_configs = 0
    total_criterion_matches = {c: 0 for c in criteria}
    total_all_match = 0

    for (defect_id, level), scores_list in combined_results.items():
        if len(scores_list) < 2:
            continue  # Need at least two runs to compare
        
        total_configs += 1
        levels_stats[level]["total"] += 1
        
        # Check overall match (all criteria identical across all runs)
        first_scores = scores_list[0]
        
        # Per-criterion matches across all runs
        for c in criteria:
            if all(run.get(c) == first_scores.get(c) for run in scores_list[1:]):
                total_criterion_matches[c] += 1
                levels_stats[level]["criterion_matches"][c] += 1
        
        # All criteria must match across all runs
        if all(
            all(run.get(c) == first_scores.get(c) for c in criteria)
            for run in scores_list[1:]
        ):
            total_all_match += 1
            levels_stats[level]["all_match"] += 1

    if total_configs == 0:
        print("No configurations with at least 2 runs found.")
        return

    # Print Report
    print(f"\nOverall Consistency (across all {len(file_paths)} runs - All Levels):")
    print(f"Total Unique (Defect, Level) Configs: {total_configs}")
    for c in criteria:
        pct = (total_criterion_matches[c] / total_configs) * 100
        print(f"  {c:25}: {pct:6.2f}% ({total_criterion_matches[c]}/{total_configs})")
    print(f"  {'Overall (All match)':25}: {total_all_match / total_configs * 100:6.2f}% ({total_all_match}/{total_configs})")

    print(f"\nConsistency per Level (across all {len(file_paths)} runs):")
    sorted_levels = sorted(levels_stats.keys())
    for level in sorted_levels:
        stats = levels_stats[level]
        total = stats["total"]
        print(f"\n--- {level} (n={total}) ---")
        for c in criteria:
            match_count = stats["criterion_matches"][c]
            pct = (match_count / total) * 100
            print(f"  {c:25}: {pct:6.2f}% ({match_count}/{total})")
        print(f"  {'Overall (All match)':25}: {stats['all_match'] / total * 100:6.2f}% ({stats['all_match']}/{total})")

    # Prepare JSON Output
    if output_path:
        output_data = {
            "metadata": {
                "runs_compared": [os.path.basename(p) for p in file_paths],
                "total_configs": total_configs,
                "criteria": criteria
            },
            "overall": {
                "per_criterion": {c: total_criterion_matches[c] / total_configs for c in criteria},
                "all_match": total_all_match / total_configs
            },
            "per_level": {}
        }
        for level, stats in levels_stats.items():
            total = stats["total"]
            output_data["per_level"][level] = {
                "total": total,
                "per_criterion": {c: stats["criterion_matches"][c] / total for c in criteria},
                "all_match": stats["all_match"] / total
            }
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to {output_path}")


def analyze_score_passrate_correlation(directory, pattern, output_path=None):
    """
    Analyze correlation between explanation quality scores and fix validation pass rates.
    
    This answers the question: Does a better scoring explanation lead to a better pass rate?
    """
    file_paths = sorted(glob.glob(os.path.join(directory, pattern)))
    if not file_paths:
        print(f"No files found matching {pattern} in {directory}")
        return

    print(f"\n{'='*80}")
    print("SCORE-TO-PASS-RATE CORRELATION ANALYSIS")
    print(f"{'='*80}")
    print(f"Analyzing {len(file_paths)} runs: {[os.path.basename(p) for p in file_paths]}")

    criteria = ["C1_Readability", "C2_Problem_Identification", "C3_Explanation_Clarity", 
                "C4_Actionability", "C5_Contextual_Adequacy", "C6_Brevity"]

    # Collect all data points: (defect_id, levels) -> {scores: [...], passed: [...]}
    combined_data = defaultdict(lambda: {"scores": [], "passed": []})
    
    for path in file_paths:
        data = load_json(path)
        for item in data:
            scores = item.get('scores')
            if scores is None:
                continue  # Skip entries without explanation scores
            key = (item['defect_id'], item['levels'])
            validation = item.get("validation") or item.get("verification", {})
            passed = validation.get('passed', False) if validation else False
            combined_data[key]["scores"].append(scores)
            combined_data[key]["passed"].append(passed)

    # Aggregate per context level
    level_stats = defaultdict(lambda: {
        "total_runs": 0,
        "total_passed": 0,
        "criterion_scores": {c: [] for c in criteria},
        "total_scores": [],
        "defect_breakdown": []
    })

    for (defect_id, level), data in combined_data.items():
        scores_list = data["scores"]
        passed_list = data["passed"]
        
        num_runs = len(scores_list)
        num_passed = sum(1 for p in passed_list if p)
        
        level_stats[level]["total_runs"] += num_runs
        level_stats[level]["total_passed"] += num_passed
        
        # Aggregate criterion scores across all runs for this defect/level
        for scores in scores_list:
            total_score = 0
            for c in criteria:
                score = scores.get(c, 0)
                if isinstance(score, (int, float)):
                    level_stats[level]["criterion_scores"][c].append(score)
                    total_score += score
            level_stats[level]["total_scores"].append(total_score)
        
        # Track per-defect breakdown
        avg_scores = {}
        for c in criteria:
            c_scores = [s.get(c, 0) for s in scores_list if isinstance(s.get(c), (int, float))]
            avg_scores[c] = mean(c_scores) if c_scores else 0
        
        level_stats[level]["defect_breakdown"].append({
            "defect_id": defect_id,
            "runs": num_runs,
            "passed": num_passed,
            "pass_rate": num_passed / num_runs if num_runs > 0 else 0,
            "avg_scores": avg_scores,
            "avg_total": sum(avg_scores.values())
        })

    # Compute summary stats per level
    level_summaries = []
    for level, stats in level_stats.items():
        total_runs = stats["total_runs"]
        total_passed = stats["total_passed"]
        pass_rate = total_passed / total_runs if total_runs > 0 else 0
        
        criterion_avgs = {}
        for c in criteria:
            scores = stats["criterion_scores"][c]
            criterion_avgs[c] = mean(scores) if scores else 0
        
        avg_total_score = mean(stats["total_scores"]) if stats["total_scores"] else 0
        
        level_summaries.append({
            "level": level,
            "total_runs": total_runs,
            "total_passed": total_passed,
            "pass_rate": pass_rate,
            "criterion_avgs": criterion_avgs,
            "avg_total_score": avg_total_score
        })

    # Sort by avg_total_score descending (best scoring first)
    level_summaries.sort(key=lambda x: x["avg_total_score"], reverse=True)

    # Print ranking by explanation score
    print(f"\n{'='*80}")
    print("CONTEXT LEVELS RANKED BY AVERAGE EXPLANATION SCORE")
    print(f"{'='*80}")
    print(f"{'Rank':<5} {'Level':<35} {'Avg Score':>10} {'Pass Rate':>12} {'Passed/Total':>15}")
    print("-" * 80)
    
    for rank, summary in enumerate(level_summaries, 1):
        level = summary["level"]
        avg_score = summary["avg_total_score"]
        pass_rate = summary["pass_rate"]
        passed = summary["total_passed"]
        total = summary["total_runs"]
        print(f"{rank:<5} {level:<35} {avg_score:>10.2f} {pass_rate*100:>11.1f}% {passed:>6}/{total:<6}")

    # Analyze correlation: group by score quartiles
    print(f"\n{'='*80}")
    print("PASS RATE BY EXPLANATION SCORE QUARTILE")
    print(f"{'='*80}")
    
    # Collect all individual data points (score, passed)
    all_datapoints = []
    for (defect_id, level), data in combined_data.items():
        for scores, passed in zip(data["scores"], data["passed"]):
            total_score = sum(scores.get(c, 0) for c in criteria if isinstance(scores.get(c), (int, float)))
            all_datapoints.append({"score": total_score, "passed": passed})
    
    # Sort by score and divide into quartiles
    all_datapoints.sort(key=lambda x: x["score"])
    n = len(all_datapoints)
    quartile_size = n // 4
    
    quartiles = [
        ("Q1 (Lowest)", all_datapoints[:quartile_size]),
        ("Q2", all_datapoints[quartile_size:2*quartile_size]),
        ("Q3", all_datapoints[2*quartile_size:3*quartile_size]),
        ("Q4 (Highest)", all_datapoints[3*quartile_size:])
    ]
    
    quartile_results = []
    print(f"{'Quartile':<20} {'Score Range':>15} {'Pass Rate':>12} {'Passed/Total':>15}")
    print("-" * 65)
    
    for name, points in quartiles:
        if not points:
            continue
        scores = [p["score"] for p in points]
        passed_count = sum(1 for p in points if p["passed"])
        total_count = len(points)
        pass_rate = passed_count / total_count if total_count > 0 else 0
        score_min = min(scores)
        score_max = max(scores)
        
        quartile_results.append({
            "quartile": name,
            "score_min": score_min,
            "score_max": score_max,
            "pass_rate": pass_rate,
            "passed": passed_count,
            "total": total_count
        })
        
        print(f"{name:<20} {score_min:>5.1f} - {score_max:<5.1f} {pass_rate*100:>11.1f}% {passed_count:>6}/{total_count:<6}")

    # Per-criterion analysis
    print(f"\n{'='*80}")
    print("PASS RATE BY INDIVIDUAL CRITERION SCORE")
    print(f"{'='*80}")
    
    criterion_correlation = {}
    for c in criteria:
        score_0_passed = 0
        score_0_total = 0
        score_1_passed = 0
        score_1_total = 0
        
        for (defect_id, level), data in combined_data.items():
            for scores, passed in zip(data["scores"], data["passed"]):
                score = scores.get(c)
                if isinstance(score, (int, float)):
                    if score == 0:
                        score_0_total += 1
                        if passed:
                            score_0_passed += 1
                    else:  # score == 1
                        score_1_total += 1
                        if passed:
                            score_1_passed += 1
        
        rate_0 = score_0_passed / score_0_total if score_0_total > 0 else 0
        rate_1 = score_1_passed / score_1_total if score_1_total > 0 else 0
        
        criterion_correlation[c] = {
            "score_0": {"passed": score_0_passed, "total": score_0_total, "rate": rate_0},
            "score_1": {"passed": score_1_passed, "total": score_1_total, "rate": rate_1},
            "delta": rate_1 - rate_0
        }
        
        print(f"\n{c}:")
        print(f"  Score=0: {rate_0*100:5.1f}% pass rate ({score_0_passed}/{score_0_total})")
        print(f"  Score=1: {rate_1*100:5.1f}% pass rate ({score_1_passed}/{score_1_total})")
        print(f"  Delta:   {(rate_1-rate_0)*100:+5.1f}pp {'↑' if rate_1 > rate_0 else '↓' if rate_1 < rate_0 else '='}")

    # Compute overall correlation insight
    print(f"\n{'='*80}")
    print("KEY INSIGHTS")
    print(f"{'='*80}")
    
    # Compare top vs bottom quartile
    if len(quartile_results) >= 2:
        top_q = quartile_results[-1]
        bottom_q = quartile_results[0]
        delta = top_q["pass_rate"] - bottom_q["pass_rate"]
        print(f"• Pass rate difference (Q4 vs Q1): {delta*100:+.1f}pp")
        if delta > 0.1:
            print(f"  → Strong positive correlation: Higher-scoring explanations lead to better pass rates")
        elif delta > 0.05:
            print(f"  → Moderate positive correlation: Higher scores somewhat improve pass rates")
        elif delta > -0.05:
            print(f"  → Weak/No correlation: Explanation scores have minimal effect on pass rates")
        else:
            print(f"  → Negative correlation: Better explanations don't necessarily improve pass rates")

    # Find most predictive criterion
    sorted_criteria = sorted(criterion_correlation.items(), key=lambda x: x[1]["delta"], reverse=True)
    best_criterion = sorted_criteria[0]
    worst_criterion = sorted_criteria[-1]
    
    print(f"\n• Most predictive criterion: {best_criterion[0]}")
    print(f"  → {best_criterion[1]['delta']*100:+.1f}pp improvement when score=1")
    
    print(f"\n• Least predictive criterion: {worst_criterion[0]}")
    print(f"  → {worst_criterion[1]['delta']*100:+.1f}pp change when score=1")

    # Prepare JSON output
    if output_path:
        output_data = {
            "metadata": {
                "runs_analyzed": [os.path.basename(p) for p in file_paths],
                "total_datapoints": n,
                "criteria": criteria
            },
            "level_ranking": level_summaries,
            "quartile_analysis": quartile_results,
            "criterion_correlation": criterion_correlation,
            "insights": {
                "quartile_delta_pp": (quartile_results[-1]["pass_rate"] - quartile_results[0]["pass_rate"]) * 100 if len(quartile_results) >= 2 else None,
                "most_predictive_criterion": best_criterion[0],
                "most_predictive_delta": best_criterion[1]["delta"] * 100,
                "least_predictive_criterion": worst_criterion[0],
                "least_predictive_delta": worst_criterion[1]["delta"] * 100
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze explanation quality metrics across multiple LLM runs.")
    parser.add_argument("--dir", type=str, default="results/runs/python", help="Directory containing result files.")
    parser.add_argument("--pattern", type=str, default="results_run*.json", help="Glob pattern for result files.")
    parser.add_argument("--output", type=str, help="Path to save consistency results as JSON.")
    parser.add_argument("--correlation-output", type=str, help="Path to save correlation results as JSON.")
    
    args = parser.parse_args()
    
    # Run both analyses by default
    evaluate_consistency(args.dir, args.pattern, args.output)
    analyze_score_passrate_correlation(args.dir, args.pattern, args.correlation_output)

