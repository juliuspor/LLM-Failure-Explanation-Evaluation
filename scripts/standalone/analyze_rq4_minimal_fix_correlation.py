import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


CRITERIA = [
    "C1_Readability",
    "C2_Problem_Identification",
    "C3_Explanation_Clarity",
    "C4_Actionability",
    "C5_Contextual_Adequacy",
    "C6_Brevity",
]

MODELS_DEFAULT = ["gpt_5_mini", "deepseek_v3_2", "grok_4_1_fast"]
BATCHES_DEFAULT = ["isolated", "two_way", "three_way"]

CONTEXT_FACTORS = [
    "CODE",
    "ERROR",
    "TEST",
    "DOCSTRING",
    "SLICE_BLOCK",
    "SLICE_BACKWARD",
    "SLICE_FORWARD",
    "SLICE_UNION",
]

SLICE_STRATEGIES = ["SLICE_BLOCK", "SLICE_BACKWARD", "SLICE_FORWARD", "SLICE_UNION"]


def _safe_bool(value: Any) -> bool:
    return bool(value) if value is not None else False


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _two_sided_p_value_from_z(z: float) -> float:
    if not np.isfinite(z):
        return float("nan")
    return 2.0 * (1.0 - _normal_cdf(abs(z)))


def _benjamini_hochberg(p_values: list[float]) -> list[float]:
    m = len(p_values)
    indexed = [(i, p) for i, p in enumerate(p_values) if np.isfinite(p)]
    if not indexed:
        return [float("nan")] * m

    indexed.sort(key=lambda t: t[1])
    q_values = [float("nan")] * m
    prev = 1.0
    for rank in range(len(indexed) - 1, -1, -1):
        i, p = indexed[rank]
        q = p * len(indexed) / (rank + 1)
        prev = min(prev, q)
        q_values[i] = prev

    return q_values


def _total_explanation_score(scores: dict[str, Any]) -> int:
    return int(
        sum(int(scores.get(c, 0)) for c in CRITERIA if isinstance(scores.get(c, 0), (int, float)))
    )


def _has_factor(levels: str, factor: str) -> bool:
    if levels == "BASELINE":
        return True
    return re.search(rf"(^|_){re.escape(factor)}(_|$)", levels) is not None


def _load_results_jsons(json_paths: list[Path]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(json_paths):
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"Expected list in {path}, got {type(data)}")
        entries.extend(data)
    return entries


