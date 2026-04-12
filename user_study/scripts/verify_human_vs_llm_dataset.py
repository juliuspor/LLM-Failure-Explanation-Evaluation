from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


HUMAN_CRITERIA = ("C2", "C3", "C4", "C6")
DEFAULT_DATASET_NAME = "human_vs_llm_gpt5mini.json"


def _default_dataset_path(study_dir: Path) -> Path:
    return study_dir / "datasets" / DEFAULT_DATASET_NAME


def _legacy_dataset_path(study_dir: Path) -> Path:
    return study_dir / DEFAULT_DATASET_NAME


def _resolve_dataset_path(study_dir: Path, explicit_path: Path | None) -> Path:
    if explicit_path is not None:
        return explicit_path.resolve()
    canonical = _default_dataset_path(study_dir)
    if canonical.exists():
        return canonical.resolve()
    legacy = _legacy_dataset_path(study_dir)
    if legacy.exists():
        return legacy.resolve()
    return canonical.resolve()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _compute_binary_metrics(pairs: Iterable[tuple[int, int]]) -> dict[str, Any]:
    pairs_list = list(pairs)
    n = len(pairs_list)
    if n == 0:
        return {"n": 0, "accuracy": None, "tp": 0, "fp": 0, "tn": 0, "fn": 0, "cohen_kappa": None}

    tp = fp = tn = fn = 0
    for y_true, y_pred in pairs_list:
        if y_true == 1 and y_pred == 1:
            tp += 1
        elif y_true == 0 and y_pred == 1:
            fp += 1
        elif y_true == 0 and y_pred == 0:
            tn += 1
        elif y_true == 1 and y_pred == 0:
            fn += 1
        else:
            raise ValueError(f"Invalid pair ({y_true!r}, {y_pred!r}); expected 0/1")

    accuracy = (tp + tn) / n
    p_true_pos = (tp + fn) / n
    p_true_neg = 1.0 - p_true_pos
    p_pred_pos = (tp + fp) / n
    p_pred_neg = 1.0 - p_pred_pos
    pe = (p_true_pos * p_pred_pos) + (p_true_neg * p_pred_neg)
    if pe >= 1.0:
        kappa = 0.0
    else:
        kappa = (accuracy - pe) / (1.0 - pe)

    return {
        "n": n,
        "accuracy": round(accuracy, 6),
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "cohen_kappa": round(kappa, 6),
    }


def _majority_vote(labels: list[int]) -> int | None:
    if not labels:
        return None
    ones = sum(labels)
    zeros = len(labels) - ones
    if ones == zeros:
        return None
    return 1 if ones > zeros else 0


