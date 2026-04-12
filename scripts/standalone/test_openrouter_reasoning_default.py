"""
Unit tests for the OpenRouter reasoning default behavior in src.llm.LLMService.

These tests are offline (no network calls) and only validate request shaping via _extra_body().
"""

from __future__ import annotations

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.llm import LLMService  # noqa: E402


class TestOpenRouterReasoningDefault(unittest.TestCase):
    def test_reasoning_is_omitted_when_unset(self) -> None:
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "dummy"}, clear=True):
            llm = LLMService(backend="openrouter", model="deepseek/deepseek-v3.2")
            body = llm._extra_body()
            assert body is not None
            self.assertNotIn("reasoning", body)

    def test_grok_default_sets_reasoning_minimal(self) -> None:
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "dummy"}, clear=True):
            llm = LLMService(backend="openrouter", model="x-ai/grok-4.1-fast")
            body = llm._extra_body()
            assert body is not None
            self.assertEqual(body.get("reasoning", {}).get("effort"), "minimal")

    def test_env_override_is_applied(self) -> None:
        with patch.dict(
            os.environ,
            {"OPENROUTER_API_KEY": "dummy", "OPENROUTER_REASONING_EFFORT": "minimal"},
            clear=True,
        ):
            llm = LLMService(backend="openrouter", model="deepseek/deepseek-v3.2")
            body = llm._extra_body()
            assert body is not None
            self.assertEqual(body["reasoning"]["effort"], "minimal")

    def test_env_max_tokens_is_applied(self) -> None:
        with patch.dict(
            os.environ,
            {"OPENROUTER_API_KEY": "dummy", "OPENROUTER_REASONING_MAX_TOKENS": "64"},
            clear=True,
        ):
            llm = LLMService(backend="openrouter", model="deepseek/deepseek-v3.2")
            body = llm._extra_body()
            assert body is not None
            self.assertEqual(body["reasoning"]["max_tokens"], 64)

    def test_invalid_env_value_raises(self) -> None:
        with patch.dict(
            os.environ,
            {"OPENROUTER_API_KEY": "dummy", "OPENROUTER_REASONING_EFFORT": "bogus"},
            clear=True,
        ):
            with self.assertRaises(ValueError):
                _ = LLMService(backend="openrouter", model="deepseek/deepseek-v3.2")

    def test_constructor_override_beats_env(self) -> None:
        with patch.dict(
            os.environ,
            {"OPENROUTER_API_KEY": "dummy", "OPENROUTER_REASONING_EFFORT": "high"},
            clear=True,
        ):
            llm = LLMService(
                backend="openrouter",
                model="deepseek/deepseek-v3.2",
                openrouter_reasoning_effort="minimal",
            )
            body = llm._extra_body()
            assert body is not None
            self.assertEqual(body["reasoning"]["effort"], "minimal")

    def test_max_tokens_beats_effort(self) -> None:
        with patch.dict(
            os.environ,
            {
                "OPENROUTER_API_KEY": "dummy",
                "OPENROUTER_REASONING_EFFORT": "minimal",
                "OPENROUTER_REASONING_MAX_TOKENS": "64",
            },
            clear=True,
        ):
            llm = LLMService(backend="openrouter", model="deepseek/deepseek-v3.2")
            body = llm._extra_body()
            assert body is not None
            self.assertEqual(body["reasoning"]["max_tokens"], 64)
            self.assertNotIn("effort", body["reasoning"])


if __name__ == "__main__":
    unittest.main()