def _extract_attempt_rows(
    *,
    results_root: Path,
    model: str,
    batch: str,
) -> pd.DataFrame:
    runs_dir = results_root / model / batch / "runs" / "python"
    json_paths = list(runs_dir.glob("results_run*.json"))
    if not json_paths:
        raise FileNotFoundError(f"No results_run*.json files found in {runs_dir}")

    entries = _load_results_jsons(json_paths)
    rows: list[dict[str, Any]] = []
    for entry in entries:
        validation = entry.get("validation") or entry.get("verification") or {}
        passed = _safe_bool(validation.get("passed"))

        scores = entry.get("scores")
        has_scores = isinstance(scores, dict)
        total_score = _total_explanation_score(scores) if has_scores else float("nan")

        comparison = entry.get("comparison") or {}

        expected = comparison.get("expected_changed_lines") or []
        actual = comparison.get("actual_changed_lines") or []
        expected_set = set(int(x) for x in expected if isinstance(x, (int, float, str)) and str(x).isdigit())
        actual_set = set(int(x) for x in actual if isinstance(x, (int, float, str)) and str(x).isdigit())

        row: dict[str, Any] = {
            "Model": model,
            "Batch": batch,
            "Defect": entry.get("defect_id"),
            "Level": entry.get("levels"),
            "Run": entry.get("run_id"),
            "Passed": passed,
            "Has_Scores": has_scores,
            "Total_Score": total_score,
            "Minimal": comparison.get("is_minimal_fix"),
            "Line_Deviation": comparison.get("line_deviation"),
            "Jaccard": comparison.get("jaccard_similarity"),
            "Levenshtein": comparison.get("normalized_levenshtein"),
            "Expected_N": len(expected_set),
            "Actual_N": len(actual_set),
            "Spurious_N": len(actual_set - expected_set),
            "Missed_N": len(expected_set - actual_set),
        }

        levels = str(entry.get("levels") or "")
        for f in CONTEXT_FACTORS:
            row[f"Factor_{f}"] = 1 if _has_factor(levels, f) else 0

        slice_coverage = comparison.get("slice_coverage") or {}
        if not isinstance(slice_coverage, dict):
            slice_coverage = {}
        for strat in SLICE_STRATEGIES:
            cov = slice_coverage.get(strat) or {}
            if not isinstance(cov, dict):
                cov = {}
            row[f"{strat}_Expected_Coverage"] = cov.get("expected_coverage")
            row[f"{strat}_Actual_Coverage"] = cov.get("actual_coverage")
            if "actual_total" in cov and "actual_in_slice" in cov:
                try:
                    row[f"{strat}_OutOfSlice_Actual_N"] = int(cov["actual_total"]) - int(cov["actual_in_slice"])
                except Exception:
                    row[f"{strat}_OutOfSlice_Actual_N"] = float("nan")
            else:
                row[f"{strat}_OutOfSlice_Actual_N"] = float("nan")

        rows.append(row)

    df = pd.DataFrame(rows)

    fix_attempts_path = results_root / model / batch / "reports" / "fix_attempts.csv"
    if fix_attempts_path.exists():
        fix_df = pd.read_csv(fix_attempts_path)
        fix_df = fix_df.rename(
            columns={
                "Defect": "Defect",
                "Level": "Level",
                "Run": "Run",
                "Baseline_Volume": "Baseline_Volume",
                "Baseline_Effort": "Baseline_Effort",
                "Delta_Volume": "Delta_Volume",
                "Delta_Effort": "Delta_Effort",
            }
        )
        df = df.merge(
            fix_df[
                [
                    "Defect",
                    "Level",
                    "Run",
                    "Baseline_Volume",
                    "Baseline_Effort",
                    "Delta_Volume",
                    "Delta_Effort",
                ]
            ],
            how="left",
            on=["Defect", "Level", "Run"],
        )

    return df


