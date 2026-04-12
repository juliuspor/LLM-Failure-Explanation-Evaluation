# Slicing Process Documentation

This document explains the construction and logic behind the three slicing strategies used in the project: `slicing_forward`, `slicing_backward`, and `slicing_union`. These strategies are implemented in `src/slicing.py` and are designed to isolate relevant code context for defect analysis.

## 1. Slicing Backward (Dynamic)

**Purpose**: To identify the sequence of statements that actually affected the state at the point of failure during execution.

**Mechanism**: Dynamic Backward Slicing on Execution Trace.

**Construction Process**:
1.  **Execution Trace**: The system runs the failing test and captures the **set of executed lines** using `sys.settrace`. It does not store the temporal sequence, only the unique lines visited.
2.  **Seed**: The process starts from the **failure line** (the line where an exception occurred, or the last executed line if no exception was trapped), which is always included in the slice.
3.  **Dependency Analysis**:
    *   **Data Dependency**: It identifies variables used at the current line. It then looks backwards in the execution history to find the most recent definition of those variables.
    *   **Control Dependency**: It identifies control structures (like `if`, `while`, `function def`) that dictate whether the current line is executed.
4.  **Iterative Fixed-Point Algorithm**:
    *   The algorithm iterates backwards through the **sorted list of unique executed lines** (from highest line number to lowest).
    *   It maintains a set of **needed variables** (initially those used at the failure line).
    *   For each executed line, it checks:
        *   **Defines Needed Variable?** If the line defines a variable currently in the "needed" set, the line is added to the slice.
        *   **Updates Dependencies**: If a line is added to the slice, the variables *used* by that line are added to the "needed" set (to be found earlier in the trace).
        *   **Control Inclusion**: The controlling line (e.g., the `if` statement that led to this line) is automatically added to the slice.
    *   This process repeats until the slice stabilizes (no new lines or variables added).

**Result**: A subset of executed lines that causally contributed to the state at the failure line.

## 2. Slicing Forward (Static)

**Purpose**: To identify code that might be affected by the variables involved in the failure, providing context on how the failure state might propagate or be used immediately after.

**Mechanism**: Static Forward Slicing (Scoped, strictly downstream).

**Construction Process**:
1.  **Static Analysis**: Unlike backward slicing, this uses **AST (Abstract Syntax Tree)** analysis and does not rely on execution history (other than identifying the failure line).
2.  **Scope Restriction**: To prevent "taint explosion" (where the slice grows to include the entire program), the forward slice is strictly **bounded to the enclosing function** of the failure line.
3.  **Seed**: Starts analysis from the **failure line** within the identified scope.
4.  **Taint Tracking**:
    *   **Initial Taint**: Variables defined *or used* at the failure line are marked as "tracked".
    *   **Forward Scan**: The algorithm scans strictly forward from the failure line (excluding the failure line itself) to the end of the enclosing function.
5.  **Inclusion Criteria**:
    *   Any line that **uses** a currently "tracked" variable is added to the slice.
    *   **Transitive Taint**: If a line is included, any new variables **defined** at that line are added to the "tracked" set, allowing the slice to follow the data flow downstream.

**Result**: A set of lines within the same function following the failure that depend on the variables at the failure site.

## 3. Slicing Union

**Purpose**: To provide a comprehensive context that includes both the cause of the failure (backward) and the immediate local consequences or usage (forward).

**Mechanism**: Set Union.

**Construction Process**:
1.  Compute **Slicing Backward** (as described above).
2.  Compute **Slicing Forward** (as described above).
3.  **Union**: Combine the two sets of lines.
    *   `Union Slice = Backward Lines ∪ Forward Lines`

**Result**: A possibly non-contiguous set of lines covering the history leading up to the failure and the potential future data flow within the local scope.

---

### Summary Table

| Strategy | Type | Direction | Scope | Key Dependencies |
| :--- | :--- | :--- | :--- | :--- |
| **Backward** | Dynamic | Past (History) | Execution Trace | Data & Control Dependencies |
| **Forward** | Static | Future (Downstream) | Enclosing Function | Data Usage & Transitive Taint |
| **Union** | Hybrid | Bidirectional | Trace + Local Function | Combined Dependencies |
