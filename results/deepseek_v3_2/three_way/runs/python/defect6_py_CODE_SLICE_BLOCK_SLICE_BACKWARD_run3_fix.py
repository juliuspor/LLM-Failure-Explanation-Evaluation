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

        # Determine if x is an integer value, considering floating-point precision.
        # Use tolerance for large numbers.
        # First, check if x is finite and not NaN.
        if math.isfinite(x):
            # Check if x is mathematically an integer.
            # Use abs(x) to handle negative numbers.
            # For large floats, we compare with the nearest integer.
            # Use a relative tolerance? Since we care about integer equality,
            # we can check if the fractional part is negligible.
            # However, for very large numbers, the fractional part may be lost.
            # Instead, we can check if rounding to integer gives back the same value.
            # But we need to avoid rounding errors causing false positives.
            # A common approach: check if floor(x) == ceil(x) within tolerance.
            # But we can also use: abs(x - round(x)) <= abs(x) * sys.float_info.epsilon * 10
            # However, we want to treat numbers like 1e23 as integers for formatting.
            # The original code used x == int(x). That fails for large integers.
            # We can use: x.is_integer() method for float.
            # But note: x.is_integer() returns True if the float is an integer value.
            # For large floats, it may still return True if the value is exactly integer.
            # However, for numbers like 1e23, float(1e23).is_integer() returns True.
            # Wait: In Python, float(1e23).is_integer() returns True because 1e23 is exactly representable? Not necessarily.
            # Actually, 1e23 is not exactly representable in binary floating point, but .is_integer() returns True if the value is integer in the mathematical sense, i.e., fractional part is zero.
            # Since floating point cannot represent fractional part for such large numbers, .is_integer() may still return True.
            # Let's test: (1e23).is_integer() -> True. So we can use that.
            # However, .is_integer() is only available for float. x is float.
            # So we can use x.is_integer().
            if x.is_integer():
                # x is an integer value.
                value = int(x)  # Convert to integer (may be huge, but Python int is arbitrary precision).
                mantissa = value
                exp = 0
                # For large integers, we want to output scientific notation if it's compact.
                # The original loop tried to factor out powers of ten.
                # We'll keep that logic but apply to the integer value.
                # However, we must be careful with negative numbers: value is negative if x<0.
                # Use abs for factoring powers of ten.
                abs_mantissa = abs(mantissa)
                if abs_mantissa >= 100:
                    # Factor out trailing zeros.
                    while abs_mantissa % 10 == 0:
                        # Check if dividing by 10 and increasing exponent gives same value.
                        # Since we are working with integers, we can compute directly.
                        # But we need to ensure we don't lose sign.
                        # We'll compute new_mantissa = mantissa // 10
                        # and new_exp = exp + 1
                        # and check if new_mantissa * (10 ** new_exp) == value.
                        # However, for large numbers, 10**new_exp may be huge, but Python can handle.
                        # Alternatively, we can check if mantissa % 10 == 0 and then divide.
                        # But we must stop when mantissa % 10 != 0.
                        # The original code had a check that might be unnecessary.
                        # We'll simplify: while mantissa % 10 == 0: mantissa //= 10; exp += 1
                        # But we need to ensure we don't factor out zeros that are not trailing? Actually, modulo 10 only checks last digit.
                        # So it's fine.
                        # However, we must handle negative mantissa: -1200 % 10 == 0? In Python, -1200 % 10 gives 0 (because remainder has sign of divisor). So it's safe.
                        # Let's implement:
                        mantissa //= 10
                        exp += 1
                        abs_mantissa = abs(mantissa)
                # Now decide format.
                if exp > 2:
                    self.add(str(mantissa) + "E" + str(exp))
                else:
                    # Reconstruct the integer from mantissa and exp? Actually, we have mantissa and exp.
                    # But if exp>0, we have factored out trailing zeros. So we need to output mantissa * 10^exp.
                    # However, if exp <=2, we output the original integer value.
                    # But we have changed mantissa and exp. So we need to reconstruct? Or we can output str(value).
                    # Simpler: we can compute the string representation of value directly.
                    # But the original code used str(value) for the else branch.
                    # We'll keep that: output str(value).
                    # However, note that we may have changed mantissa and exp. So we need to use the original value.
                    # Actually, we have value stored. So we can use that.
                    self.add(str(value))
            else:
                # x is not an integer.
                self.add(str(x))
        else:
            # x is inf or nan.
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