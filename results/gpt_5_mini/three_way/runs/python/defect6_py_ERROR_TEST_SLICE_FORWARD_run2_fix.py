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
        # Preserve negative zero explicitly
        if CodeConsumer.is_negative_zero(x):
            self.add("-0.0")
            return

        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")

        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            value = int(x)
            mantissa = value
            exp = 0
            if abs(x) >= 100:
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
        else:
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