def _assign_quartiles(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Quartile"] = pd.NA
    scored = df[df["Has_Scores"] == True]
    for (model, batch), g in scored.groupby(["Model", "Batch"], sort=False):
        g_sorted = g.sort_values("Total_Score", ascending=True, kind="mergesort")
        n = len(g_sorted)
        if n == 0:
            continue
        q = n // 4
        if q == 0:
            df.loc[g_sorted.index, "Quartile"] = "Q4"
            continue
        quartiles = {
            "Q1": g_sorted.index[:q],
            "Q2": g_sorted.index[q : 2 * q],
            "Q3": g_sorted.index[2 * q : 3 * q],
            "Q4": g_sorted.index[3 * q :],
        }
        for label, idx in quartiles.items():
            df.loc[idx, "Quartile"] = label
    return df


def _quartile_summary(df: pd.DataFrame) -> pd.DataFrame:
    scored = df[(df["Has_Scores"] == True) & (df["Quartile"].notna())]
    rows: list[dict[str, Any]] = []
    for (model, batch, quartile), g in scored.groupby(["Model", "Batch", "Quartile"], sort=False):
        total_scored = len(g)
        passed = g[g["Passed"] == True]
        n_passed = len(passed)

        def mean_or_nan(series: pd.Series) -> float:
            if series.dropna().empty:
                return float("nan")
            return float(series.dropna().mean())

        rows.append(
            {
                "Model": model,
                "Batch": batch,
                "Quartile": quartile,
                "N_Scored": total_scored,
                "N_Passed": n_passed,
                "Pass_Rate": (n_passed / total_scored) if total_scored else float("nan"),
                "Minimal_Rate_Passed": mean_or_nan(passed["Minimal"].astype(float)),
                "Avg_Line_Deviation": mean_or_nan(passed["Line_Deviation"]),
                "Avg_Levenshtein": mean_or_nan(passed["Levenshtein"]),
                "Avg_Jaccard": mean_or_nan(passed["Jaccard"]),
                "Avg_Expected_N": mean_or_nan(passed["Expected_N"]),
                "Avg_Actual_N": mean_or_nan(passed["Actual_N"]),
                "Avg_Spurious_N": mean_or_nan(passed["Spurious_N"]),
                "Avg_Missed_N": mean_or_nan(passed["Missed_N"]),
                "Avg_Delta_Volume": mean_or_nan(passed.get("Delta_Volume", pd.Series(dtype=float))),
                "Avg_Delta_Effort": mean_or_nan(passed.get("Delta_Effort", pd.Series(dtype=float))),
                "Avg_Union_Actual_Coverage": mean_or_nan(passed["SLICE_UNION_Actual_Coverage"]),
                "Avg_Union_OutOfSlice_Actual_N": mean_or_nan(passed["SLICE_UNION_OutOfSlice_Actual_N"]),
            }
        )
    return pd.DataFrame(rows).sort_values(["Model", "Batch", "Quartile"])


def _no_explanation_baseline(results_root: Path, model: str) -> dict[str, Any]:
    runs_dir = results_root / model / "no_explanation" / "runs" / "python"
    json_paths = list(runs_dir.glob("results_run*.json"))
    if not json_paths:
        return {"Model": model, "N": 0, "N_Passed": 0}

    entries = _load_results_jsons(json_paths)
    rows: list[dict[str, Any]] = []
    for entry in entries:
        validation = entry.get("validation") or entry.get("verification") or {}
        passed = _safe_bool(validation.get("passed"))
        comp = entry.get("comparison") or {}
        rows.append(
            {
                "Passed": passed,
                "Minimal": comp.get("is_minimal_fix"),
                "Line_Deviation": comp.get("line_deviation"),
                "Jaccard": comp.get("jaccard_similarity"),
                "Levenshtein": comp.get("normalized_levenshtein"),
            }
        )

    df = pd.DataFrame(rows)
    passed = df[df["Passed"] == True]
    out: dict[str, Any] = {"Model": model, "N": len(df), "N_Passed": len(passed)}
    if len(passed) == 0:
        return out

    out.update(
        {
            "Minimal_Rate_Passed": float(passed["Minimal"].astype(float).mean()),
            "Avg_Line_Deviation": float(passed["Line_Deviation"].mean()),
            "Avg_Levenshtein": float(passed["Levenshtein"].mean()),
            "Avg_Jaccard": float(passed["Jaccard"].mean()),
        }
    )
    return out


def _rank_series(values: np.ndarray) -> np.ndarray:
    s = pd.Series(values)
    return s.rank(method="average").to_numpy(dtype=float)


def _spearman(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return float("nan")
    rx = _rank_series(x[mask])
    ry = _rank_series(y[mask])
    return float(np.corrcoef(rx, ry)[0, 1])


def _cluster_robust_covariance(
    *,
    X: np.ndarray,
    residuals: np.ndarray,
    clusters: np.ndarray,
    hessian: np.ndarray,
) -> np.ndarray:
    n, p = X.shape
    unique = pd.unique(pd.Series(clusters))
    g = len(unique)

    h_inv = np.linalg.pinv(hessian)
    meat = np.zeros((p, p), dtype=float)
    for cluster in unique:
        idx = clusters == cluster
        if not np.any(idx):
            continue
        s_g = X[idx].T @ residuals[idx]
        meat += np.outer(s_g, s_g)

    cov = h_inv @ meat @ h_inv
    if g > 1:
        cov *= (g / (g - 1)) * ((n - 1) / max(n - p, 1))
    return cov


def _drop_constant_columns(X: pd.DataFrame) -> pd.DataFrame:
    keep = [c for c in X.columns if X[c].nunique(dropna=False) > 1]
    return X[keep]


def _build_design_matrix(df: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    base = pd.DataFrame(
        {
            "Intercept": 1.0,
            "Total_Score": df["Total_Score"].astype(float),
        }
    )

    if "Baseline_Volume" in df.columns:
        vol = df["Baseline_Volume"].astype(float)
        z = (vol - vol.mean()) / (vol.std(ddof=0) if vol.std(ddof=0) else 1.0)
        base["Baseline_Volume_Z"] = z

    for f in CONTEXT_FACTORS:
        col = f"Factor_{f}"
        if col in df.columns:
            base[col] = df[col].astype(float)

    batch_d = pd.get_dummies(df["Batch"].astype(str), prefix="Batch", drop_first=True, dtype=float)
    run_d = pd.get_dummies(df["Run"].astype(int), prefix="Run", drop_first=True, dtype=float)
    defect_d = pd.get_dummies(df["Defect"].astype(str), prefix="Defect", drop_first=True, dtype=float)

    X_df = pd.concat([base, batch_d, run_d, defect_d], axis=1)
    X_df = _drop_constant_columns(X_df)
    return X_df.to_numpy(dtype=float), X_df.columns.tolist()


def _fit_logit_with_cluster_robust_se(
    *,
    X: np.ndarray,
    y: np.ndarray,
    clusters: np.ndarray,
    ridge: float = 1e-8,
    max_iter: int = 50,
    tol: float = 1e-8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n, p = X.shape
    beta = np.zeros(p, dtype=float)
    for _ in range(max_iter):
        eta = X @ beta
        mu = 1.0 / (1.0 + np.exp(-np.clip(eta, -35, 35)))
        w = mu * (1.0 - mu)
        w = np.clip(w, 1e-9, None)
        z = eta + (y - mu) / w

        XtW = X.T * w
        hessian = XtW @ X + ridge * np.eye(p)
        rhs = XtW @ z
        beta_new = np.linalg.solve(hessian, rhs)
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            break
        beta = beta_new

    eta = X @ beta
    mu = 1.0 / (1.0 + np.exp(-np.clip(eta, -35, 35)))
    w = np.clip(mu * (1.0 - mu), 1e-9, None)
    XtW = X.T * w
    hessian = XtW @ X + ridge * np.eye(p)

    cov = _cluster_robust_covariance(
        X=X,
        residuals=(y - mu),
        clusters=clusters,
        hessian=hessian,
    )
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
    return beta, se, cov


def _fit_ols_with_cluster_robust_se(
    *,
    X: np.ndarray,
    y: np.ndarray,
    clusters: np.ndarray,
    ridge: float = 1e-8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n, p = X.shape
    hessian = X.T @ X + ridge * np.eye(p)
    beta = np.linalg.solve(hessian, X.T @ y)
    resid = y - (X @ beta)
    cov = _cluster_robust_covariance(X=X, residuals=resid, clusters=clusters, hessian=hessian)
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
    return beta, se, cov


def _run_regressions(df: pd.DataFrame) -> pd.DataFrame:
    outcomes: list[tuple[str, str]] = [
        ("minimal_logit", "Minimal"),
        ("lev_ols", "Levenshtein"),
        ("log1p_dev_ols", "Line_Deviation"),
        ("jaccard_distance_ols", "Jaccard"),
        ("log1p_spurious_ols", "Spurious_N"),
        ("log1p_missed_ols", "Missed_N"),
        ("delta_volume_ols", "Delta_Volume"),
        ("delta_effort_ols", "Delta_Effort"),
    ]

    rows: list[dict[str, Any]] = []
    for model, g_model in df.groupby("Model", sort=False):
        g = g_model[(g_model["Passed"] == True) & (g_model["Has_Scores"] == True)].copy()
        if g.empty:
            continue

        clusters = g["Defect"].astype(str).to_numpy()

        for outcome_name, col in outcomes:
            y_raw = g[col] if col in g.columns else pd.Series(dtype=float)
            y = y_raw.astype(float)
            if outcome_name == "minimal_logit":
                mask = y.notna()
                if mask.sum() < 10:
                    continue
                y_bin = y[mask].astype(int).to_numpy(dtype=float)
                X, names = _build_design_matrix(g[mask])
                beta, se, _ = _fit_logit_with_cluster_robust_se(X=X, y=y_bin, clusters=clusters[mask.to_numpy()])
                idx = names.index("Total_Score")
                b = float(beta[idx])
                s = float(se[idx]) if np.isfinite(se[idx]) else float("nan")
                z = b / s if s and np.isfinite(s) else float("nan")
                p = _two_sided_p_value_from_z(z)
                rows.append(
                    {
                        "Model": model,
                        "Outcome": "Minimal (logit)",
                        "N": int(mask.sum()),
                        "Coef_TotalScore": b,
                        "SE_TotalScore": s,
                        "Z": z,
                        "P": p,
                        "OR": math.exp(b) if np.isfinite(b) else float("nan"),
                        "OR_CI_Low": math.exp(b - 1.96 * s) if np.isfinite(b) and np.isfinite(s) else float("nan"),
                        "OR_CI_High": math.exp(b + 1.96 * s) if np.isfinite(b) and np.isfinite(s) else float("nan"),
                    }
                )
                continue

            if outcome_name in {"log1p_dev_ols", "log1p_spurious_ols", "log1p_missed_ols"}:
                y = np.log1p(y)
            if outcome_name == "jaccard_distance_ols":
                y = 1.0 - y

            mask = y.notna() & np.isfinite(y)
            if mask.sum() < 30:
                continue

            X, names = _build_design_matrix(g[mask])
            beta, se, _ = _fit_ols_with_cluster_robust_se(
                X=X, y=y[mask].to_numpy(dtype=float), clusters=clusters[mask.to_numpy()]
            )
            idx = names.index("Total_Score")
            b = float(beta[idx])
            s = float(se[idx]) if np.isfinite(se[idx]) else float("nan")
            z = b / s if s and np.isfinite(s) else float("nan")
            p = _two_sided_p_value_from_z(z)
            rows.append(
                {
                    "Model": model,
                    "Outcome": outcome_name.replace("_ols", "").replace("_", " "),
                    "N": int(mask.sum()),
                    "Coef_TotalScore": b,
                    "SE_TotalScore": s,
                    "Z": z,
                    "P": p,
                }
            )

        # Slice-union adherence subset
        slice_g = g[g["SLICE_UNION_Actual_Coverage"].notna()].copy()
        if not slice_g.empty:
            clusters_s = slice_g["Defect"].astype(str).to_numpy()
            for outcome_name, y_series in [
                ("union_actual_coverage_ols", slice_g["SLICE_UNION_Actual_Coverage"].astype(float)),
                ("log1p_union_out_of_slice_actual_ols", np.log1p(slice_g["SLICE_UNION_OutOfSlice_Actual_N"].astype(float))),
            ]:
                mask = y_series.notna() & np.isfinite(y_series)
                if mask.sum() < 30:
                    continue
                X, names = _build_design_matrix(slice_g[mask])
                beta, se, _ = _fit_ols_with_cluster_robust_se(
                    X=X, y=y_series[mask].to_numpy(dtype=float), clusters=clusters_s[mask.to_numpy()]
                )
                idx = names.index("Total_Score")
                b = float(beta[idx])
                s = float(se[idx]) if np.isfinite(se[idx]) else float("nan")
                z = b / s if s and np.isfinite(s) else float("nan")
                p = _two_sided_p_value_from_z(z)
                rows.append(
                    {
                        "Model": model,
                        "Outcome": outcome_name.replace("_ols", "").replace("_", " "),
                        "N": int(mask.sum()),
                        "Coef_TotalScore": b,
                        "SE_TotalScore": s,
                        "Z": z,
                        "P": p,
                    }
                )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["Q"] = float("nan")
    for model, idxs in out.groupby("Model").groups.items():
        pvals = out.loc[idxs, "P"].astype(float).tolist()
        qvals = _benjamini_hochberg(pvals)
        out.loc[idxs, "Q"] = qvals
    return out.sort_values(["Model", "Outcome"])


def _bootstrap_quartile_delta(
    *,
    df: pd.DataFrame,
    metric_col: str,
    reps: int,
    seed: int,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    scored = df[(df["Has_Scores"] == True) & (df["Passed"] == True) & (df["Quartile"].isin(["Q1", "Q4"]))].copy()
    if scored.empty:
        return pd.DataFrame(columns=["Model", "Batch", "Metric", "Delta", "CI_Low", "CI_High"])

    rows: list[dict[str, Any]] = []
    for (model, batch), g in scored.groupby(["Model", "Batch"], sort=False):
        defects = pd.unique(g["Defect"].astype(str))
        if len(defects) < 2:
            continue

        def delta(data: pd.DataFrame) -> float:
            q1 = data[data["Quartile"] == "Q1"][metric_col].astype(float).dropna()
            q4 = data[data["Quartile"] == "Q4"][metric_col].astype(float).dropna()
            if q1.empty or q4.empty:
                return float("nan")
            return float(q4.mean() - q1.mean())

        point = delta(g)
        samples: list[float] = []
        for _ in range(reps):
            sampled_defects = rng.choice(defects, size=len(defects), replace=True)
            boot = pd.concat([g[g["Defect"].astype(str) == d] for d in sampled_defects], ignore_index=True)
            samples.append(delta(boot))

        arr = np.array([x for x in samples if np.isfinite(x)], dtype=float)
        if arr.size < 50:
            continue

        rows.append(
            {
                "Model": model,
                "Batch": batch,
                "Metric": metric_col,
                "Delta": point,
                "CI_Low": float(np.quantile(arr, 0.025)),
                "CI_High": float(np.quantile(arr, 0.975)),
            }
        )
    return pd.DataFrame(rows)


def _bootstrap_batch_delta_diff(
    *,
    df: pd.DataFrame,
    metric_col: str,
    reps: int,
    seed: int,
    batch_a: str = "two_way",
    batch_b: str = "three_way",
) -> pd.DataFrame:
    """
    Computes a defect-cluster bootstrap CI for the batch difference in quartile deltas:

        DeltaDiff = (Q4 - Q1 in batch_b) - (Q4 - Q1 in batch_a)

    Aggregation is over passing attempts only (consistent with RQ4 similarity metrics),
    while bootstrap resampling is performed at the defect level.
    """
    rng = np.random.default_rng(seed)
    scored = df[
        (df["Has_Scores"] == True)
        & (df["Passed"] == True)
        & (df["Quartile"].isin(["Q1", "Q4"]))
        & (df["Batch"].isin([batch_a, batch_b]))
    ].copy()
    if scored.empty:
        return pd.DataFrame(columns=["Model", "Metric", "DeltaDiff", "CI_Low", "CI_High", "N_Defects"])

    rows: list[dict[str, Any]] = []
    for model, g in scored.groupby("Model", sort=False):
        defects_a = pd.unique(g[g["Batch"] == batch_a]["Defect"].astype(str))
        defects_b = pd.unique(g[g["Batch"] == batch_b]["Defect"].astype(str))
        defects = sorted(set(defects_a).intersection(defects_b))
        if len(defects) < 2:
            continue

        g = g[g["Defect"].astype(str).isin(defects)].copy()

        def delta(data: pd.DataFrame, batch: str) -> float:
            sub = data[data["Batch"] == batch]
            q1 = sub[sub["Quartile"] == "Q1"][metric_col].astype(float).dropna()
            q4 = sub[sub["Quartile"] == "Q4"][metric_col].astype(float).dropna()
            if q1.empty or q4.empty:
                return float("nan")
            return float(q4.mean() - q1.mean())

        def diff(data: pd.DataFrame) -> float:
            d_a = delta(data, batch_a)
            d_b = delta(data, batch_b)
            if not (np.isfinite(d_a) and np.isfinite(d_b)):
                return float("nan")
            return float(d_b - d_a)

        point = diff(g)
        if not np.isfinite(point):
            continue

        samples: list[float] = []
        for _ in range(reps):
            sampled_defects = rng.choice(defects, size=len(defects), replace=True)
            boot = pd.concat([g[g["Defect"].astype(str) == d] for d in sampled_defects], ignore_index=True)
            samples.append(diff(boot))

        arr = np.array([x for x in samples if np.isfinite(x)], dtype=float)
        if arr.size < 50:
            continue

        rows.append(
            {
                "Model": model,
                "Metric": metric_col,
                "DeltaDiff": float(point),
                "CI_Low": float(np.quantile(arr, 0.025)),
                "CI_High": float(np.quantile(arr, 0.975)),
                "N_Defects": int(len(defects)),
            }
        )

    return pd.DataFrame(rows).sort_values(["Model", "Metric"])


def _bootstrap_quartile_rate_ci(
    *,
    df: pd.DataFrame,
    metric_col: str,
    reps: int,
    seed: int,
    models: list[str],
    batches: list[str],
) -> pd.DataFrame:
    """
    Computes defect-cluster bootstrap CIs for the within-(model,batch,quartile) mean of `metric_col`,
    over passing attempts only.

    For minimality, this corresponds to the minimal-fix rate among passing fixes per quartile.
    """
    rng = np.random.default_rng(seed)
    quartiles = ["Q1", "Q2", "Q3", "Q4"]

    scored = df[
        (df["Has_Scores"] == True)
        & (df["Passed"] == True)
        & (df["Quartile"].isin(quartiles))
        & (df[metric_col].notna())
    ].copy()

    rows: list[dict[str, Any]] = []
    for model in models:
        for batch in batches:
            for quartile in quartiles:
                g = scored[
                    (scored["Model"] == model) & (scored["Batch"] == batch) & (scored["Quartile"] == quartile)
                ]
                n = int(len(g))
                defects = pd.unique(g["Defect"].astype(str)) if n else np.array([], dtype=str)
                n_defects = int(len(defects))

                rate = float(g[metric_col].astype(float).mean()) if n else float("nan")
                ci_low = float("nan")
                ci_high = float("nan")

                if n_defects >= 2 and n > 0 and reps > 0:
                    samples: list[float] = []
                    for _ in range(reps):
                        sampled_defects = rng.choice(defects, size=n_defects, replace=True)
                        boot = pd.concat(
                            [g[g["Defect"].astype(str) == d] for d in sampled_defects],
                            ignore_index=True,
                        )
                        samples.append(float(boot[metric_col].astype(float).mean()))

                    arr = np.array([x for x in samples if np.isfinite(x)], dtype=float)
                    if arr.size >= 50:
                        ci_low = float(np.quantile(arr, 0.025))
                        ci_high = float(np.quantile(arr, 0.975))

                rows.append(
                    {
                        "Model": model,
                        "Batch": batch,
                        "Quartile": quartile,
                        "Rate": rate,
                        "CI_Low": ci_low,
                        "CI_High": ci_high,
                        "N_Passed": n,
                        "N_Defects": n_defects,
                        "Bootstrap_Reps": int(reps),
                        "Seed": int(seed),
                    }
                )

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RQ4 analysis: explanation quality vs. minimal-fix / non-spurious-change metrics."
    )
    parser.add_argument(
        "--results-root",
        type=str,
        default=None,
        help="Path to results/ (default: <MasterThesis>/results).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: <MasterThesis>/documentation/reporting/rq4_outputs).",
    )
    parser.add_argument("--models", nargs="+", default=MODELS_DEFAULT)
    parser.add_argument("--batches", nargs="+", default=BATCHES_DEFAULT)
    parser.add_argument("--include-no-explanation", action="store_true")
    parser.add_argument("--bootstrap-reps", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0)

    args = parser.parse_args()

    thesis_root = Path(__file__).resolve().parents[2]
    results_root = Path(args.results_root) if args.results_root else (thesis_root / "results")
    output_dir = (
        Path(args.output_dir)
        if args.output_dir
        else (thesis_root / "documentation" / "reporting" / "rq4_outputs")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    all_dfs: list[pd.DataFrame] = []
    for model in args.models:
        for batch in args.batches:
            all_dfs.append(_extract_attempt_rows(results_root=results_root, model=model, batch=batch))

    attempts = pd.concat(all_dfs, ignore_index=True)
    attempts = _assign_quartiles(attempts)

    attempts.to_csv(output_dir / "rq4_attempts.csv", index=False)

    quartiles = _quartile_summary(attempts)
    quartiles.to_csv(output_dir / "rq4_quartiles_summary.csv", index=False)

    if args.include_no_explanation:
        baselines = pd.DataFrame([_no_explanation_baseline(results_root, m) for m in args.models])
        baselines.to_csv(output_dir / "rq4_no_explanation_baseline.csv", index=False)

    # Spearman correlations within (model,batch) over passing attempts
    corr_rows: list[dict[str, Any]] = []
    corr_metrics = [
        ("Minimal", "Minimal"),
        ("Line_Deviation", "Line_Deviation"),
        ("Levenshtein", "Levenshtein"),
        ("Jaccard", "Jaccard"),
        ("Spurious_N", "Spurious_N"),
        ("Missed_N", "Missed_N"),
        ("Delta_Volume", "Delta_Volume"),
        ("Delta_Effort", "Delta_Effort"),
        ("Union_Actual_Coverage", "SLICE_UNION_Actual_Coverage"),
        ("Union_OutOfSlice_Actual_N", "SLICE_UNION_OutOfSlice_Actual_N"),
    ]
    scored_passed = attempts[(attempts["Has_Scores"] == True) & (attempts["Passed"] == True)].copy()
    for (model, batch), g in scored_passed.groupby(["Model", "Batch"], sort=False):
        x = g["Total_Score"].astype(float).to_numpy()
        for metric_name, col in corr_metrics:
            if col not in g.columns:
                continue
            y = g[col].astype(float).to_numpy()
            corr_rows.append(
                {
                    "Model": model,
                    "Batch": batch,
                    "Metric": metric_name,
                    "SpearmanR": _spearman(x, y),
                    "N": int(np.isfinite(x).sum()),
                }
            )
    pd.DataFrame(corr_rows).to_csv(output_dir / "rq4_spearman_correlations.csv", index=False)

    regs = _run_regressions(attempts)
    regs.to_csv(output_dir / "rq4_regression_summary.csv", index=False)

    deltas = []
    for metric_col in [
        "Minimal",
        "Line_Deviation",
        "Levenshtein",
        "Spurious_N",
        "Delta_Volume",
        "SLICE_UNION_Actual_Coverage",
        "SLICE_UNION_OutOfSlice_Actual_N",
    ]:
        if metric_col not in attempts.columns:
            continue
        deltas.append(
            _bootstrap_quartile_delta(
                df=attempts,
                metric_col=metric_col,
                reps=int(args.bootstrap_reps),
                seed=int(args.seed),
            )
        )
    if deltas:
        pd.concat(deltas, ignore_index=True).to_csv(output_dir / "rq4_quartile_deltas_bootstrap_ci.csv", index=False)

    rates = _bootstrap_quartile_rate_ci(
        df=attempts,
        metric_col="Minimal",
        reps=int(args.bootstrap_reps),
        seed=int(args.seed),
        models=list(args.models),
        batches=list(args.batches),
    )
    rates.to_csv(output_dir / "rq4_minimality_quartile_rates_bootstrap_ci.csv", index=False)

    # Batch-difference bootstrap CIs: (three-way delta) - (two-way delta)
    diff_metrics = ["Line_Deviation", "Levenshtein", "Spurious_N", "Delta_Volume"]
    diffs: list[pd.DataFrame] = []
    for metric_col in diff_metrics:
        if metric_col not in attempts.columns:
            continue
        diffs.append(
            _bootstrap_batch_delta_diff(
                df=attempts,
                metric_col=metric_col,
                reps=int(args.bootstrap_reps),
                seed=int(args.seed),
                batch_a="two_way",
                batch_b="three_way",
            )
        )
    if diffs:
        pd.concat(diffs, ignore_index=True).to_csv(
            output_dir / "rq4_quartile_delta_batch_diff_bootstrap_ci.csv",
            index=False,
        )

    metadata = {
        "models": args.models,
        "batches": args.batches,
        "n_attempts": int(len(attempts)),
        "n_scored": int((attempts["Has_Scores"] == True).sum()),
        "n_passed": int((attempts["Passed"] == True).sum()),
        "bootstrap_reps": int(args.bootstrap_reps),
        "seed": int(args.seed),
    }
    with (output_dir / "rq4_metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Wrote RQ4 analysis outputs to: {output_dir}")


if __name__ == "__main__":
    main()
