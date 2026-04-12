from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


HUMAN_CRITERIA = ("C2", "C3", "C4", "C6")

CRITERION_NAMES: Mapping[str, str] = {
    "C2": "Problem identification",
    "C3": "Explanation clarity",
    "C4": "Actionability",
    "C6": "Brevity",
}

STUDY_DIR = Path(__file__).resolve().parents[1]
MANUSCRIPT_ROOT = Path(__file__).resolve().parents[3]
MANUSCRIPT_TABLES_DIR = MANUSCRIPT_ROOT / "6_results_and_discussion" / "tables"
DEFAULT_TABLES_DIR = (
    MANUSCRIPT_TABLES_DIR
    if MANUSCRIPT_TABLES_DIR.exists()
    else (STUDY_DIR / "analysis" / "rq2_tables")
)

MODEL_ORDER = ("gpt-5-mini", "DeepSeek-V3.2", "Grok-4.1-fast")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _majority_vote(labels: Iterable[int]) -> int | None:
    labels_list = list(labels)
    if not labels_list:
        return None
    ones = sum(1 for x in labels_list if x == 1)
    zeros = len(labels_list) - ones
    if ones == zeros:
        return None
    return 1 if ones > zeros else 0


def _normalize_model_name(raw: str) -> str:
    raw = (raw or "").strip()
    low = raw.lower()
    if low == "gpt-5-mini":
        return "gpt-5-mini"
    if low in {"deepseek/deepseek-v3.2", "deepseek-v3.2"}:
        return "DeepSeek-V3.2"
    if low in {"x-ai/grok-4.1-fast", "grok-4.1-fast"}:
        return "Grok-4.1-fast"
    raise ValueError(f"Unsupported judge model name {raw!r} (expected one of gpt-5-mini, deepseek/deepseek-v3.2, x-ai/grok-4.1-fast)")


def _fmt(x: float | None, *, decimals: int = 3) -> str:
    if x is None:
        return "---"
    return f"{x:.{decimals}f}"


def _makecell(lines: Iterable[str], *, align: str | None = None) -> str:
    parts = [x.strip() for x in lines if x is not None and str(x).strip()]
    if not parts:
        return "---"
    joined = r" \\ ".join(parts)
    if align:
        return r"\makecell[" + align + "]{" + joined + r"}"
    return r"\makecell{" + joined + r"}"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _row_id(r: Mapping[str, Any]) -> tuple[str, str, str]:
    return (str(r["token_hash"]), str(r["defect_id"]), str(r["letter"]))


@dataclass(frozen=True)
class Dataset:
    path: Path
    model: str
    rows: list[dict[str, Any]]


def _validate_dataset(ds: Dataset) -> None:
    rows = ds.rows
    if len(rows) != 288:
        raise ValueError(f"{ds.path.name}: expected 288 rows, got {len(rows)}")

    keys = {str(r.get("explanation_key")) for r in rows}
    if len(keys) != 24:
        raise ValueError(f"{ds.path.name}: expected 24 unique explanation_key values, got {len(keys)}")

    by_key: dict[str, int] = defaultdict(int)
    for r in rows:
        by_key[str(r["explanation_key"])] += 1
        h = r.get("human_labels")
        l = r.get("llm_labels")
        if not isinstance(h, dict) or not isinstance(l, dict):
            raise ValueError(f"{ds.path.name}: row missing human_labels/llm_labels objects")
        for c in HUMAN_CRITERIA:
            if c not in h or c not in l:
                raise ValueError(f"{ds.path.name}: row missing criterion {c} in human_labels/llm_labels")
            hv = int(h[c])
            lv = int(l[c])
            if hv not in (0, 1) or lv not in (0, 1):
                raise ValueError(f"{ds.path.name}: invalid labels for {c}: human={hv!r}, llm={lv!r}")

    bad = {k: n for k, n in by_key.items() if n != 12}
    if bad:
        example = sorted(bad.items(), key=lambda x: (-x[1], x[0]))[0]
        raise ValueError(f"{ds.path.name}: expected 12 rows per explanation_key, e.g. {example[0]} has {example[1]}")

    ids = {_row_id(r) for r in rows}
    if len(ids) != 288:
        raise ValueError(f"{ds.path.name}: expected 288 unique (token_hash, defect_id, letter) row IDs, got {len(ids)}")


