import json
import os
import re
import time
import random
from openai import (
    OpenAI, RateLimitError, BadRequestError,
    APIConnectionError, APITimeoutError, InternalServerError
)
import instructor
from pydantic import BaseModel
from typing import Any, Optional, Literal, cast

# Define valid reasoning efforts. 
# "minimal" is specific to GPT-5 series for fastest output, "low" is the standard fast option.
ReasoningEffort = Literal["minimal", "low", "medium", "high"]
OpenRouterReasoningEffort = Literal["xhigh", "high", "medium", "low", "minimal", "none"]
Backend = Literal["openai", "openrouter"]

# Transient errors that should trigger retry with backoff
TRANSIENT_ERRORS = (RateLimitError, APIConnectionError, APITimeoutError, InternalServerError)

OPENROUTER_REASONING_EFFORTS: set[str] = {"xhigh", "high", "medium", "low", "minimal", "none"}

class LLMService:
    def __init__(
        self, 
        model: str = "gpt-5-mini",
        backend: Backend = "openai",
        max_wait: int = 300,         # Max wait between retries (5 minutes)
        max_total_wait: int = 1800,  # Total time willing to wait (30 minutes)
        default_effort: ReasoningEffort = "minimal",
        openrouter_require_parameters: bool = True,
        openrouter_response_healing: bool | None = None,
        openrouter_reasoning_effort: OpenRouterReasoningEffort | None = None,
        openrouter_reasoning_max_tokens: int | None = None,
    ):
        self.backend: Backend = backend
        self.model = model
        self.max_wait = max_wait
        self.max_total_wait = max_total_wait
        self.default_effort = default_effort
        if openrouter_require_parameters is True: # Only check env if default True was passed
            env_req = os.environ.get("OPENROUTER_REQUIRE_PARAMETERS")
            if env_req is not None:
                openrouter_require_parameters = env_req.strip().lower() not in ("0", "false", "no", "off")
        self.openrouter_require_parameters = openrouter_require_parameters
        if openrouter_response_healing is None:
            env = os.environ.get("OPENROUTER_RESPONSE_HEALING")
            if env is None:
                openrouter_response_healing = True
            else:
                openrouter_response_healing = env.strip().lower() not in ("0", "false", "no", "off")
        self.openrouter_response_healing = openrouter_response_healing
        self.openrouter_reasoning_effort: OpenRouterReasoningEffort | None = None
        self.openrouter_reasoning_max_tokens: int | None = None
        if self.backend == "openrouter":
            effort = openrouter_reasoning_effort
            if effort is None:
                env_effort = os.environ.get("OPENROUTER_REASONING_EFFORT")
                if env_effort is not None and env_effort.strip():
                    effort = env_effort.strip().lower()
            else:
                effort = effort.strip().lower()
            if effort is not None:
                if effort not in OPENROUTER_REASONING_EFFORTS:
                    raise ValueError(
                        f"Invalid OPENROUTER_REASONING_EFFORT {effort!r}. "
                        f"Expected one of: {sorted(OPENROUTER_REASONING_EFFORTS)}"
                    )
                self.openrouter_reasoning_effort = cast(OpenRouterReasoningEffort, effort)

            max_tokens = openrouter_reasoning_max_tokens
            if max_tokens is None:
                env_max = os.environ.get("OPENROUTER_REASONING_MAX_TOKENS")
                if env_max is not None and env_max.strip():
                    try:
                        max_tokens = int(env_max.strip())
                    except ValueError as e:
                        raise ValueError(
                            f"Invalid OPENROUTER_REASONING_MAX_TOKENS {env_max!r}. "
                            "Expected an integer."
                        ) from e
            if max_tokens is not None:
                if max_tokens <= 0:
                    raise ValueError(
                        f"Invalid OPENROUTER_REASONING_MAX_TOKENS {max_tokens!r}. Expected a positive integer."
                    )
                self.openrouter_reasoning_max_tokens = int(max_tokens)

            # OpenRouter allows either reasoning.effort or reasoning.max_tokens (not both).
            # If both are configured, prefer max_tokens for determinism.
            if self.openrouter_reasoning_effort is not None and self.openrouter_reasoning_max_tokens is not None:
                print(
                    "Warning: Both OPENROUTER_REASONING_EFFORT and OPENROUTER_REASONING_MAX_TOKENS are set; "
                    "using reasoning.max_tokens and omitting reasoning.effort.",
                    flush=True,
                )
                self.openrouter_reasoning_effort = None

            # Grok 4.1 Fast: default to minimal reasoning (same default effort as GPT-5 in our OpenAI backend)
            # unless the user explicitly configures it via constructor args or env vars.
            if self.openrouter_reasoning_effort is None and self.openrouter_reasoning_max_tokens is None:
                if self.model.strip().lower().endswith("grok-4.1-fast"):
                    self.openrouter_reasoning_effort = "none"

        self.client = self._build_client()
        self.instructor_client = instructor.from_openai(self.client)

    def _build_client(self) -> OpenAI:
        if self.backend == "openai":
            return OpenAI()

        if self.backend == "openrouter":
            api_key = os.environ.get("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY must be set when backend='openrouter'.")

            default_headers: dict[str, str] = {}
            site_url = os.environ.get("OPENROUTER_SITE_URL")
            app_name = os.environ.get("OPENROUTER_APP_NAME")
            if site_url:
                default_headers["HTTP-Referer"] = site_url
            if app_name:
                default_headers["X-Title"] = app_name

            return OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers=default_headers or None,
            )

        raise ValueError(f"Unknown backend: {self.backend!r}")

    def _supports_reasoning_effort(self) -> bool:
        # reasoning_effort is currently GPT-5 specific in our usage.
        return self.backend == "openai" and self.model.startswith("gpt-5")

    def _extra_body(self, structured: bool = False) -> dict[str, Any] | None:
        if self.backend != "openrouter":
            return None

        body: dict[str, Any] = {}

        provider: dict[str, Any] = {}
        if structured or self.openrouter_require_parameters:
            provider["require_parameters"] = True
        if provider:
            body["provider"] = provider

        if self.openrouter_reasoning_max_tokens is not None:
            body["reasoning"] = {"max_tokens": self.openrouter_reasoning_max_tokens}
        elif self.openrouter_reasoning_effort is not None:
            body["reasoning"] = {"effort": self.openrouter_reasoning_effort}

        if structured and self.openrouter_response_healing:
            body["plugins"] = [{"id": "response-healing"}]

        return body or None

    def _retry_with_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff on transient errors.
        
        Retries until max_total_wait time is exceeded (default 30 minutes).
        Uses exponential backoff (2^attempt seconds) capped at max_wait (default 5 minutes).
        """
        total_waited = 0
        attempt = 0
        
        while True:
            try:
                return func(*args, **kwargs)
            except TRANSIENT_ERRORS as e:
                attempt += 1
                
                # Exponential backoff with jitter, capped at max_wait
                wait_time = min(2 ** attempt, self.max_wait) + random.uniform(0, 1)
                
                # Check if we've exceeded total wait time
                if total_waited + wait_time > self.max_total_wait:
                    print(f"\nMax total wait time ({self.max_total_wait}s) exceeded after {attempt} attempts. Giving up.")
                    raise e
                
                error_type = type(e).__name__
                print(f"\n{error_type}: waiting {wait_time:.0f}s (attempt {attempt}, total waited: {total_waited:.0f}s)...", 
                      flush=True)
                time.sleep(wait_time)
                total_waited += wait_time
                
            except BadRequestError as e:
                message = str(e)

                # OpenRouter: some routes reject reasoning.effort="none".
                if self.backend == "openrouter":
                    if "Reasoning is mandatory" in message and self.openrouter_reasoning_effort == "none":
                        print(
                            "Warning: reasoning.effort='none' rejected by OpenRouter route; retrying without it",
                            flush=True,
                        )
                        # Persistently drop this setting to avoid repeated 400s on subsequent calls.
                        self.openrouter_reasoning_effort = None
                        return func(*args, **kwargs)

                # OpenAI: specific error handling for unsupported "minimal" effort
                if "reasoning_effort" in message and kwargs.get("reasoning_effort") == "minimal":
                    print("Warning: 'minimal' effort not supported, falling back to 'low'")
                    kwargs["reasoning_effort"] = "low"
                    return func(*args, **kwargs)
                raise e

    def generate(self, prompt: str, reasoning_effort: Optional[ReasoningEffort] = None) -> str:
        """Generates text response with optimized speed settings."""
        # Use instance default if not provided
        effort = reasoning_effort or self.default_effort
        
        def _call(reasoning_effort=effort):
            extra_body = self._extra_body()
            request_kwargs: dict[str, Any] = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
            }
            if self.backend == "openrouter":
                request_kwargs["temperature"] = 0
            if self._supports_reasoning_effort():
                request_kwargs["reasoning_effort"] = reasoning_effort
            if extra_body is not None:
                request_kwargs["extra_body"] = extra_body

            response = self.client.chat.completions.create(**request_kwargs)
            return response.choices[0].message.content
        
        return self._retry_with_backoff(_call, reasoning_effort=effort)

    def generate_structured(
        self, 
        prompt: str, 
        response_model: type[BaseModel],
        reasoning_effort: Optional[ReasoningEffort] = None
    ) -> BaseModel:
        """Generates structured response with optimized speed settings."""
        effort = reasoning_effort or self.default_effort

        def _call(reasoning_effort=effort):
            extra_body = self._extra_body(structured=True)
            if self.backend == "openrouter":
                def _extract_json(text: str) -> dict[str, Any]:
                    candidate = text.strip()
                    if candidate.startswith("```"):
                        # Strip Markdown fences like ```json ... ```
                        lines = candidate.splitlines()
                        if lines:
                            lines = lines[1:]
                        if lines and lines[-1].strip() == "```":
                            lines = lines[:-1]
                        candidate = "\n".join(lines).strip()

                    try:
                        parsed = json.loads(candidate)
                    except json.JSONDecodeError:
                        start = candidate.find("{")
                        end = candidate.rfind("}")
                        if start == -1 or end == -1 or end < start:
                            preview = candidate[:500].replace("\n", "\\n")
                            raise ValueError(f"Structured output was not valid JSON. Preview: {preview!r}")
                        parsed = json.loads(candidate[start : end + 1])

                    if not isinstance(parsed, dict):
                        raise ValueError(f"Expected JSON object for structured output, got {type(parsed).__name__}")
                    return parsed

                schema = response_model.model_json_schema()
                if schema.get("type") == "object" and "additionalProperties" not in schema:
                    schema["additionalProperties"] = False

                request_kwargs: dict[str, Any] = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0,
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": {
                            "name": response_model.__name__,
                            "strict": True,
                            "schema": schema,
                        },
                    },
                }  # OpenRouter path always uses temperature=0
                if extra_body is not None:
                    request_kwargs["extra_body"] = extra_body

                response = self.client.chat.completions.create(**request_kwargs)
                content = response.choices[0].message.content
                if not content:
                    raise ValueError("Empty response content for structured output.")
                try:
                    data = _extract_json(content)
                except Exception:
                    data = _fallback_structured_dict(content, response_model)
                return response_model.model_validate(data)

            request_kwargs = {
                "model": self.model,
                "response_model": response_model,
                "messages": [{"role": "user", "content": prompt}],
            }
            if self._supports_reasoning_effort():
                request_kwargs["reasoning_effort"] = reasoning_effort
            if extra_body is not None:
                request_kwargs["extra_body"] = extra_body

            return self.instructor_client.chat.completions.create(**request_kwargs)
        
        return self._retry_with_backoff(_call, reasoning_effort=effort)


def _truncate(text: str, *, max_chars: int) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 15].rstrip() + "… (truncated)"


def _parse_binary_score(text: str, key: str) -> int | None:
    # Common formats:
    # - **C2 (Problem Identification): 0**
    # - C2: 1
    # - | **C2 – Problem Identification** | **1** | ...
    pattern = rf"(?is)\b{re.escape(key)}\b[^0-9]{{0,40}}([01])(?!\.)\b"
    m = re.search(pattern, text)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def _parse_unit_float(text: str, key: str) -> float | None:
    # Extract a float in [0, 1] following the key, e.g. "C6: 0.35"
    pattern = rf"(?is)\b{re.escape(key)}\b[^0-9]{{0,40}}((?:0(?:\.\d+)?|1(?:\.0+)?))\b"
    m = re.search(pattern, text)
    if not m:
        return None
    try:
        v = float(m.group(1))
    except ValueError:
        return None
    if 0.0 <= v <= 1.0:
        return v
    return None


def _extract_first_code_block(text: str) -> str | None:
    m = re.search(r"```(?:python|py)?\s*\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    return m.group(1).strip()


def _fallback_structured_dict(text: str, response_model: type[BaseModel]) -> dict[str, Any]:
    fields = set(getattr(response_model, "model_fields", {}).keys())

    if fields == {"explanation"}:
        return {"explanation": text.strip()}

    if fields == {"C2", "C3", "C4", "C6", "reasoning"}:
        c2 = _parse_binary_score(text, "C2") or 0
        c3 = _parse_binary_score(text, "C3") or 0
        c4 = _parse_binary_score(text, "C4") or 0
        c6 = _parse_binary_score(text, "C6") or 0

        return {
            "C2": int(c2),
            "C3": int(c3),
            "C4": int(c4),
            "C6": int(c6),
            "reasoning": _truncate(text, max_chars=4000),
        }

    if fields == {"thought_process", "code"}:
        code = _extract_first_code_block(text)
        if code is None:
            code = text.strip()
        return {
            "thought_process": "Heuristic fallback: model returned non-JSON structured output.",
            "code": code,
        }

    raise ValueError(f"Unsupported structured response model fields: {sorted(fields)}")
