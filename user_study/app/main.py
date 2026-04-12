from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .storage import LoadedState, StudyStorage, create_storage, token_key
from .study_data import CRITERIA, StudyData
from .warmup_data import WARMUP_DEFECT, WARMUP_EXPLANATIONS


APP_DIR = Path(__file__).resolve().parent
STUDY_ROOT = Path(__file__).resolve().parents[1]

STUDY = StudyData.load(STUDY_ROOT)
STORAGE = create_storage()

LETTERS = ("A", "B", "C")
CRIT_KEYS = ("C2", "C3", "C4", "C6")


app = FastAPI(title="User Study (RQ2)")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _compute_seed(token: str) -> int:
    import hashlib

    return int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16) % (2**32)


def _compute_seed_for_text(text: str) -> int:
    import hashlib

    return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (2**32)


def _letter_order(token: str, defect_id: str) -> list[str]:
    import random

    order = list(LETTERS)
    rng = random.Random(_compute_seed_for_text(f"{token}|order|{defect_id}"))
    rng.shuffle(order)
    return order


def _any_real_progress(state: dict[str, Any]) -> bool:
    responses = state.get("responses", {})
    if not isinstance(responses, dict):
        return False
    for key in ("initial_labels", "likert"):
        value = responses.get(key)
        if isinstance(value, dict) and value:
            return True
    return False


def _new_state(token: str) -> dict[str, Any]:
    import random

    rng = random.Random(_compute_seed(token))
    defect_ids = sorted(STUDY.defects.keys())
    rng.shuffle(defect_ids)

    explanation_map: dict[str, dict[str, int]] = {}
    explanation_order: dict[str, list[str]] = {}
    for defect_id in defect_ids:
        runs = [1, 2, 3]
        rng.shuffle(runs)
        explanation_map[defect_id] = {letter: run_id for letter, run_id in zip(LETTERS, runs, strict=True)}
        explanation_order[defect_id] = _letter_order(token, defect_id)

    return {
        "schema_version": 2,
        "participant": {
            "created_at": _now_iso(),
            "token_hash": token_key(token),
            "consent": False,
            "warmup_label_completed": False,
            "warmup_completed": False,
        },
        "assignment": {
            "defect_order": defect_ids,
            "explanation_map": explanation_map,
            "explanation_order": explanation_order,
        },
        "responses": {
            "initial_labels": {},
            "likert": {},
            "interview": {},
        },
        "app": {
            "app_env": os.getenv("APP_ENV", "local"),
            "git_sha": os.getenv("GIT_SHA", ""),
        },
    }


def _normalize_state(state: dict[str, Any] | None, token: str) -> dict[str, Any]:
    if state is None:
        state = _new_state(token)
    state.setdefault("schema_version", 2)
    state.setdefault("participant", {})
    state["participant"].setdefault("created_at", _now_iso())
    state["participant"].setdefault("token_hash", token_key(token))
    state["participant"].setdefault("consent", False)
    state["participant"].setdefault("participant_id", "")
    state["participant"].setdefault("warmup_label_completed", False)
    state["participant"].setdefault("warmup_completed", False)
    state.setdefault("assignment", {})
    state["assignment"].setdefault("defect_order", sorted(STUDY.defects.keys()))
    state["assignment"].setdefault("explanation_map", {})
    state["assignment"].setdefault("explanation_order", {})
    state.setdefault("responses", {})
    for k in ("initial_labels", "likert", "interview"):
        state["responses"].setdefault(k, {})
    state.setdefault("app", {})
    state["app"].setdefault("git_sha", os.getenv("GIT_SHA", ""))
    state["app"].setdefault("app_env", os.getenv("APP_ENV", "local"))

    # If a participant already started real tasks (before warm-up was introduced), auto-skip warm-up.
    if _any_real_progress(state):
        state["participant"]["warmup_label_completed"] = True
        state["participant"]["warmup_completed"] = True

    # Ensure per-defect display order exists and is valid.
    order_map = state["assignment"].get("explanation_order")
    if not isinstance(order_map, dict):
        order_map = {}
        state["assignment"]["explanation_order"] = order_map
    for defect_id in state["assignment"].get("defect_order", sorted(STUDY.defects.keys())):
        cur = order_map.get(defect_id)
        if not isinstance(cur, list) or sorted(cur) != list(LETTERS):
            order_map[str(defect_id)] = _letter_order(token, str(defect_id))
    return state


