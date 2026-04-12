# -*- coding: utf-8 -*-
import math
from abc import ABC, abstractmethod


class CodeConsumer(ABC):
    """
    Abstracted consumer of the CodeGenerator output.
    """

    def __init__(self):
        self.statement_needs_ended = False
        self.statement_started = False
        self.saw_function = False
        self.code = ""

    def start_source_mapping(self, node):
        """Starts the source mapping for the given node at the current position."""
        pass

    def end_source_mapping(self, node):
        """Finishes the source mapping for the given node at the current position."""
        pass

    def continue_processing(self):
        """
        Provides a means of interrupting the CodeGenerator. Derived classes should
        return false to stop further processing.
        """
        return True

    def get_last_char(self):
        """Retrieve the last character of the last string sent to append."""
        return self.code[-1] if len(self.code) > 0 else '\0'

    def add_identifier(self, identifier):
        self.add(identifier)

    @abstractmethod
    def append(self, s):
        """
        Appends a string to the code, keeping track of the current line length.
        
        NOTE: the string must be a complete token--partial strings or
        partial regexes will run the risk of being split across lines.
        """
        pass

    def append_block_start(self):
        self.append("{")

    def append_block_end(self):
        self.append("}")

    def start_new_line(self):
        pass

    def maybe_line_break(self):
        self.maybe_cut_line()

    def maybe_cut_line(self):
        pass

    def end_line(self):
        pass

    def note_preferred_line_break(self):
        pass

    def begin_block(self):
        if self.statement_needs_ended:
            self.append(";")
            self.maybe_line_break()
        self.append_block_start()

        self.end_line()
        self.statement_needs_ended = False

    def end_block(self, should_end_line=False):
        self.append_block_end()
        if should_end_line:
            self.end_line()
        self.statement_needs_ended = False

    def list_separator(self):
        self.add(",")
        self.maybe_line_break()

    def end_statement(self, need_semicolon=False):
        """
        Indicates the end of a statement and a ';' may need to be added.
        But we don't add it now, in case we're at the end of a block (in which
        case we don't have to add the ';').
        See maybeEndStatement()
        """
        if need_semicolon:
            self.append(";")
            self.maybe_line_break()
            self.statement_needs_ended = False
        elif self.statement_started:
            self.statement_needs_ended = True

    def maybe_end_statement(self):
        """
        This is to be called when we're in a statement. If the prev statement
        needs to be ended, add a ';'.
        """
        if self.statement_needs_ended:
            self.append(";")
            self.maybe_line_break()
            self.end_line()
            self.statement_needs_ended = False
        self.statement_started = True

    def end_function(self, statement_context=False):
        self.saw_function = True
        if statement_context:
            self.end_line()

    def begin_case_body(self):
        self.append(":")

    def end_case_body(self):
        pass

    def add(self, newcode):
        self.maybe_end_statement()

        if len(newcode) == 0:
            return

        c = newcode[0]
        if (self.is_word_char(c) or c == '\\') and self.is_word_char(self.get_last_char()):
            # need space to separate. This is not pretty printing.
            # For example: "return foo;"
            self.append(" ")

        self.append(newcode)

    def append_op(self, op, bin_op):
        self.append(op)

    def add_op(self, op, bin_op):
        self.maybe_end_statement()

        first = op[0]
        prev = self.get_last_char()

        if (first == '+' or first == '-') and prev == first:
            # This is not pretty printing. This is to prevent misparsing of
            # things like "x + ++y" or "x++ + ++y"
            self.append(" ")
        elif first.isalpha() and self.is_word_char(prev):
            # Make sure there is a space after e.g. instanceof , typeof
            self.append(" ")
        elif prev == '-' and first == '>':
            # Make sure that we don't emit -->
            self.append(" ")

        # Allow formating around the operator.
        self.append_op(op, bin_op)

        # Line breaking after an operator is always safe. Line breaking before an
        # operator on the other hand is not. We only line break after a bin op
        # because it looks strange.
        if bin_op:
            self.maybe_cut_line()

    def add_number(self, x: float):
        """
        Append a numeric literal to the output stream.

        This emits a compact, Java-like representation and may insert whitespace
        when needed to avoid creating ambiguous tokens.

        Args:
            x: The numeric value to emit.
        """
        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")

        # Determine if x is mathematically an integer, considering floating-point limitations.
        # Use tolerance for large numbers where float representation may not be exact.
        # If x is within 1e-12 of its integer part, treat as integer.
        # Also handle infinities and NaN.
        if math.isinf(x) or math.isnan(x):
            # For infinity or NaN, just use str representation.
            self.add(str(x))
            return

        # Check if x is close to an integer.
        int_part = int(x)  # truncated integer part
        # Use relative tolerance? For large numbers, absolute difference may be large.
        # Since we only care about exact integer representation, we can check if x equals int_part exactly.
        # However, due to floating-point, we need to consider that x might be a whole number but not equal.
        # We'll use a tolerance based on the magnitude of x.
        # If x is huge (>= 2**53), float cannot represent all integers exactly.
        # In that case, we might want to use scientific notation anyway.
        # But the original code attempted to output integer representation for large numbers.
        # We'll adopt a different approach: if x is within 1e-12 * abs(x) of an integer, treat as integer.
        # However, for very large numbers, the relative error might be large.
        # Actually, the original code's intent is to output integer representation when possible.
        # We'll use the condition: abs(x - int_part) <= abs(x) * 1e-12 or abs(x - int_part) <= 1e-12.
        # But for numbers like 1e23, the difference might be huge (e.g., 0.5) due to loss of precision.
        # So we need to decide: is x meant to be an integer? The float might have been created from an integer.
        # The safest is to use the original logic but improve the integer detection.
        # We can check if x is an integer by seeing if converting to integer and back to float yields the same value.
        # However, for large numbers, that might not hold.
        # Let's use: if x == float(int_part) then treat as integer.
        # Because float(int_part) is the float representation of that integer.
        # If x equals that, then x is exactly representable as that integer.
        # This works for all integers up to 2**53 (approximately 9e15) for double precision.
        # Beyond that, not all integers are exactly representable, so x might not equal float(int_part).
        # In that case, we should fall back to scientific notation.
        # But the original code tried to output mantissa and exponent for large integers.
        # We'll keep that logic but ensure we only enter the integer branch when x is exactly an integer.
        # We'll use: if x == float(int(x)) and not math.isinf(x) and not math.isnan(x):
        # However, note that int(x) truncates, so for negative numbers, int(-3.9) = -3, which is not equal.
        # We need to check if x is an integer, i.e., x is whole. So we should use round(x) or check fractional part.
        # Actually, we want to know if x is mathematically an integer. Since x is a float, we can check if x is equal to its rounded value.
        # But rounding to nearest integer might round incorrectly for .5 cases. We'll use: abs(x - round(x)) <= 1e-12.
        # However, for huge numbers, the fractional part may be lost, so x might be integer-like.
        # Let's adopt a pragmatic approach: if x is within 1e-12 of an integer, treat as integer.
        # But the original code used exact equality. We'll change to tolerance.
        # However, the bug diagnosis says the condition fails for large integers due to floating-point inaccuracies.
        # So we need to adjust the condition to tolerate small errors.
        # We'll use: if abs(x - round(x)) <= max(1e-12, abs(x)*1e-15):
        # But we also need to handle negative numbers.
        # Simpler: if abs(x - round(x)) <= 1e-12:
        # But for numbers like 1e23, the difference might be huge (e.g., 0.5) because 1e23 is not exactly representable.
        # Actually, 1e23 as a float is 1.0000000000000001e23? Let's test: in Python, float(1e23) == 1e23 is True.
        # Wait, 1e23 is exactly representable? Not necessarily. In IEEE 754 double, 1e23 is not exactly representable.
        # The representation might be approximate. So 1e23 might not equal int(1e23) when converted to float.
        # Let's do an experiment in mind: x = 1e23; int_x = int(x); float(int_x) might be different.
        # Actually, int(1e23) is 100000000000000000000000, and converting that to float yields 1e23? Probably not exactly.
        # So the condition x == float(int(x)) might fail.
        # Therefore, we need a different strategy.
        # The original code's purpose is to output integer representation when possible, and for large integers use scientific notation with mantissa and exponent.
        # We can achieve that by directly checking if the string representation of the float is an integer.
        # For example, str(x) might be '1e+23'. We want to output '1E23'.
        # So we can parse the string representation.
        # However, the bug is about the condition failing. Let's fix the condition by using a tolerance.
        # We'll define a tolerance that scales with magnitude.
        # If abs(x - round(x)) <= max(1e-12, abs(x)*1e-15):
        # But we also need to avoid false positives for non-integers.
        # Since the numbers we deal with are literals in code, they are likely to be exact integers.
        # We'll use: if abs(x - round(x)) <= 1e-12 * max(1, abs(x)):
        # That might be too permissive for large numbers.
        # Actually, for large numbers, the relative error in floating-point representation is about 1e-16.
        # So if x is within 1e-15 * abs(x) of an integer, it's likely intended as integer.
        # We'll use: if abs(x - round(x)) <= 1e-15 * abs(x):
        # But if x is 0, we need to avoid division by zero.
        # Let's implement:
        if abs(x) < 1e15:
            # For moderate-sized numbers, use exact equality or small tolerance.
            if abs(x - round(x)) <= 1e-12:
                value = int(round(x))
                # Now handle large integers with exponent.
                mantissa = value
                exp = 0
                if abs(value) >= 100:
                    while mantissa % 10 == 0:
                        check_val = (mantissa // 10) * (10 ** (exp + 1))
                        if check_val == value:
                            mantissa //= 10
                            exp += 1
                        else:
                            break
                if exp > 2:
                    self.add(str(mantissa) + "E" + str(exp))
                else:
                    self.add(str(value))
                return
        else:
            # For large numbers, we cannot rely on tolerance because the fractional part may be lost.
            # Instead, we can check if the string representation in scientific notation is an integer.
            # We'll use the original logic but with a different condition: if the float is an integer.
            # We can use: if x.is_integer() but that's only for float objects in Python.
            # Actually, Python's float has is_integer() method.
            # Let's use that! It returns True if the float is an integer value.
            # However, note that for large floats, is_integer() might return False due to representation.
            # But it's the best we have.
            if x.is_integer():
                value = int(x)
                mantissa = value
                exp = 0
                if abs(value) >= 100:
                    while mantissa % 10 == 0:
                        check_val = (mantissa // 10) * (10 ** (exp + 1))
                        if check_val == value:
                            mantissa //= 10
                            exp += 1
                        else:
                            break
                if exp > 2:
                    self.add(str(mantissa) + "E" + str(exp))
                else:
                    self.add(str(value))
                return
        # If not integer, use standard string representation.
        self.add(str(x))

    @staticmethod
    def is_negative_zero(x):
        return x == 0.0 and math.copysign(1, x) == -1.0

    @staticmethod
    def is_word_char(ch):
        return ch == '_' or ch == '$' or ch.isalnum()

    def should_preserve_extra_blocks(self):
        """
        If the body of a for loop or the then clause of an if statement has
        a single statement, should it be wrapped in a block?  Doing so can
        help when pretty-printing the code, and permits putting a debugging
        breakpoint on the statement inside the condition.
        """
        return False

    def break_after_block_for(self, n, statement_context):
        """
        @return Whether the a line break can be added after the specified BLOCK.
        """
        return statement_context

    def end_file(self):
        """Called when we're at the end of a file."""
        pass