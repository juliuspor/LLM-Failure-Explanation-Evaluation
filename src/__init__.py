"""
Core modules for LLM failure explanation evaluation.
"""

from .data import python_defects
from .llm import LLMService
from .experiment import Experiment, ContextLevel, CRITERIA_INSTRUCTIONS, parse_levels
from .evaluation import ExplanationEvaluator
from .fix import FixGenerator
from .slicing import get_context
from .utils import normalize_python_code

__all__ = [
    'python_defects',
    'LLMService',
    'Experiment',
    'ContextLevel',
    'CRITERIA_INSTRUCTIONS',
    'parse_levels',
    'ExplanationEvaluator',
    'FixGenerator',
    'get_context',
    'normalize_python_code',
]