def _assert_human_alignment(datasets: list[Dataset]) -> None:
    if not datasets:
        raise ValueError("No datasets provided")

    base = datasets[0]
    base_rows_by_id: dict[tuple[str, str, str], dict[str, Any]] = {_row_id(r): r for r in base.rows}
    base_keys = {str(r["explanation_key"]) for r in base.rows}

    for other in datasets[1:]:
        other_rows_by_id: dict[tuple[str, str, str], dict[str, Any]] = {_row_id(r): r for r in other.rows}
        if set(other_rows_by_id.keys()) != set(base_rows_by_id.keys()):
            raise ValueError(f"{other.path.name}: row IDs differ from {base.path.name} (token_hash/defect_id/letter mismatch)")

        other_keys = {str(r["explanation_key"]) for r in other.rows}
        if other_keys != base_keys:
            raise ValueError(f"{other.path.name}: explanation_key set differs from {base.path.name}")

        for rid, br in base_rows_by_id.items():
            orow = other_rows_by_id[rid]
            if br.get("human_labels") != orow.get("human_labels"):
                raise ValueError(f"{other.path.name}: human_labels mismatch for row {rid}")
            if br.get("human_likert") != orow.get("human_likert"):
                raise ValueError(f"{other.path.name}: human_likert mismatch for row {rid}")
            if int(br.get("run_id")) != int(orow.get("run_id")):
                raise ValueError(f"{other.path.name}: run_id mismatch for row {rid}")
            if str(br.get("explanation_key")) != str(orow.get("explanation_key")):
                raise ValueError(f"{other.path.name}: explanation_key mismatch for row {rid}")


def _mean(values: Iterable[int]) -> float | None:
    vals = list(values)
    if not vals:
        return None
    return sum(vals) / len(vals)


def _macro_avg(values_by_model: dict[str, float | None], *, required_models: Iterable[str]) -> float | None:
    required = list(required_models)
    vals: list[float] = []
    for m in required:
        v = values_by_model.get(m)
        if v is None:
            return None
        vals.append(float(v))
    if not vals:
        return None
    return sum(vals) / len(vals)