def _require_consent(state: dict[str, Any]) -> None:
    if not state.get("participant", {}).get("consent", False):
        raise HTTPException(status_code=403, detail="Consent required")


def _require_participant_id(state: dict[str, Any]) -> None:
    participant_id = str(state.get("participant", {}).get("participant_id", "")).strip()
    if not participant_id:
        raise HTTPException(status_code=403, detail="Participant ID required")


def _require_ready(state: dict[str, Any]) -> None:
    _require_consent(state)
    _require_participant_id(state)


def _label_complete(state: dict[str, Any], defect_id: str) -> bool:
    labels = state["responses"]["initial_labels"].get(defect_id, {})
    return all(labels.get(letter, {}).get(crit) in (0, 1) for letter in LETTERS for crit in CRIT_KEYS)

def _likert_complete(state: dict[str, Any], defect_id: str) -> bool:
    likert = state["responses"]["likert"].get(defect_id, {})
    return all(likert.get(crit) in (1, 2, 3, 4, 5) for crit in CRIT_KEYS)


def _next_url(token: str, state: dict[str, Any]) -> str:
    if not state.get("participant", {}).get("warmup_completed", False):
        if state.get("participant", {}).get("warmup_label_completed", False):
            return f"/t/{token}/warmup/likert"
        return f"/t/{token}/warmup/label"
    for defect_id in state["assignment"]["defect_order"]:
        if not _label_complete(state, defect_id):
            return f"/t/{token}/d/{defect_id}/label"
        if not _likert_complete(state, defect_id):
            return f"/t/{token}/d/{defect_id}/likert"
    return f"/t/{token}/done"


def _progress(state: dict[str, Any]) -> dict[str, Any]:
    order = state["assignment"]["defect_order"]
    completed = sum(1 for d in order if _likert_complete(state, d))
    return {"completed": completed, "total": len(order)}


def _defect_context(state: dict[str, Any], defect_id: str) -> dict[str, Any]:
    defect = STUDY.defects.get(defect_id)
    if defect is None:
        raise HTTPException(status_code=404, detail="Unknown defect")
    run_map = state["assignment"]["explanation_map"].get(defect_id)
    if not isinstance(run_map, dict) or any(letter not in run_map for letter in LETTERS):
        raise HTTPException(status_code=500, detail="Missing explanation mapping")

    letter_order = state["assignment"].get("explanation_order", {}).get(defect_id)
    if not isinstance(letter_order, list) or sorted(letter_order) != list(LETTERS):
        letter_order = list(LETTERS)
    explanations = []
    for letter in letter_order:
        run_id = int(run_map[letter])
        explanations.append(
            {
                "letter": letter,
                "run_id": run_id,
                "text": STUDY.explanations[defect_id][run_id],
            }
        )
    order = state["assignment"].get("defect_order", [])
    try:
        defect_idx = int(order.index(defect_id)) + 1
    except Exception:
        defect_idx = None
    return {
        "defect": defect,
        "explanations": explanations,
        "defect_idx": defect_idx,
    }


def _warmup_context(token: str) -> dict[str, Any]:
    order = _letter_order(token, "warmup")
    explanations = [{"letter": letter, "run_id": 0, "text": WARMUP_EXPLANATIONS[letter]} for letter in order]
    return {
        "defect": WARMUP_DEFECT,
        "explanations": explanations,
        "defect_idx": None,
    }


def _redirect_to_warmup_if_needed(token: str, state: dict[str, Any]) -> RedirectResponse | None:
    if not state.get("participant", {}).get("warmup_completed", False):
        return RedirectResponse(_next_url(token, state), status_code=303)
    return None


def _save_with_audit(storage: StudyStorage, token: str, loaded: LoadedState, state: dict[str, Any], event: dict[str, Any]) -> None:
    for attempt in range(3):
        try:
            storage.save_state(token, state, if_generation_match=loaded.generation if attempt == 0 else None)
            break
        except Exception:
            if attempt >= 2:
                raise
            time.sleep(0.05)
    storage.append_audit(token, event)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@app.get("/t/{token}", response_class=HTMLResponse)