def _assert_close(a: float | None, b: float | None, *, name: str) -> None:
    if a is None and b is None:
        return
    if a is None or b is None:
        raise AssertionError(f"{name}: {a!r} != {b!r}")
    if abs(a - b) > 1e-6:
        raise AssertionError(f"{name}: {a!r} != {b!r}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a human_vs_llm_gpt5mini.json dataset against participant exports and explanation stimuli."
    )
    parser.add_argument(
        "--study-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to the user_study/ directory (default: script-relative).",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=None,
        help="Path to the dataset JSON (default: <study-dir>/datasets/human_vs_llm_gpt5mini.json).",
    )
    parser.add_argument(
        "--participants-glob",
        default="results/*.json",
        help="Glob (relative to study-dir) for participant state JSONs (default: results/*.json).",
    )
    parser.add_argument(
        "--ground-truth",
        type=Path,
        default=None,
        help="Path to ground_truth.json (default: <study-dir>/ground_truth.json).",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Expected number of runs per defect (default: 3).",
    )
    args = parser.parse_args()

    study_dir = args.study_dir.resolve()
    dataset_path = _resolve_dataset_path(study_dir, args.dataset)
    ground_truth_path = (args.ground_truth or (study_dir / "ground_truth.json")).resolve()

    if args.runs <= 0:
        raise SystemExit("--runs must be a positive integer")
    if not dataset_path.exists():
        raise SystemExit(f"Missing dataset file: {dataset_path}")
    if not ground_truth_path.exists():
        raise SystemExit(f"Missing ground truth file: {ground_truth_path}")

    participant_paths = sorted(study_dir.glob(args.participants_glob))
    if not participant_paths:
        raise SystemExit(f"No participant files found for glob {args.participants_glob!r} in {study_dir}")

    dataset = _load_json(dataset_path)
    schema_version = int(dataset.get("schema_version") or 1)
    if schema_version not in (1, 2):
        raise AssertionError(f"Unsupported dataset schema_version: {schema_version}")
    rows = dataset.get("rows")
    llm_explanations = dataset.get("llm_explanations")
    summary = dataset.get("summary")

    if not isinstance(rows, list):
        raise AssertionError("dataset.rows must be a list")
    if not isinstance(llm_explanations, dict):
        raise AssertionError("dataset.llm_explanations must be an object")
    if not isinstance(summary, dict):
        raise AssertionError("dataset.summary must be an object")

    if dataset.get("n_rows") != len(rows):
        raise AssertionError(f"dataset.n_rows={dataset.get('n_rows')} but len(rows)={len(rows)}")
    if schema_version >= 2:
        n_llm_calls = dataset.get("n_llm_calls")
        if not isinstance(n_llm_calls, int) or n_llm_calls <= 0:
            raise AssertionError(f"dataset.n_llm_calls must be a positive int, got {n_llm_calls!r}")
        if n_llm_calls != len(rows):
            raise AssertionError(f"dataset.n_llm_calls={n_llm_calls} but len(rows)={len(rows)}")

    gt_items = _load_json(ground_truth_path)
    defect_ids = [str(x["id"]) for x in gt_items]
    if dataset.get("n_defects") != len(defect_ids):
        raise AssertionError(f"dataset.n_defects={dataset.get('n_defects')} but ground_truth has {len(defect_ids)}")

    # Load participant state JSONs and index by token_hash.
    participants_by_token: dict[str, Any] = {}
    for p in participant_paths:
        d = _load_json(p)
        token = d.get("participant", {}).get("token_hash")
        if not token:
            raise AssertionError(f"Missing participant.token_hash in {p}")
        if token in participants_by_token:
            raise AssertionError(f"Duplicate token_hash {token} in participant files")
        participants_by_token[str(token)] = d

    if dataset.get("n_participants") != len(participants_by_token):
        raise AssertionError(
            f"dataset.n_participants={dataset.get('n_participants')} but found {len(participants_by_token)} participant files"
        )

    # Check llm_explanations coverage and file hashes.
    expected_llm_keys = {f"{defect_id}#run{run_id}" for defect_id in defect_ids for run_id in range(1, args.runs + 1)}
    missing_llm = sorted(expected_llm_keys - set(llm_explanations.keys()))
    extra_llm = sorted(set(llm_explanations.keys()) - expected_llm_keys)
    if missing_llm:
        raise AssertionError(f"Missing llm_explanations keys: {missing_llm[:5]}{'...' if len(missing_llm)>5 else ''}")
    if extra_llm:
        raise AssertionError(f"Unexpected llm_explanations keys: {extra_llm[:5]}{'...' if len(extra_llm)>5 else ''}")

    for key in sorted(expected_llm_keys):
        item = llm_explanations[key]
        expl_file = item.get("explanation_file")
        expl_sha = item.get("explanation_sha256")
        if not isinstance(expl_file, str) or not expl_file:
            raise AssertionError(f"{key}: missing explanation_file")
        if not isinstance(expl_sha, str) or not expl_sha:
            raise AssertionError(f"{key}: missing explanation_sha256")
        path = Path(expl_file)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        if not path.exists():
            raise AssertionError(f"{key}: explanation_file does not exist: {path}")
        text = path.read_text(encoding="utf-8")
        if _sha256_text(text) != expl_sha:
            raise AssertionError(f"{key}: explanation_sha256 mismatch for {path}")

        if schema_version == 1:
            scores = item.get("scores")
            if not isinstance(scores, dict):
                raise AssertionError(f"{key}: scores must be an object")
            for required in (
                "C1_Readability",
                "C2_Problem_Identification",
                "C3_Explanation_Clarity",
                "C4_Actionability",
                "C5_Contextual_Adequacy",
                "C6_Brevity",
            ):
                v = scores.get(required)
                if v not in (0, 1):
                    raise AssertionError(f"{key}: invalid score {required}={v!r}")

    # Verify every row matches participant mapping + stored llm_explanations.
    bad = 0
    for i, r in enumerate(rows):
        token = r.get("token_hash")
        state = participants_by_token.get(token)
        if state is None:
            bad += 1
            continue

        defect_id = r.get("defect_id")
        letter = r.get("letter")
        run_id = r.get("run_id")
        explanation_key = r.get("explanation_key")

        if explanation_key != f"{defect_id}#run{run_id}":
            raise AssertionError(f"Row {i}: explanation_key mismatch: {explanation_key!r}")

        run_expected = state["assignment"]["explanation_map"][defect_id][letter]
        if run_id != run_expected:
            raise AssertionError(
                f"Row {i}: run_id mismatch for token {token}: {defect_id} {letter} got {run_id}, expected {run_expected}"
            )

        if r.get("participant_id") != state["participant"].get("participant_id"):
            raise AssertionError(f"Row {i}: participant_id mismatch for token {token}")

        if r.get("human_labels") != state["responses"]["initial_labels"][defect_id][letter]:
            raise AssertionError(f"Row {i}: human_labels mismatch for token {token} {defect_id} {letter}")

        if r.get("human_likert") != state["responses"]["likert"][defect_id]:
            raise AssertionError(f"Row {i}: human_likert mismatch for token {token} {defect_id}")

        if schema_version == 1:
            expl_scores = llm_explanations[explanation_key]["scores"]
            llm_expected = {
                "C2": expl_scores["C2_Problem_Identification"],
                "C3": expl_scores["C3_Explanation_Clarity"],
                "C4": expl_scores["C4_Actionability"],
                "C6": expl_scores["C6_Brevity"],
            }
            if r.get("llm_labels") != llm_expected:
                raise AssertionError(f"Row {i}: llm_labels mismatch for {explanation_key}")
        else:
            llm_labels = r.get("llm_labels")
            if not isinstance(llm_labels, dict):
                raise AssertionError(f"Row {i}: llm_labels must be an object")
            for c in HUMAN_CRITERIA:
                v = llm_labels.get(c)
                if v not in (0, 1):
                    raise AssertionError(f"Row {i}: invalid llm_labels.{c}={v!r}, expected 0/1")

        match_expected = {c: (r["human_labels"][c] == r["llm_labels"][c]) for c in HUMAN_CRITERIA}
        if r.get("match") != match_expected:
            raise AssertionError(f"Row {i}: match mismatch for {explanation_key}")

    if bad:
        raise AssertionError(f"{bad} rows reference unknown token_hash values")

    # Count invariants.
    n_participants = len(participants_by_token)
    expected_rows = n_participants * len(defect_ids) * 3
    if len(rows) != expected_rows:
        raise AssertionError(f"Expected {expected_rows} rows, got {len(rows)}")

    # Each participant×defect should have A/B/C once.
    per_pd = defaultdict(list)
    for r in rows:
        per_pd[(r["token_hash"], r["defect_id"])].append(r)
    for (token, defect), group in per_pd.items():
        letters = sorted(g["letter"] for g in group)
        if letters != ["A", "B", "C"]:
            raise AssertionError(f"{token[:8]} {defect}: expected letters A/B/C once, got {letters}")
        runs = sorted(g["run_id"] for g in group)
        if runs != list(range(1, args.runs + 1)):
            raise AssertionError(f"{token[:8]} {defect}: expected runs 1..{args.runs}, got {runs}")

    # Each explanation_key should appear once per participant (so count == n_participants).
    key_counts = Counter(r["explanation_key"] for r in rows)
    for key in sorted(expected_llm_keys):
        if key_counts.get(key) != n_participants:
            raise AssertionError(f"{key}: expected count {n_participants}, got {key_counts.get(key)}")

    # Verify summaries by recomputation.
    agreement_vs_individuals = summary.get("agreement_vs_individuals")
    agreement_vs_majority = summary.get("agreement_vs_majority")
    if not isinstance(agreement_vs_individuals, dict) or not isinstance(agreement_vs_majority, dict):
        raise AssertionError("summary agreement fields missing/invalid")

    for c in HUMAN_CRITERIA:
        pairs = [(int(r["human_labels"][c]), int(r["llm_labels"][c])) for r in rows]
        expected = _compute_binary_metrics(pairs)
        got = agreement_vs_individuals.get(c)
        if not isinstance(got, dict):
            raise AssertionError(f"summary.agreement_vs_individuals.{c} missing")
        if got.get("tp") != expected["tp"] or got.get("fp") != expected["fp"] or got.get("tn") != expected["tn"] or got.get("fn") != expected["fn"]:
            raise AssertionError(f"summary.agreement_vs_individuals.{c} confusion matrix mismatch")
        _assert_close(float(got.get("accuracy")), float(expected["accuracy"]), name=f"agreement_vs_individuals.{c}.accuracy")
        _assert_close(float(got.get("cohen_kappa")), float(expected["cohen_kappa"]), name=f"agreement_vs_individuals.{c}.cohen_kappa")

    # Majority vote summaries.
    by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_key[r["explanation_key"]].append(r)
    for c in HUMAN_CRITERIA:
        ties = 0
        majority_pairs: list[tuple[int, int]] = []
        for key, group in sorted(by_key.items()):
            human_votes = [int(g["human_labels"][c]) for g in group]
            human_maj = _majority_vote(human_votes)
            if schema_version == 1:
                if human_maj is None:
                    ties += 1
                    continue
                llm_vote = int(group[0]["llm_labels"][c])
                majority_pairs.append((human_maj, llm_vote))
            else:
                llm_votes = [int(g["llm_labels"][c]) for g in group]
                llm_maj = _majority_vote(llm_votes)
                if human_maj is None or llm_maj is None:
                    ties += 1
                    continue
                majority_pairs.append((human_maj, llm_maj))
        expected = _compute_binary_metrics(majority_pairs)
        got = agreement_vs_majority.get(c)
        if not isinstance(got, dict):
            raise AssertionError(f"summary.agreement_vs_majority.{c} missing")
        if got.get("n_items_total") != len(by_key):
            raise AssertionError(f"summary.agreement_vs_majority.{c}.n_items_total mismatch")
        if got.get("n_ties") != ties:
            raise AssertionError(f"summary.agreement_vs_majority.{c}.n_ties mismatch")
        if got.get("tp") != expected["tp"] or got.get("fp") != expected["fp"] or got.get("tn") != expected["tn"] or got.get("fn") != expected["fn"]:
            raise AssertionError(f"summary.agreement_vs_majority.{c} confusion matrix mismatch")
        _assert_close(float(got.get("accuracy")), float(expected["accuracy"]), name=f"agreement_vs_majority.{c}.accuracy")
        _assert_close(float(got.get("cohen_kappa")), float(expected["cohen_kappa"]), name=f"agreement_vs_majority.{c}.cohen_kappa")

    print(f"OK: {dataset_path.name} verified against {len(participant_paths)} participant files and {len(expected_llm_keys)} explanations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
