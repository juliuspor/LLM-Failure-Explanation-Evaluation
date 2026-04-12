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

        # Determine if x is an integer (within floating-point precision)
        # Use math.isclose to account for precision issues.
        # Also handle special cases: inf, nan, negative zero.
        if math.isinf(x) or math.isnan(x):
            # For infinity or NaN, just use string representation.
            self.add(str(x))
            return

        # Check if x is an integer. We consider it an integer if it's within a small epsilon of its rounded value.
        # However, for very large floats, the integer representation may be exact if the float is a whole number.
        # We'll use the fact that float.as_integer_ratio can help, but simpler: compare to nearest integer.
        # Use a relative tolerance? For integer values up to 1e15, float representation is exact.
        # For larger numbers, we may want to avoid the integer path if the float cannot represent it exactly.
        # We'll use: if abs(x) <= 1e15, then we can safely check integer equality.
        # Otherwise, we need to be careful.
        # Actually, we can use: x.is_integer() method of float, which returns True if the float is an integer value.
        # This method works for all floats, including large ones, because it checks the exponent.
        if x.is_integer():
            # x is mathematically an integer, but may be large.
            # Convert to int without loss of precision? int(x) may raise OverflowError for huge floats.
            # However, if x.is_integer() is True, then x is exactly representable as an integer? Not necessarily.
            # For large floats, the integer may be beyond 53 bits of precision, but x.is_integer() still True.
            # We'll try to convert to int, but if it's too large, we'll fall back to string representation.
            try:
                value = int(x)
            except OverflowError:
                # If x is too large to convert to int, we'll use scientific notation via str(x).
                # But str(x) might produce scientific notation, which is acceptable.
                self.add(str(x))
                return
            # Now we have an integer value.
            # We want to output it in a compact form, possibly using scientific notation for large numbers.
            # The original code attempted to factor out trailing zeros.
            # We'll replicate that logic but using integer arithmetic on 'value'.
            mantissa = value
            exp = 0
            if abs(value) >= 100:
                while mantissa % 10 == 0:
                    # Check if dividing by 10 and increasing exponent gives the same value.
                    # Since we are using integer arithmetic, we can compute directly.
                    # We want to ensure that mantissa // 10 * 10**(exp+1) == value.
                    # But note: we are already dividing mantissa by 10, so we need to adjust exponent.
                    # Actually, the original code had a bug: it recalculated check_val incorrectly.
                    # Let's fix: we want to see if we can factor out a factor of 10.
                    # We can do: if (mantissa // 10) * (10 ** (exp + 1)) == value.
                    # But since we are iteratively dividing mantissa, we can just keep dividing until non-zero digit.
                    # However, we must ensure that the overall number remains the same.
                    # Since we are using integer arithmetic, we can simply count trailing zeros.
                    # Let's compute the number of trailing zeros of 'value'.
                    # But we want to factor out only if the resulting exponent is >2? Actually the original code only factors if exp>2.
                    # We'll change the approach: count trailing zeros, then decide.
                    # However, we must be careful: for numbers like 1000, we want to output 1000, not 1E3? The original code only uses scientific notation if exp>2.
                    # So we'll count trailing zeros, but we'll only factor out if the exponent after factoring is >2.
                    # Let's compute the number of trailing zeros safely.
                    # We'll do a loop similar to original but with integer arithmetic.
                    # The condition mantissa % 10 == 0 is true, so we can divide.
                    # But we need to check that after dividing, the number with increased exponent equals the original.
                    # Since we are dividing by 10, we must multiply by 10 elsewhere. We'll keep track of exponent.
                    # Actually, we can just compute the number of trailing zeros without loop? But loop is fine.
                    # We'll do:
                    #   temp_mantissa = mantissa // 10
                    #   temp_exp = exp + 1
                    #   if temp_mantissa * (10 ** temp_exp) == value:
                    #        mantissa = temp_mantissa
                    #        exp = temp_exp
                    #   else:
                    #        break
                    # However, note that 10**temp_exp may become huge for large exponents, causing performance issues.
                    # Instead, we can note that if mantissa % 10 == 0, then dividing by 10 and increasing exponent by 1 always yields the same number.
                    # Because: mantissa = value / (10**exp). If mantissa % 10 == 0, then value is divisible by 10**(exp+1).
                    # So we can safely divide. The original check was unnecessary.
                    # Therefore, we can simply count trailing zeros of mantissa.
                    # Let's break the loop when mantissa % 10 != 0.
                    # But we also want to stop if the exponent becomes too large? We'll just continue until no more trailing zeros.
                    # However, we must ensure we don't factor out all zeros: we want to keep at least two digits? Actually the original code only factors if exp>2.
                    # We'll factor out all trailing zeros, then later decide whether to use scientific notation based on exp.
                    # So we'll do:
                    mantissa //= 10
                    exp += 1
                # After the loop, we have factored out all trailing zeros.
            # Now decide on representation.
            if exp > 2:
                self.add(str(mantissa) + "E" + str(exp))
            else:
                # We need to output the original integer value, but we have factored out zeros.
                # So we must reconstruct: mantissa * 10**exp.
                # However, if we factored out zeros, we need to output the original number? Actually we want to output the compact representation.
                # The original code used mantissa and exp only if exp>2, otherwise it used str(value).
                # So we should use str(value) for exp<=2.
                self.add(str(value))
        else:
            # x is not an integer.
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