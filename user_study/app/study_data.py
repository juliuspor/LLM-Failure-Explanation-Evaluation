from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CRITERIA: dict[str, dict[str, str]] = {
    "C2": {
        "title": "Problem Identification",
        "text": (
            "Score 1 if the explanation correctly identifies the ROOT CAUSE.\n"
            "Strict rejection: If it only restates the error message (symptom) without explaining WHY it happened, score 0."
        ),
    },
    "C3": {
        "title": "Explanation Clarity",
        "text": (
            "Score 1 if the explanation provides a complete CAUSAL CHAIN.\n"
            "Strict rejection: The “Why” must explicitly explain how the code logic led to the failure. If the explanation is circular, gaps exist, or it just says “it failed”, score 0."
        ),
    },
    "C4": {
        "title": "Actionability",
        "text": (
            "Score 1 if the explanation provides a concrete, numbered list of steps (1., 2., 3.) that explicitly reference specific variable names, function names, or line numbers found in the code.\n"
            "Strict rejection: Score 0 for generic advice like “check the index” or “fix the loop” if specific identifiers are not mentioned."
        ),
    },
    "C6": {
        "title": "Brevity",
        "text": (
            "Score 1 if the explanation is concise and information-dense (little repetition, mostly useful details).\n"
            "Score 0 if it is overly verbose/rambling OR too sparse to be useful."
        ),
    },
}


@dataclass(frozen=True)
class Defect:
    defect_id: str
    function_name: str
    error: str
    ground_truth: str


@dataclass(frozen=True)
class StudyData:
    defects: dict[str, Defect]
    explanations: dict[str, dict[int, str]]  # defect_id -> run_id -> text

    @staticmethod
    def load(study_root: Path) -> "StudyData":
        defects = _load_defects(study_root / "ground_truth.json")
        explanations = _load_explanations(study_root)
        _validate_coverage(defects, explanations)
        return StudyData(defects=defects, explanations=explanations)


def _load_defects(ground_truth_json_path: Path) -> dict[str, Defect]:
    if not ground_truth_json_path.exists():
        raise FileNotFoundError(
            f"Missing ground truth file: {ground_truth_json_path}. "
            "Expected it to exist inside the `user_study/` folder."
        )

    python_defects_value: Any = json.loads(ground_truth_json_path.read_text(encoding="utf-8"))
    if not isinstance(python_defects_value, list):
        raise TypeError("ground_truth.json must be a list")

    defects: dict[str, Defect] = {}
    for item in python_defects_value:
        if not isinstance(item, dict):
            continue
        defect_id = str(item.get("id", "")).strip()
        if not defect_id:
            continue
        defects[defect_id] = Defect(
            defect_id=defect_id,
            function_name=str(item.get("function_name", "")),
            error=str(item.get("error", "")),
            ground_truth=str(item.get("ground_truth", "")),
        )
    if not defects:
        raise ValueError(f"No defects loaded from {ground_truth_json_path}")
    return defects


_EXPL_RE = re.compile(r"^(defect\d+_py)_BASELINE_run(\d+)\.txt$")


def _load_explanations(user_study_dir: Path) -> dict[str, dict[int, str]]:
    explanations: dict[str, dict[int, str]] = {}
    candidate_dirs = [user_study_dir / "stimuli", user_study_dir]
    for candidate_dir in candidate_dirs:
        for path in sorted(candidate_dir.glob("*.txt")):
            match = _EXPL_RE.match(path.name)
            if not match:
                continue
            defect_id, run_id_s = match.groups()
            run_id = int(run_id_s)
            explanations.setdefault(defect_id, {})[run_id] = path.read_text(encoding="utf-8")
        if explanations:
            return explanations
    if not explanations:
        raise ValueError(f"No explanation files found in {user_study_dir / 'stimuli'} or {user_study_dir}")
    return explanations


def _validate_coverage(defects: dict[str, Defect], explanations: dict[str, dict[int, str]]) -> None:
    missing_defects = [d for d in defects if d not in explanations]
    if missing_defects:
        raise ValueError(f"Missing explanations for defects: {missing_defects}")

    for defect_id, by_run in explanations.items():
        missing_runs = [r for r in (1, 2, 3) if r not in by_run]
        if missing_runs:
            raise ValueError(f"Missing run files for {defect_id}: {missing_runs}")