async def entry(token: str, request: Request) -> HTMLResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    if state["participant"].get("consent", False) and not str(state["participant"].get("participant_id", "")).strip():
        return RedirectResponse(f"/t/{token}/identify", status_code=303)
    if state["participant"].get("consent", False):
        return RedirectResponse(_next_url(token, state), status_code=303)

    return templates.TemplateResponse(
        "consent.html",
        {
            "request": request,
            "token": token,
            "progress": _progress(state),
        },
    )


@app.get("/t/{token}/identify", response_class=HTMLResponse)
async def identify_get(token: str, request: Request) -> HTMLResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_consent(state)

    return templates.TemplateResponse(
        "identify.html",
        {
            "request": request,
            "token": token,
            "progress": _progress(state),
            "existing": str(state.get("participant", {}).get("participant_id", "")).strip(),
        },
    )


@app.post("/t/{token}/identify")
async def identify_post(token: str, request: Request) -> RedirectResponse:
    form = await request.form()
    participant_id = str(form.get("participant_id", "")).strip()
    if not participant_id:
        raise HTTPException(status_code=400, detail="Participant ID required")

    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_consent(state)
    state["participant"]["participant_id"] = participant_id
    state["participant"]["last_updated_at"] = _now_iso()

    _save_with_audit(
        STORAGE,
        token,
        loaded,
        state,
        {"type": "identify", "ts": _now_iso(), "participant_id": participant_id},
    )
    return RedirectResponse(_next_url(token, state), status_code=303)


@app.post("/t/{token}/consent")
async def consent(token: str, request: Request) -> RedirectResponse:
    form = await request.form()
    if form.get("consent") != "yes":
        raise HTTPException(status_code=400, detail="Consent not provided")
    participant_id = str(form.get("participant_id", "")).strip()
    if not participant_id:
        raise HTTPException(status_code=400, detail="Participant ID required")

    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    state["participant"]["consent"] = True
    state["participant"]["consented_at"] = _now_iso()
    state["participant"]["participant_id"] = participant_id
    state["participant"]["last_updated_at"] = _now_iso()

    _save_with_audit(
        STORAGE,
        token,
        loaded,
        state,
        {"type": "consent", "ts": _now_iso(), "participant_id": participant_id},
    )
    return RedirectResponse(_next_url(token, state), status_code=303)


@app.get("/t/{token}/warmup/label", response_class=HTMLResponse)
async def warmup_label_get(token: str, request: Request) -> HTMLResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    if state["participant"].get("warmup_completed", False):
        return RedirectResponse(_next_url(token, state), status_code=303)
    if state["participant"].get("warmup_label_completed", False):
        return RedirectResponse(f"/t/{token}/warmup/likert", status_code=303)

    ctx = _warmup_context(token)
    return templates.TemplateResponse(
        "label.html",
        {
            "request": request,
            "token": token,
            "defect_id": "warmup",
            "mode": "warmup",
            "criteria": CRITERIA,
            "crit_keys": CRIT_KEYS,
            "progress": _progress(state),
            "existing": {},
            "is_warmup": True,
            "page_title": "Warm-up — Label",
            "post_url": f"/t/{token}/warmup/label",
            **ctx,
        },
    )


@app.post("/t/{token}/warmup/label")
async def warmup_label_post(token: str, request: Request) -> RedirectResponse:
    form = await request.form()
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    if state["participant"].get("warmup_completed", False):
        return RedirectResponse(_next_url(token, state), status_code=303)

    for letter in LETTERS:
        for crit in CRIT_KEYS:
            raw = form.get(f"label_{letter}_{crit}")
            if raw not in ("0", "1"):
                raise HTTPException(status_code=400, detail=f"Missing warm-up label for {letter} {crit}")

    state["participant"]["warmup_label_completed"] = True
    state["participant"]["last_updated_at"] = _now_iso()
    _save_with_audit(
        STORAGE,
        token,
        loaded,
        state,
        {"type": "warmup_label_complete", "ts": _now_iso()},
    )
    return RedirectResponse(f"/t/{token}/warmup/likert", status_code=303)


