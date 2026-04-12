"""
Offline unit tests that verify temperature is explicitly set to 0 for both
OpenAI and OpenRouter calls in src.llm.LLMService.

These tests do not make network calls; they patch the OpenAI client methods and
validate request shaping.
"""

from __future__ import annotations

import os
import sys
import unittest
from unittest.mock import patch

from pydantic import BaseModel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.llm import LLMService  # noqa: E402


class _DummyStructured(BaseModel):
    explanation: str


class _DummyMessage:
    def __init__(self, content: str):
        self.content = content


class _DummyChoice:
    def __init__(self, content: str):
        self.message = _DummyMessage(content)


class _DummyResponse:
    def __init__(self, content: str):
        self.choices = [_DummyChoice(content)]


class TestLLMTemperatureDefaults(unittest.TestCase):
    def test_openai_generate_sets_temperature_zero(self) -> None:
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}, clear=True):
            llm = LLMService(backend="openai", model="gpt-5-mini")
            captured: dict[str, object] = {}

            def fake_create(**kwargs):  # type: ignore[no-untyped-def]
                captured.update(kwargs)
                return _DummyResponse("ok")

            with patch.object(llm.client.chat.completions, "create", side_effect=fake_create):
                out = llm.generate("hi")
                self.assertEqual(out, "ok")
                self.assertEqual(captured.get("temperature"), 0)

    def test_openai_generate_structured_sets_temperature_zero(self) -> None:
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}, clear=True):
            llm = LLMService(backend="openai", model="gpt-5-mini")
            captured: dict[str, object] = {}

            def fake_create(**kwargs):  # type: ignore[no-untyped-def]
                captured.update(kwargs)
                model_cls = kwargs["response_model"]
                return model_cls.model_validate({"explanation": "ok"})

            with patch.object(llm.instructor_client.chat.completions, "create", side_effect=fake_create):
                out = llm.generate_structured("hi", _DummyStructured)
                self.assertEqual(out.explanation, "ok")
                self.assertEqual(captured.get("temperature"), 0)

    def test_openrouter_generate_sets_temperature_zero(self) -> None:
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "sk-or-test"}, clear=True):
            llm = LLMService(backend="openrouter", model="deepseek/deepseek-v3.2")
            captured: dict[str, object] = {}

            def fake_create(**kwargs):  # type: ignore[no-untyped-def]
                captured.update(kwargs)
                return _DummyResponse("ok")

            with patch.object(llm.client.chat.completions, "create", side_effect=fake_create):
                out = llm.generate("hi")
                self.assertEqual(out, "ok")
                self.assertEqual(captured.get("temperature"), 0)

    def test_openrouter_generate_structured_sets_temperature_zero(self) -> None:
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "sk-or-test"}, clear=True):
            llm = LLMService(backend="openrouter", model="deepseek/deepseek-v3.2")
            captured: dict[str, object] = {}

            def fake_create(**kwargs):  # type: ignore[no-untyped-def]
                captured.update(kwargs)
                return _DummyResponse('{"explanation":"ok"}')

            with patch.object(llm.client.chat.completions, "create", side_effect=fake_create):
                out = llm.generate_structured("hi", _DummyStructured)
                self.assertEqual(out.explanation, "ok")
                self.assertEqual(captured.get("temperature"), 0)


if __name__ == "__main__":
    unittest.main()

