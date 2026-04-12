from __future__ import annotations

from .study_data import Defect


WARMUP_DEFECT = Defect(
    defect_id="warmup",
    function_name="sum_positive",
    error="IndexError: list index out of range",
    ground_truth=(
        "The bug was caused by an off-by-one loop that iterated one step too far and accessed an index beyond the end of "
        "a list. After fixing, the loop bounds were corrected so indexing only occurs for valid positions."
    ),
)


WARMUP_EXPLANATIONS: dict[str, str] = {
    "A": (
        "Root cause: an off-by-one error in the loop bounds causes an out-of-range access.\n\n"
        "Why it fails: the code iterates one element past the end of the list and then tries to read values[i], which "
        "raises IndexError when i == len(values).\n\n"
        "How to fix:\n"
        "1. In sum_positive(values), change the loop to stop at len(values) (not len(values)+1).\n"
        "2. Ensure any indexing uses i where 0 <= i < len(values).\n"
        "3. Re-run the failing test to confirm the IndexError is gone."
    ),
    "B": (
        "It fails with IndexError: list index out of range. The code is trying to access a list element that does not "
        "exist."
    ),
    "C": (
        "The failure happens because the loop goes too far and ends up indexing past the end of the list. This is an "
        "off-by-one issue: the last iteration uses an index equal to the list length, which is invalid in Python. "
        "Adjust the loop bounds so the final index is len(values)-1 and the IndexError will stop occurring. "
        "Also consider adding a check before indexing."
    ),
}

