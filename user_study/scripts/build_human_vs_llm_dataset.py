from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Literal


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts._common import load_env  # noqa: E402
from src.evaluation import ExplanationEvaluator  # noqa: E402
from src.llm import LLMService  # noqa: E402


Backend = Literal["openai", "openrouter"]

HUMAN_CRITERIA = ("C2", "C3", "C4", "C6")
LLM_SCORE_MAP = {
    "C2": "C2_Problem_Identification",
    "C3": "C3_Explanation_Clarity",
    "C4": "C4_Actionability",
    "C6": "C6_Brevity",
}
DEFAULT_DATASET_NAME = "human_vs_llm_gpt5mini.json"


def _default_dataset_path(study_dir: Path) -> Path:
    return study_dir / "datasets" / DEFAULT_DATASET_NAME


def _stimulus_path(study_dir: Path, defect_id: str, run_id: int) -> Path:
    filename = f"{defect_id}_BASELINE_run{run_id}.txt"
    canonical = study_dir / "stimuli" / filename
    legacy = study_dir / filename
    if canonical.exists():
        return canonical
    if legacy.exists():
        return legacy
    return canonical


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ParticipantState:
    path: Path
    participant_id: str
    token_hash: str
    explanation_map: dict[str, dict[str, int]]
    initial_labels: dict[str, dict[str, dict[str, int]]]
    likert: dict[str, dict[str, int]]


def _parse_participant_state(path: Path) -> ParticipantState:
    d = _load_json(path)

    participant = d.get("participant") or {}
    participant_id = participant.get("participant_id")
    token_hash = participant.get("token_hash")
    if not participant_id or not token_hash:
        raise ValueError(f"Missing participant_id/token_hash in {path}")

    assignment = d.get("assignment") or {}
    explanation_map = assignment.get("explanation_map")
    if not isinstance(explanation_map, dict):
        raise ValueError(f"Missing assignment.explanation_map in {path}")

    responses = d.get("responses") or {}
    initial_labels = responses.get("initial_labels")
    if not isinstance(initial_labels, dict):
        raise ValueError(f"Missing responses.initial_labels in {path}")

    likert = responses.get("likert")
    if not isinstance(likert, dict):
        raise ValueError(f"Missing responses.likert in {path}")

    return ParticipantState(
        path=path,
        participant_id=str(participant_id),
        token_hash=str(token_hash),
        explanation_map=explanation_map,
        initial_labels=initial_labels,
        likert=likert,
    )