@app.get("/t/{token}/warmup/likert", response_class=HTMLResponse)
async def warmup_likert_get(token: str, request: Request) -> HTMLResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    if state["participant"].get("warmup_completed", False):
        return RedirectResponse(_next_url(token, state), status_code=303)
    if not state["participant"].get("warmup_label_completed", False):
        return RedirectResponse(f"/t/{token}/warmup/label", status_code=303)

    ctx = _warmup_context(token)
    return templates.TemplateResponse(
        "likert.html",
        {
            "request": request,
            "token": token,
            "defect_id": "warmup",
            "criteria": CRITERIA,
            "crit_keys": CRIT_KEYS,
            "progress": _progress(state),
            "existing": {},
            "is_warmup": True,
            "page_title": "Warm-up — Difficulty / Uncertainty",
            "post_url": f"/t/{token}/warmup/likert",
            **ctx,
        },
    )


@app.post("/t/{token}/warmup/likert")
async def warmup_likert_post(token: str, request: Request) -> RedirectResponse:
    form = await request.form()
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    if state["participant"].get("warmup_completed", False):
        return RedirectResponse(_next_url(token, state), status_code=303)
    if not state["participant"].get("warmup_label_completed", False):
        return RedirectResponse(f"/t/{token}/warmup/label", status_code=303)

    for crit in CRIT_KEYS:
        raw = form.get(f"likert_{crit}")
        if raw not in ("1", "2", "3", "4", "5"):
            raise HTTPException(status_code=400, detail=f"Missing warm-up Likert for {crit}")

    state["participant"]["warmup_label_completed"] = True
    state["participant"]["warmup_completed"] = True
    state["participant"]["warmup_completed_at"] = _now_iso()
    state["participant"]["last_updated_at"] = _now_iso()

    _save_with_audit(
        STORAGE,
        token,
        loaded,
        state,
        {"type": "warmup_complete", "ts": _now_iso()},
    )
    return RedirectResponse(_next_url(token, state), status_code=303)


@app.get("/t/{token}/d/{defect_id}/label", response_class=HTMLResponse)
async def label_get(token: str, defect_id: str, request: Request) -> HTMLResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect

    ctx = _defect_context(state, defect_id)
    existing = state["responses"]["initial_labels"].get(defect_id, {})

    return templates.TemplateResponse(
        "label.html",
        {
            "request": request,
            "token": token,
            "defect_id": defect_id,
            "mode": "initial",
            "criteria": CRITERIA,
            "crit_keys": CRIT_KEYS,
            "progress": _progress(state),
            "existing": existing,
            **ctx,
        },
    )


@app.post("/t/{token}/d/{defect_id}/label")
async def label_post(token: str, defect_id: str, request: Request) -> RedirectResponse:
    form = await request.form()
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect
    _defect_context(state, defect_id)

    labels_for_defect: dict[str, dict[str, int]] = {}
    for letter in LETTERS:
        labels_for_defect[letter] = {}
        for crit in CRIT_KEYS:
            raw = form.get(f"label_{letter}_{crit}")
            if raw not in ("0", "1"):
                raise HTTPException(status_code=400, detail=f"Missing label for {letter} {crit}")
            labels_for_defect[letter][crit] = int(raw)

    state["responses"]["initial_labels"][defect_id] = labels_for_defect
    state["participant"]["last_updated_at"] = _now_iso()

    _save_with_audit(
        STORAGE,
        token,
        loaded,
        state,
        {"type": "label_initial", "ts": _now_iso(), "defect_id": defect_id, "labels": labels_for_defect},
    )
    return RedirectResponse(f"/t/{token}/d/{defect_id}/likert", status_code=303)


@app.get("/t/{token}/d/{defect_id}/rank")
async def rank_get(token: str, defect_id: str, request: Request) -> RedirectResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect
    if not _label_complete(state, defect_id):
        return RedirectResponse(f"/t/{token}/d/{defect_id}/label", status_code=303)
    return RedirectResponse(f"/t/{token}/d/{defect_id}/likert", status_code=303)


@app.post("/t/{token}/d/{defect_id}/rank")
async def rank_post(token: str, defect_id: str, request: Request) -> RedirectResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect
    if not _label_complete(state, defect_id):
        return RedirectResponse(f"/t/{token}/d/{defect_id}/label", status_code=303)
    return RedirectResponse(f"/t/{token}/d/{defect_id}/likert", status_code=303)


@app.get("/t/{token}/d/{defect_id}/relabel")
async def relabel_get(token: str, defect_id: str, request: Request) -> RedirectResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect
    if not _label_complete(state, defect_id):
        return RedirectResponse(f"/t/{token}/d/{defect_id}/label", status_code=303)
    return RedirectResponse(f"/t/{token}/d/{defect_id}/likert", status_code=303)


