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

        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            value = int(x)
            s = str(value).rstrip('0')
            num_zeros = len(str(value)) - len(s)
            if num_zeros > 2:
                self.add(s + 'E' + str(num_zeros))
            else:
                self.add(str(value))
        else:
            self.add(str(x))