def _compute_individual(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for c in HUMAN_CRITERIA:
        acc = _mean(1 if int(r["human_labels"][c]) == int(r["llm_labels"][c]) else 0 for r in rows)
        p_l = _mean(int(r["llm_labels"][c]) for r in rows)
        if acc is None or p_l is None:
            raise ValueError(f"Unexpected empty rows for {c}")
        out[c] = {"acc": float(acc), "p_l": float(p_l)}
    return out


def _compute_human_p(rows: list[dict[str, Any]]) -> dict[str, float]:
    out: dict[str, float] = {}
    for c in HUMAN_CRITERIA:
        p_h = _mean(int(r["human_labels"][c]) for r in rows)
        if p_h is None:
            raise ValueError(f"Unexpected empty rows for {c}")
        out[c] = float(p_h)
    return out


def _group_by_key(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_key[str(r["explanation_key"])].append(r)
    return by_key


def _compute_majority(rows: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    by_key = _group_by_key(rows)
    if len(by_key) != 24:
        raise ValueError(f"Expected 24 stimuli, got {len(by_key)}")

    out: dict[str, dict[str, float | int]] = {}
    for c in HUMAN_CRITERIA:
        used = 0
        correct = 0
        l_ones = 0
        for key, group in by_key.items():
            hmaj = _majority_vote(int(g["human_labels"][c]) for g in group)
            lmaj = _majority_vote(int(g["llm_labels"][c]) for g in group)
            if hmaj is None or lmaj is None:
                continue
            used += 1
            correct += int(hmaj == lmaj)
            l_ones += int(lmaj == 1)
        acc = (correct / used) if used else None
        p_l = (l_ones / used) if used else None
        out[c] = {"acc": acc, "p_l": p_l, "n_used": used, "n_total": len(by_key)}
    return out


def _compute_human_majority(rows: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    by_key = _group_by_key(rows)
    out: dict[str, dict[str, float | int]] = {}
    for c in HUMAN_CRITERIA:
        used = 0
        ones = 0
        for key, group in by_key.items():
            hmaj = _majority_vote(int(g["human_labels"][c]) for g in group)
            if hmaj is None:
                continue
            used += 1
            ones += int(hmaj == 1)
        out[c] = {
            "p_maj_h": (ones / used) if used else None,
            "n_used": used,
            "n_total": len(by_key),
        }
    return out


def _compute_consistency(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    by_key = _group_by_key(rows)
    out: dict[str, dict[str, float]] = {}
    for c in HUMAN_CRITERIA:
        h_unanim = 0
        l_unanim = 0
        h_ext = 0.0
        l_ext = 0.0
        for key, group in by_key.items():
            h_vals = [int(g["human_labels"][c]) for g in group]
            l_vals = [int(g["llm_labels"][c]) for g in group]
            p_h = sum(h_vals) / len(h_vals)
            p_l = sum(l_vals) / len(l_vals)
            h_ext += max(p_h, 1 - p_h)
            l_ext += max(p_l, 1 - p_l)
            if len(set(h_vals)) == 1:
                h_unanim += 1
            if len(set(l_vals)) == 1:
                l_unanim += 1
        n = len(by_key)
        out[c] = {
            "human_unanim": h_unanim / n,
            "llm_unanim": l_unanim / n,
            "human_ext": h_ext / n,
            "llm_ext": l_ext / n,
        }
    return out


def _compute_difficulty(rows: list[dict[str, Any]]) -> dict[str, float]:
    seen: set[tuple[str, str]] = set()
    vals: dict[str, list[int]] = {c: [] for c in HUMAN_CRITERIA}
    for r in rows:
        pid = str(r["token_hash"])
        defect_id = str(r["defect_id"])
        key = (pid, defect_id)
        if key in seen:
            continue
        seen.add(key)
        likert = r.get("human_likert") or {}
        for c in HUMAN_CRITERIA:
            vals[c].append(int(likert[c]))
    out: dict[str, float] = {}
    for c in HUMAN_CRITERIA:
        if not vals[c]:
            raise ValueError(f"Missing Likert values for {c}")
        out[c] = sum(vals[c]) / len(vals[c])
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze RQ2 across multiple LLM-as-a-judge models (agreement vs humans + consistency)."
    )
    parser.add_argument(
        "--datasets",
        type=Path,
        nargs="+",
        default=None,
        help=(
            "One or more human_vs_llm_*.json datasets to compare (e.g., gpt5mini/deepseek/grok). "
            "If omitted, uses the three default filenames under user_study/datasets/."
        ),
    )
    parser.add_argument(
        "--tables-dir",
        type=Path,
        default=DEFAULT_TABLES_DIR,
        help="Directory to write LaTeX tables into (default: 6_results_and_discussion/tables).",
    )
    parser.add_argument(
        "--names",
        nargs="*",
        default=None,
        help="Optional display names aligned with --datasets (otherwise inferred from dataset['judge']['model']).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail unless all three expected models (gpt-5-mini, DeepSeek-V3.2, Grok-4.1-fast) are provided.",
    )
    args = parser.parse_args()

    default_paths = [
        STUDY_DIR / "datasets" / "human_vs_llm_gpt5mini.json",
        STUDY_DIR / "datasets" / "human_vs_llm_deepseek.json",
        STUDY_DIR / "datasets" / "human_vs_llm_grok.json",
    ]
    dataset_paths = [p.resolve() for p in (args.datasets or default_paths)]

    names = args.names or []
    if names and len(names) != len(dataset_paths):
        raise SystemExit("--names must have the same length as --datasets (or be omitted).")

    datasets: list[Dataset] = []
    for idx, path in enumerate(dataset_paths):
        if not path.exists():
            if args.datasets is None:
                # Allow default missing (e.g., DeepSeek still running) unless strict.
                continue
            raise SystemExit(f"Missing dataset file: {path}")
        payload = _load_json(path)
        rows = payload.get("rows")
        if not isinstance(rows, list) or not rows:
            raise SystemExit(f"{path.name}: dataset.rows must be a non-empty list")
        judge = payload.get("judge") or {}
        raw_model = names[idx] if names else str(judge.get("model") or "")
        model = _normalize_model_name(raw_model)
        datasets.append(Dataset(path=path, model=model, rows=rows))

    if not datasets:
        raise SystemExit("No datasets found. Provide --datasets or ensure default human_vs_llm_*.json files exist.")

    for ds in datasets:
        _validate_dataset(ds)

    _assert_human_alignment(datasets)

    by_model: dict[str, Dataset] = {ds.model: ds for ds in datasets}
    if len(by_model) != len(datasets):
        counts = Counter(ds.model for ds in datasets)
        dupes = [m for m, n in counts.items() if n > 1]
        raise SystemExit(f"Duplicate datasets for model(s): {dupes}")

    missing_models = [m for m in MODEL_ORDER if m not in by_model]
    if args.strict and missing_models:
        raise SystemExit(f"Missing required model datasets: {missing_models}")
    if missing_models:
        print(f"Warning: Missing model datasets: {missing_models}. Tables will use '---' placeholders.", flush=True)

    base_rows = datasets[0].rows
    p_h = _compute_human_p(base_rows)
    human_majority = _compute_human_majority(base_rows)
    difficulty = _compute_difficulty(base_rows)

    individual: dict[str, dict[str, dict[str, float]]] = {}
    majority: dict[str, dict[str, dict[str, float | int]]] = {}
    consistency: dict[str, dict[str, dict[str, float]]] = {}
    unique_vecs: dict[str, int] = {}
    for model, ds in by_model.items():
        individual[model] = _compute_individual(ds.rows)
        majority[model] = _compute_majority(ds.rows)
        consistency[model] = _compute_consistency(ds.rows)
        vecs = {tuple(int(r["llm_labels"][c]) for c in HUMAN_CRITERIA) for r in ds.rows}
        unique_vecs[model] = len(vecs)

    # Combined LLM (macro-average across the three models; only defined when all are present).
    combined_individual: dict[str, dict[str, float | None]] = {}
    combined_majority: dict[str, dict[str, float | None]] = {}
    combined_consistency: dict[str, dict[str, float | None]] = {}
    for c in HUMAN_CRITERIA:
        combined_individual[c] = {
            "acc": _macro_avg({m: individual.get(m, {}).get(c, {}).get("acc") for m in MODEL_ORDER}, required_models=MODEL_ORDER),
            "p_l": _macro_avg({m: individual.get(m, {}).get(c, {}).get("p_l") for m in MODEL_ORDER}, required_models=MODEL_ORDER),
        }
        combined_majority[c] = {
            "acc": _macro_avg({m: majority.get(m, {}).get(c, {}).get("acc") for m in MODEL_ORDER}, required_models=MODEL_ORDER),
            "p_l": _macro_avg({m: majority.get(m, {}).get(c, {}).get("p_l") for m in MODEL_ORDER}, required_models=MODEL_ORDER),
        }
        combined_consistency[c] = {
            "unanim": _macro_avg({m: consistency.get(m, {}).get(c, {}).get("llm_unanim") for m in MODEL_ORDER}, required_models=MODEL_ORDER),
            "extrem": _macro_avg({m: consistency.get(m, {}).get(c, {}).get("llm_ext") for m in MODEL_ORDER}, required_models=MODEL_ORDER),
        }

    # --- Write LaTeX tables ---
    tables_dir = args.tables_dir.resolve()
    individual_path = tables_dir / "tab_rq2_llm_vs_human_individual.tex"
    individual_prev_path = tables_dir / "tab_rq2_llm_vs_human_individual_prevalence.tex"
    majority_path = tables_dir / "tab_rq2_llm_vs_human_majority.tex"
    majority_prev_path = tables_dir / "tab_rq2_llm_vs_human_majority_prevalence.tex"
    consistency_path = tables_dir / "tab_rq2_llm_consistency.tex"
    difficulty_path = tables_dir / "tab_rq2_human_difficulty.tex"

    # Table 1: individuals (accuracy)
    lines: list[str] = []
    lines.append(r"\begin{table}[tbp]")
    lines.append(r"    \centering")
    lines.append(
        r"    \caption{Agreement between human labels and three LLM-as-a-judge models for the four LLM-judge criteria (C2--C4 and C6; names shown in the first column; ``Individuals'': $n=288$ labels per model). Each model column reports accuracy (Acc). ``LLM (avg.)'' is the macro-average across \texttt{gpt-5-mini}, \texttt{DeepSeek-V3.2}, and \texttt{Grok-4.1-fast}.}"
    )
    lines.append(r"    \label{tab:rq2:llm_individual}")
    lines.append(r"    \renewcommand{\arraystretch}{1.2}")
    lines.append(r"    \scriptsize")
    lines.append(r"    \setlength{\tabcolsep}{4pt}")
    lines.append(r"    \begin{tabular*}{\linewidth}{@{}@{\extracolsep{\fill}}lcccc@{}}")
    lines.append(r"        \toprule")
    lines.append(
        r"        \textbf{Criterion} & \textbf{\texttt{gpt-5-mini}} & \textbf{\texttt{DeepSeek-V3.2}} & \textbf{\makecell{\texttt{Grok-}\\\texttt{4.1-fast}}} & \textbf{LLM (avg.)} \\"
    )
    lines.append(r"        \midrule")
    for c in HUMAN_CRITERIA:
        crit = _makecell([rf"\textbf{{{c}}}", CRITERION_NAMES[c]], align="l")
        row = [crit]
        for m in MODEL_ORDER:
            if m in individual:
                acc = individual[m][c]["acc"]
                cell = _fmt(acc)
            else:
                cell = "---"
            row.append(cell)
        acc_avg = combined_individual[c]["acc"]
        row.append(_fmt(acc_avg) if acc_avg is not None else "---")
        lines.append("        " + " & ".join(row) + r" \\")
    lines.append(r"        \bottomrule")
    lines.append(r"    \end{tabular*}")
    lines.append(r"\end{table}")
    _write(individual_path, "\n".join(lines))

    # Table 2: individuals (prevalence)
    lines = []
    lines.append(r"\begin{table}[tbp]")
    lines.append(r"    \centering")
    lines.append(
        r"    \caption{Pass prevalence for human labels and three LLM-as-a-judge models for the four LLM-judge criteria (C2--C4 and C6; ``Individuals'': $n=288$ labels per model). The human column reports $P(h{=}1)$; each model column reports $P(l{=}1)$. ``LLM (avg.)'' is the macro-average across \texttt{gpt-5-mini}, \texttt{DeepSeek-V3.2}, and \texttt{Grok-4.1-fast}.}"
    )
    lines.append(r"    \label{tab:rq2:llm_individual_prev}")
    lines.append(r"    \renewcommand{\arraystretch}{1.2}")
    lines.append(r"    \scriptsize")
    lines.append(r"    \setlength{\tabcolsep}{4pt}")
    lines.append(r"    \begin{tabular*}{\linewidth}{@{}@{\extracolsep{\fill}}lccccc@{}}")
    lines.append(r"        \toprule")
    lines.append(
        r"        \textbf{Criterion} & \textbf{$P(h{=}1)$} & \textbf{\texttt{gpt-5-mini}} & \textbf{\texttt{DeepSeek-V3.2}} & \textbf{\makecell{\texttt{Grok-}\\\texttt{4.1-fast}}} & \textbf{LLM (avg.)} \\"
    )
    lines.append(r"        \midrule")
    for c in HUMAN_CRITERIA:
        crit = _makecell([rf"\textbf{{{c}}}", CRITERION_NAMES[c]], align="l")
        row = [crit, _fmt(p_h[c], decimals=3)]
        for m in MODEL_ORDER:
            if m in individual:
                row.append(_fmt(individual[m][c]["p_l"]))
            else:
                row.append("---")
        pl_avg = combined_individual[c]["p_l"]
        row.append(_fmt(pl_avg) if pl_avg is not None else "---")
        lines.append("        " + " & ".join(row) + r" \\")
    lines.append(r"        \bottomrule")
    lines.append(r"    \end{tabular*}")
    lines.append(r"\end{table}")
    _write(individual_prev_path, "\n".join(lines))

    # Table 3: majority (accuracy)
    lines = []
    lines.append(r"\begin{table}[tbp]")
    lines.append(r"    \centering")
    lines.append(
        r"    \caption{Agreement between human and LLM judge majority votes per explanation item ($n=24$ items; $8$ defects $\times$ $3$ runs). Ties are excluded per criterion and model, so the effective $n$ can vary (shown as $n/24$). Each model cell reports majority-vote accuracy (Acc) with the effective $n$ shown as $(n/24)$.}"
    )
    lines.append(r"    \label{tab:rq2:llm_majority}")
    lines.append(r"    \renewcommand{\arraystretch}{1.2}")
    lines.append(r"    \scriptsize")
    lines.append(r"    \setlength{\tabcolsep}{4pt}")
    lines.append(r"    \begin{tabular*}{\linewidth}{@{}@{\extracolsep{\fill}}lcccc@{}}")
    lines.append(r"        \toprule")
    lines.append(
        r"        \textbf{Criterion} & \textbf{\texttt{gpt-5-mini}} & \textbf{\texttt{DeepSeek-V3.2}} & \textbf{\makecell{\texttt{Grok-}\\\texttt{4.1-fast}}} & \textbf{LLM (avg.)} \\"
    )
    lines.append(r"        \midrule")
    for c in HUMAN_CRITERIA:
        crit = _makecell([rf"\textbf{{{c}}}", CRITERION_NAMES[c]], align="l")
        row = [crit]
        for m in MODEL_ORDER:
            if m in majority:
                acc = majority[m][c]["acc"]
                n_used = int(majority[m][c]["n_used"])
                cell = f"{_fmt(acc)} ({n_used}/24)"
            else:
                cell = "---"
            row.append(cell)

        acc_avg = combined_majority[c]["acc"]
        row.append(_fmt(acc_avg) if acc_avg is not None else "---")
        lines.append("        " + " & ".join(row) + r" \\")
    lines.append(r"        \bottomrule")
    lines.append(r"    \end{tabular*}")
    lines.append(r"\end{table}")
    _write(majority_path, "\n".join(lines))

    # Table 4: majority (prevalence)
    lines = []
    lines.append(r"\begin{table}[tbp]")
    lines.append(r"    \centering")
    lines.append(
        r"    \caption{Majority-vote pass prevalence per explanation item ($n=24$ items; $8$ defects $\times$ $3$ runs). The human column reports $P(maj_h{=}1)$; each model column reports $P(maj_l{=}1)$. Ties are excluded per criterion and model, so the effective $n$ can vary (shown as $n/24$). ``LLM (avg.)'' is the macro-average across \texttt{gpt-5-mini}, \texttt{DeepSeek-V3.2}, and \texttt{Grok-4.1-fast}.}"
    )
    lines.append(r"    \label{tab:rq2:llm_majority_prev}")
    lines.append(r"    \renewcommand{\arraystretch}{1.2}")
    lines.append(r"    \scriptsize")
    lines.append(r"    \setlength{\tabcolsep}{4pt}")
    lines.append(r"    \begin{tabular*}{\linewidth}{@{}@{\extracolsep{\fill}}lccccc@{}}")
    lines.append(r"        \toprule")
    lines.append(
        r"        \textbf{Criterion} & \textbf{Human maj.} & \textbf{\texttt{gpt-5-mini}} & \textbf{\texttt{DeepSeek-V3.2}} & \textbf{\makecell{\texttt{Grok-}\\\texttt{4.1-fast}}} & \textbf{LLM (avg.)} \\"
    )
    lines.append(r"        \midrule")
    for c in HUMAN_CRITERIA:
        ph = human_majority[c]["p_maj_h"]
        nh = int(human_majority[c]["n_used"])
        crit = _makecell([rf"\textbf{{{c}}}", CRITERION_NAMES[c]], align="l")
        row = [crit, f"{_fmt(ph, decimals=3)} ({nh}/24)" if ph is not None else "---"]
        for m in MODEL_ORDER:
            if m in majority:
                pl = majority[m][c]["p_l"]
                n_used = int(majority[m][c]["n_used"])
                row.append(f"{_fmt(pl)} ({n_used}/24)")
            else:
                row.append("---")
        pl_avg = combined_majority[c]["p_l"]
        row.append(_fmt(pl_avg) if pl_avg is not None else "---")
        lines.append("        " + " & ".join(row) + r" \\")
    lines.append(r"        \bottomrule")
    lines.append(r"    \end{tabular*}")
    lines.append(r"\end{table}")
    _write(majority_prev_path, "\n".join(lines))

    # Table 5: consistency
    lines = []
    lines.append(r"\begin{table}[tbp]")
    lines.append(r"    \centering")
    lines.append(
        r"    \caption{Consistency of ratings across multiple judgments for the same explanation item ($n=24$ items; each item has 12 human votes and 12 repeated judge calls per model). ``Unanim.'' is the fraction of items with unanimous votes; ``Extrem.'' is $\mathrm{mean}(\max(p,1-p))$ over items, where $p$ is the pass vote share.}"
    )
    lines.append(r"    \label{tab:rq2:llm_consistency}")
    lines.append(r"    \renewcommand{\arraystretch}{1.2}")
    lines.append(r"    \scriptsize")
    lines.append(r"    \setlength{\tabcolsep}{4pt}")
    lines.append(r"    \begin{tabular*}{\linewidth}{@{}@{\extracolsep{\fill}}lccccc@{}}")
    lines.append(r"        \toprule")
    lines.append(
        r"        \textbf{Criterion} & \textbf{Human} & \textbf{\texttt{gpt-5-mini}} & \textbf{\texttt{DeepSeek-V3.2}} & \textbf{\makecell{\texttt{Grok-}\\\texttt{4.1-fast}}} & \textbf{LLM (avg.)} \\"
    )
    lines.append(r"        \midrule")
    human_consistency = _compute_consistency(base_rows)
    for c in HUMAN_CRITERIA:
        h = human_consistency[c]
        row = [
            _makecell([rf"\textbf{{{c}}}", CRITERION_NAMES[c]], align="l"),
            _makecell([rf"Unanim {_fmt(h['human_unanim'])}", rf"Extrem {_fmt(h['human_ext'])}"]),
        ]
        for m in MODEL_ORDER:
            if m in consistency:
                d = consistency[m][c]
                row.append(_makecell([rf"Unanim {_fmt(d['llm_unanim'])}", rf"Extrem {_fmt(d['llm_ext'])}"]))
            else:
                row.append("---")
        u_avg = combined_consistency[c]["unanim"]
        e_avg = combined_consistency[c]["extrem"]
        row.append(_makecell([rf"Unanim {_fmt(u_avg)}", rf"Extrem {_fmt(e_avg)}"]) if u_avg is not None else "---")
        lines.append("        " + " & ".join(row) + r" \\")
    lines.append(r"        \bottomrule")
    lines.append(r"    \end{tabular*}")
    lines.append(r"\end{table}")
    _write(consistency_path, "\n".join(lines))

    # Table 6: difficulty (no CI)
    lines = []
    lines.append(r"\begin{table}[tbp]")
    lines.append(r"    \centering")
    lines.append(
        r"    \caption{Per-criterion difficulty ratings from the user study (5-point Likert; 1 = easiest, 5 = hardest). Ratings are per participant and defect ($n=96$ participant$\times$defect cases). Values report the mean.}"
    )
    lines.append(r"    \label{tab:rq2:difficulty}")
    lines.append(r"    \renewcommand{\arraystretch}{1.2}")
    lines.append(r"    \small")
    lines.append(r"    \setlength{\tabcolsep}{4pt}")
    lines.append(r"    \begin{tabular*}{\linewidth}{@{}@{\extracolsep{\fill}}lc@{}}")
    lines.append(r"        \toprule")
    lines.append(r"        \textbf{Criterion} & \textbf{Mean difficulty} \\")
    lines.append(r"        \midrule")
    for c in HUMAN_CRITERIA:
        crit = _makecell([rf"\textbf{{{c}}}", CRITERION_NAMES[c]], align="l")
        lines.append(rf"        {crit} & {_fmt(difficulty[c], decimals=2)} \\")
    lines.append(r"        \bottomrule")
    lines.append(r"    \end{tabular*}")
    lines.append(r"\end{table}")
    _write(difficulty_path, "\n".join(lines))

    # Print small diagnostics for the write-up.
    for m in MODEL_ORDER:
        if m in unique_vecs:
            print(f"{m}: unique judge label vectors (C2/C3/C4/C6) = {unique_vecs[m]}", flush=True)

    print(f"Wrote tables to: {tables_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