@app.post("/t/{token}/d/{defect_id}/relabel")
async def relabel_post(token: str, defect_id: str, request: Request) -> RedirectResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect
    if not _label_complete(state, defect_id):
        return RedirectResponse(f"/t/{token}/d/{defect_id}/label", status_code=303)
    return RedirectResponse(f"/t/{token}/d/{defect_id}/likert", status_code=303)


@app.get("/t/{token}/d/{defect_id}/likert", response_class=HTMLResponse)
async def likert_get(token: str, defect_id: str, request: Request) -> HTMLResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect
    if not _label_complete(state, defect_id):
        return RedirectResponse(f"/t/{token}/d/{defect_id}/label", status_code=303)

    ctx = _defect_context(state, defect_id)
    existing = state["responses"]["likert"].get(defect_id, {})

    return templates.TemplateResponse(
        "likert.html",
        {
            "request": request,
            "token": token,
            "defect_id": defect_id,
            "criteria": CRITERIA,
            "crit_keys": CRIT_KEYS,
            "progress": _progress(state),
            "existing": existing,
            **ctx,
        },
    )


@app.post("/t/{token}/d/{defect_id}/likert")
async def likert_post(token: str, defect_id: str, request: Request) -> RedirectResponse:
    form = await request.form()
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect

    if not _label_complete(state, defect_id):
        return RedirectResponse(f"/t/{token}/d/{defect_id}/label", status_code=303)

    likert_for_defect: dict[str, int] = {}
    for crit in CRIT_KEYS:
        raw = form.get(f"likert_{crit}")
        if raw not in ("1", "2", "3", "4", "5"):
            raise HTTPException(status_code=400, detail=f"Missing Likert for {crit}")
        likert_for_defect[crit] = int(raw)

    state["responses"]["likert"][defect_id] = likert_for_defect
    state["participant"]["last_updated_at"] = _now_iso()

    _save_with_audit(
        STORAGE,
        token,
        loaded,
        state,
        {"type": "likert", "ts": _now_iso(), "defect_id": defect_id, "likert": likert_for_defect},
    )

    return RedirectResponse(_next_url(token, state), status_code=303)


@app.get("/t/{token}/done", response_class=HTMLResponse)
async def done(token: str, request: Request) -> HTMLResponse:
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect
    next_url = _next_url(token, state)
    if next_url != f"/t/{token}/done":
        return RedirectResponse(next_url, status_code=303)

    return templates.TemplateResponse(
        "done.html",
        {
            "request": request,
            "token": token,
            "progress": _progress(state),
            "saved": request.query_params.get("saved") == "1",
            "interview": state["responses"].get("interview", {}),
        },
    )


@app.post("/t/{token}/done")
async def done_post(token: str, request: Request) -> RedirectResponse:
    form = await request.form()
    loaded = STORAGE.load_state(token)
    state = _normalize_state(loaded.state, token)
    _require_ready(state)
    warmup_redirect = _redirect_to_warmup_if_needed(token, state)
    if warmup_redirect is not None:
        return warmup_redirect
    next_url = _next_url(token, state)
    if next_url != f"/t/{token}/done":
        return RedirectResponse(next_url, status_code=303)

    judging = str(form.get("interview_judging", "")).strip()
    has_ranking_field = "interview_ranking" in form
    ranking = str(form.get("interview_ranking", "")).strip() if has_ranking_field else None

    interview = state["responses"].get("interview", {})
    if not isinstance(interview, dict):
        interview = {}
    interview.setdefault("created_at", _now_iso())
    interview["judging_by_criterion"] = judging
    if ranking is not None:
        interview["ranking_challenges"] = ranking
    interview["updated_at"] = _now_iso()
    state["responses"]["interview"] = interview
    state["participant"]["last_updated_at"] = _now_iso()

    audit_responses: dict[str, str] = {"judging_by_criterion": judging}
    if ranking is not None:
        audit_responses["ranking_challenges"] = ranking
    _save_with_audit(
        STORAGE,
        token,
        loaded,
        state,
        {
            "type": "interview",
            "ts": _now_iso(),
            "responses": {
                **audit_responses,
            },
        },
    )

    return RedirectResponse(f"/t/{token}/done?saved=1", status_code=303)
