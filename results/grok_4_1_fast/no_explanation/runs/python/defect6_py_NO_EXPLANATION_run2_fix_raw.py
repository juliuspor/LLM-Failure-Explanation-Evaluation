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
            self.append(" ")

        if self.is_negative_zero(x):
            self.append("-0")
            return

        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            value = int(x)
            if abs(x) >= 100:
                exp = int(math.floor(math.log10(abs(x))))
                mantissa = value // (10 ** exp)
                if exp > 2:
                    self.append(str(mantissa) + "E" + str(exp))
                    return
            self.append(str(value))
        else:
            self.append(str(x))