def _validate_participant_completeness(
    participants: list[ParticipantState], defect_ids: list[str], *, runs: int
) -> None:
    expected_letters = {"A", "B", "C"}
    for p in participants:
        missing_defects = [d for d in defect_ids if d not in p.initial_labels]
        if missing_defects:
            raise ValueError(
                f"{p.participant_id} ({p.path.name}) missing initial_labels for: {missing_defects}"
            )
        missing_map_defects = [d for d in defect_ids if d not in p.explanation_map]
        if missing_map_defects:
            raise ValueError(
                f"{p.participant_id} ({p.path.name}) missing explanation_map for: {missing_map_defects}"
            )

        for defect_id in defect_ids:
            letters = set(p.initial_labels[defect_id].keys())
            if letters != expected_letters:
                raise ValueError(
                    f"{p.participant_id} ({p.path.name}) defect {defect_id} has letters {sorted(letters)}, "
                    f"expected {sorted(expected_letters)}"
                )
            map_letters = set(p.explanation_map[defect_id].keys())
            if map_letters != expected_letters:
                raise ValueError(
                    f"{p.participant_id} ({p.path.name}) defect {defect_id} explanation_map has letters "
                    f"{sorted(map_letters)}, expected {sorted(expected_letters)}"
                )

            for letter in ("A", "B", "C"):
                labels = p.initial_labels[defect_id][letter]
                for c in HUMAN_CRITERIA:
                    v = labels.get(c)
                    if v not in (0, 1):
                        raise ValueError(
                            f"{p.participant_id} ({p.path.name}) defect {defect_id} letter {letter} "
                            f"has invalid {c}={v!r}, expected 0/1"
                        )
                run_id = p.explanation_map[defect_id][letter]
                if not isinstance(run_id, int) or run_id <= 0:
                    raise ValueError(
                        f"{p.participant_id} ({p.path.name}) defect {defect_id} letter {letter} "
                        f"has invalid run_id {run_id!r}"
                    )
                if run_id > runs:
                    raise ValueError(
                        f"{p.participant_id} ({p.path.name}) defect {defect_id} letter {letter} "
                        f"maps to run_id {run_id}, but --runs is {runs}"
                    )

            lik = p.likert.get(defect_id)
            if not isinstance(lik, dict):
                raise ValueError(
                    f"{p.participant_id} ({p.path.name}) missing likert for defect {defect_id}"
                )
            for c in HUMAN_CRITERIA:
                v = lik.get(c)
                if not isinstance(v, int) or not (1 <= v <= 5):
                    raise ValueError(
                        f"{p.participant_id} ({p.path.name}) defect {defect_id} has invalid likert {c}={v!r}, "
                        "expected integer 1..5"
                    )


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Join human user-study labels with GPT-5-mini LLM-as-a-judge labels for the same explanations."
    )
    parser.add_argument(
        "--study-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to the user_study/ directory (default: script-relative).",
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
        help="Number of explanation runs per defect to evaluate (default: 3).",
    )
    parser.add_argument(
        "--backend",
        choices=("openai", "openrouter"),
        default="openai",
        help="LLM backend for judging (default: openai).",
    )
    parser.add_argument(
        "--model",
        default="gpt-5-mini",
        help="LLM model for judging (default: gpt-5-mini).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output JSON path (default: <study-dir>/datasets/human_vs_llm_gpt5mini.json).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print planned work without making LLM calls or writing output.",
    )
    args = parser.parse_args()

    load_env(override=False)

    study_dir: Path = args.study_dir.resolve()
    ground_truth_path: Path = (args.ground_truth or (study_dir / "ground_truth.json")).resolve()
    out_path: Path = (args.out or _default_dataset_path(study_dir)).resolve()

    if not ground_truth_path.exists():
        raise SystemExit(f"Missing ground truth file: {ground_truth_path}")

    participant_paths = sorted(study_dir.glob(args.participants_glob))
    if not participant_paths:
        raise SystemExit(f"No participant files found for glob {args.participants_glob!r} in {study_dir}")

    participants = [_parse_participant_state(p) for p in participant_paths]
    participants.sort(key=lambda p: (p.participant_id.lower(), p.token_hash))

    gt_items = _load_json(ground_truth_path)
    if not isinstance(gt_items, list):
        raise SystemExit(f"Expected list in {ground_truth_path}, got {type(gt_items).__name__}")

    defect_ids: list[str] = []
    ground_truth_map: dict[str, str] = {}
    for item in gt_items:
        defect_id = item.get("id")
        gt = item.get("ground_truth")
        if not defect_id or not isinstance(defect_id, str):
            raise SystemExit(f"Invalid defect id in {ground_truth_path}: {item!r}")
        if not isinstance(gt, str):
            raise SystemExit(f"Invalid ground_truth for defect {defect_id} in {ground_truth_path}")
        defect_ids.append(defect_id)
        ground_truth_map[defect_id] = gt

    if args.runs <= 0:
        raise SystemExit("--runs must be a positive integer")

    _validate_participant_completeness(participants, defect_ids, runs=args.runs)

    # Validate explanation files exist/readable up-front.
    explanation_paths: dict[str, Path] = {}
    explanation_texts: dict[str, str] = {}
    for defect_id in defect_ids:
        for run_id in range(1, args.runs + 1):
            key = f"{defect_id}#run{run_id}"
            p = _stimulus_path(study_dir, defect_id, run_id)
            if not p.exists():
                raise SystemExit(f"Missing explanation file: {p}")
            explanation_texts[key] = p.read_text(encoding="utf-8")
            explanation_paths[key] = p

    n_rows_expected = len(participants) * len(defect_ids) * 3
    n_llm_calls_expected = n_rows_expected
    print(
        f"Participants: {len(participants)} | Defects: {len(defect_ids)} | Runs: {args.runs} | "
        f"Planned rows: {n_rows_expected} | Planned LLM calls: {n_llm_calls_expected}"
    )

    if args.dry_run:
        print("Dry-run OK (no LLM calls, no output written).")
        return 0

    if out_path.exists() and not args.force:
        raise SystemExit(f"Output already exists: {out_path} (use --force to overwrite)")

    llm_service = LLMService(model=args.model, backend=args.backend)  # type: ignore[arg-type]
    evaluator = ExplanationEvaluator(llm_service)

    llm_explanations: dict[str, Any] = {}
    for key, path in sorted(explanation_paths.items()):
        defect_id, run_part = key.split("#run", 1)
        run_id = int(run_part)
        explanation = explanation_texts[key]
        try:
            explanation_file = str(path.relative_to(PROJECT_ROOT))
        except ValueError:
            explanation_file = str(path)
        llm_explanations[key] = {
            "defect_id": defect_id,
            "run_id": run_id,
            "levels": "BASELINE",
            "explanation_file": explanation_file,
            "explanation_sha256": _sha256_text(explanation),
        }

    rows: list[dict[str, Any]] = []
    llm_calls_made = 0
    for p_idx, p in enumerate(participants, start=1):
        print(f"Judging participant {p_idx}/{len(participants)} ({p.participant_id})...", flush=True)
        for defect_id in defect_ids:
            for letter in ("A", "B", "C"):
                run_id = p.explanation_map[defect_id][letter]
                explanation_key = f"{defect_id}#run{run_id}"
                explanation = explanation_texts[explanation_key]
                gt = ground_truth_map[defect_id]
                llm_scores = evaluator.evaluate(explanation, gt)
                llm_calls_made += 1
                llm_scores.pop("reasoning", None)
                llm_labels = {c: int(llm_scores[LLM_SCORE_MAP[c]]) for c in HUMAN_CRITERIA}
                human_labels = {c: int(p.initial_labels[defect_id][letter][c]) for c in HUMAN_CRITERIA}
                human_likert = {c: int(p.likert[defect_id][c]) for c in HUMAN_CRITERIA}
                match = {c: bool(human_labels[c] == llm_labels[c]) for c in HUMAN_CRITERIA}

                rows.append(
                    {
                        "participant_id": p.participant_id,
                        "token_hash": p.token_hash,
                        "defect_id": defect_id,
                        "letter": letter,
                        "run_id": run_id,
                        "levels": "BASELINE",
                        "human_labels": human_labels,
                        "human_likert": human_likert,
                        "llm_labels": llm_labels,
                        "match": match,
                        "explanation_key": explanation_key,
                    }
                )

    if len(rows) != n_rows_expected:
        raise SystemExit(f"Unexpected row count: {len(rows)} (expected {n_rows_expected})")
    if llm_calls_made != n_llm_calls_expected:
        raise SystemExit(
            f"Unexpected LLM call count: {llm_calls_made} (expected {n_llm_calls_expected})"
        )

    # Agreement vs individual human labels (288 pairs per criterion).
    agreement_vs_individuals: dict[str, Any] = {}
    for c in HUMAN_CRITERIA:
        pairs = [(r["human_labels"][c], r["llm_labels"][c]) for r in rows]
        agreement_vs_individuals[c] = _compute_binary_metrics(pairs)

    # Agreement vs majority vote per unique explanation_key (24 items; ties excluded).
    by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_key[r["explanation_key"]].append(r)

    agreement_vs_majority: dict[str, Any] = {}
    for c in HUMAN_CRITERIA:
        ties = 0
        majority_pairs: list[tuple[int, int]] = []
        for key, group in sorted(by_key.items()):
            human_votes = [int(g["human_labels"][c]) for g in group]
            human_maj = _majority_vote(human_votes)
            llm_votes = [int(g["llm_labels"][c]) for g in group]
            llm_maj = _majority_vote(llm_votes)
            if human_maj is None or llm_maj is None:
                ties += 1
                continue
            majority_pairs.append((human_maj, llm_maj))

        metrics = _compute_binary_metrics(majority_pairs)
        metrics["n_items_total"] = len(by_key)
        metrics["n_items_used"] = metrics.pop("n")
        metrics["n_ties"] = ties
        agreement_vs_majority[c] = metrics

    payload = {
        "schema_version": 2,
        "created_at": _now_iso(),
        "judge": {"backend": args.backend, "model": args.model, "strategy": "per_row"},
        "n_participants": len(participants),
        "n_defects": len(defect_ids),
        "n_runs": args.runs,
        "n_rows": len(rows),
        "n_llm_calls": llm_calls_made,
        "llm_explanations": llm_explanations,
        "rows": rows,
        "summary": {
            "agreement_vs_individuals": agreement_vs_individuals,
            "agreement_vs_majority": agreement_vs_majority,
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=False), encoding="utf-8")
    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
