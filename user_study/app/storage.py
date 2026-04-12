from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)


def token_key(token: str) -> str:
    import hashlib

    # Used for storage object names. Must remain stable across deployments.
    # A plain SHA-256 of the (unguessable) token avoids persisting the raw token.
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class LoadedState:
    state: dict[str, Any] | None
    generation: int | None


class StudyStorage:
    def load_state(self, token: str) -> LoadedState:  # pragma: no cover
        raise NotImplementedError

    def save_state(self, token: str, state: dict[str, Any], if_generation_match: int | None) -> int | None:  # pragma: no cover
        raise NotImplementedError

    def append_audit(self, token: str, event: dict[str, Any]) -> None:  # pragma: no cover
        raise NotImplementedError


class LocalStudyStorage(StudyStorage):
    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _state_path(self, token: str) -> Path:
        key = token_key(token)
        return self._base_dir / "state" / f"{key}.json"

    def _audit_dir(self, token: str) -> Path:
        key = token_key(token)
        return self._base_dir / "audit" / key

    def load_state(self, token: str) -> LoadedState:
        path = self._state_path(token)
        if not path.exists():
            return LoadedState(state=None, generation=None)
        return LoadedState(state=json.loads(path.read_text(encoding="utf-8")), generation=None)

    def save_state(self, token: str, state: dict[str, Any], if_generation_match: int | None) -> int | None:
        path = self._state_path(token)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(_json_dumps(state), encoding="utf-8")
        tmp.replace(path)
        return None

    def append_audit(self, token: str, event: dict[str, Any]) -> None:
        audit_dir = self._audit_dir(token)
        audit_dir.mkdir(parents=True, exist_ok=True)
        ts = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
        nonce = os.urandom(3).hex()
        (audit_dir / f"{ts}_{nonce}_{event.get('type','event')}.json").write_text(
            _json_dumps(event),
            encoding="utf-8",
        )


class GCSStudyStorage(StudyStorage):
    def __init__(self, bucket_name: str) -> None:
        from google.cloud import storage  # type: ignore

        self._client = storage.Client()
        self._bucket = self._client.bucket(bucket_name)

    def _state_blob_name(self, token: str) -> str:
        key = token_key(token)
        return f"user_study/state/{key}.json"

    def _audit_blob_prefix(self, token: str) -> str:
        key = token_key(token)
        return f"user_study/audit/{key}/"

    def load_state(self, token: str) -> LoadedState:
        blob = self._bucket.blob(self._state_blob_name(token))
        if not blob.exists():
            return LoadedState(state=None, generation=None)
        content = blob.download_as_text(encoding="utf-8")
        blob.reload()
        return LoadedState(state=json.loads(content), generation=int(blob.generation or 0) or None)

    def save_state(self, token: str, state: dict[str, Any], if_generation_match: int | None) -> int | None:
        blob = self._bucket.blob(self._state_blob_name(token))
        payload = _json_dumps(state)
        blob.upload_from_string(
            payload,
            content_type="application/json; charset=utf-8",
            if_generation_match=if_generation_match,
        )
        blob.reload()
        return int(blob.generation or 0) or None

    def append_audit(self, token: str, event: dict[str, Any]) -> None:
        ts = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
        nonce = os.urandom(3).hex()
        blob = self._bucket.blob(f"{self._audit_blob_prefix(token)}{ts}_{nonce}_{event.get('type','event')}.json")
        blob.upload_from_string(
            _json_dumps(event),
            content_type="application/json; charset=utf-8",
        )


def create_storage() -> StudyStorage:
    bucket = os.getenv("GCS_BUCKET", "").strip()
    if bucket:
        return GCSStudyStorage(bucket)
    local_dir = Path(os.getenv("USER_STUDY_LOCAL_DIR", "/tmp/user_study_data"))
    return LocalStudyStorage(local_dir)
