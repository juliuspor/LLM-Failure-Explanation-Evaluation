import re
from pydantic import BaseModel, Field
from .llm import LLMService


# Thresholds for binary conversion
READABILITY_THRESHOLD = 12.0      # C1: Flesch-Kincaid <= 12 = readable (high school level)
CONTEXT_THRESHOLD = 2            # C5: >= 2 code references = contextual



class EvaluationScores(BaseModel):
    """Structured output for LLM-based evaluation criteria."""
    C2: int = Field(..., ge=0, le=1, description="Problem Identification: 1 if Root Cause is identified (FAIL if only symptom described), 0 otherwise")
    C3: int = Field(..., ge=0, le=1, description="Clarity: 1 if explanation has a complete, gap-free causal chain (Why explains What), 0 otherwise")
    C4: int = Field(..., ge=0, le=1, description="Actionability: 1 if explanation provides a concrete, numbered list of steps (1., 2., 3.) to fix the issue, 0 otherwise")
    C6: int = Field(..., ge=0, le=1, description="Brevity: 1 if concise and information-dense, 0 if overly verbose/rambling or too sparse")
    reasoning: str = Field(..., description="Brief explanation of why these scores were assigned.")


class ExplanationEvaluator:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def evaluate(self, explanation: str, ground_truth: str) -> dict:
        """Evaluates the explanation based on C1-C6 criteria. All binary (0/1)."""
        # Raw scores
        c1_raw = self._calculate_flesch_kincaid(explanation)
        c5_raw = self._count_code_references(explanation)
        llm_scores = self._evaluate_with_llm(explanation, ground_truth)
        
        # Convert to binary
        return {
            "C1_Readability": 1 if c1_raw <= READABILITY_THRESHOLD else 0,
            "C2_Problem_Identification": llm_scores.C2,  # binary (0/1)
            "C3_Explanation_Clarity": llm_scores.C3,     # binary (0/1)
            "C4_Actionability": llm_scores.C4,           # binary (0/1)
            "C5_Contextual_Adequacy": 1 if c5_raw >= CONTEXT_THRESHOLD else 0,
            "C6_Brevity": llm_scores.C6,
            "reasoning": llm_scores.reasoning
        }

    def _calculate_flesch_kincaid(self, text: str) -> float:
        """Flesch-Kincaid Grade Level."""
        if not text.strip():
            return 0.0
            
        words = re.findall(r'\b\w+\b', text)
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        
        num_words = len(words)
        num_sentences = max(1, len(sentences))
        
        def count_syllables(word):
            word = word.lower()
            count = 0
            vowels = "aeiouy"
            if word[0] in vowels:
                count += 1
            for i in range(1, len(word)):
                if word[i] in vowels and word[i - 1] not in vowels:
                    count += 1
            if word.endswith("e"):
                count -= 1
            return max(1, count)

        num_syllables = sum(count_syllables(w) for w in words)
        
        if num_words == 0:
            return 0.0

        score = 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59
        return round(score, 2)

    def _count_code_references(self, text: str) -> int:
        """Counts explicit references to code locations."""
        line_refs = len(re.findall(r'\b(line|L)\s*\d+', text, re.IGNORECASE))
        method_refs = len(re.findall(r'\b[a-zA-Z0-9_]+\(\)', text))
        return line_refs + method_refs

    def _evaluate_with_llm(self, explanation: str, ground_truth: str) -> EvaluationScores:
        """Uses LLM to evaluate C2, C3, C4, C6 with structured output."""
        prompt = f"""Evaluate the following software failure explanation against the ground truth.

Ground Truth: "{ground_truth}"

Explanation: "{explanation}"

[OUTPUT FORMAT]
Return ONLY a valid JSON object with exactly these keys:
{{"C2": 0, "C3": 0, "C4": 0, "C6": 0, "reasoning": "..."}}

Rules:
- Output exactly one top-level JSON object (no surrounding text).
- Use exactly the keys: C2, C3, C4, C6, reasoning (no extra keys).
- C2/C3/C4/C6 must be integers 0 or 1.
- reasoning must be a JSON string. If you need newlines, write "\\n" (do not include literal newlines).
- Do NOT output Markdown, tables, or code fences.

Criteria:
- C2 (Problem Identification): 1 if the explanation correctly identifies the ROOT CAUSE. 
  * STRICT REJECTION: If the explanation only restates the error message (symptom) without explaining WHY it happened, score 0.
- C3 (Explanation Clarity): 1 if the explanation provides a complete CAUSAL CHAIN.
  * STRICT REJECTION: The "Why" must explicitly explain how the code logic led to the failure. If the explanation is circular, gaps exist, or it just says "it failed", score 0.
- C4 (Actionability): 1 if the explanation provides a concrete, numbered list of steps (1., 2., 3.) that explicitly reference specific variable names, function names, or line numbers found in the code.
  * STRICT REJECTION: Score 0 for generic advice like "check the index" or "fix the loop" if the specific variable name (e.g., `i`, `max_val`) is not mentioned in the steps.
- C6 (Brevity): 1 if the explanation is concise and information-dense (little repetition, mostly useful details). 0 if it is overly verbose/rambling OR too sparse to be useful.
- reasoning: Explain why you assigned these scores."""

        try:
            return self.llm.generate_structured(prompt, EvaluationScores)
        except Exception as e:
            print(f"Evaluation error: {e}")
            return EvaluationScores(C2=0, C3=0, C4=0, C6=0, reasoning=f"Error: {e}")
