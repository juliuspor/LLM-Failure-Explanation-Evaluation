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

        # Determine if x is an integer within float precision.
        # Use math.trunc to get integer part, but also check if x is finite.
        if math.isfinite(x) and not math.isnan(x):
            # Check if x is an integer (i.e., fractional part is zero).
            # Use abs to handle negative numbers.
            if x == math.trunc(x):
                # x is an integer within float precision.
                # Convert to int for safe integer operations.
                value = int(x)
                mantissa = value
                exp = 0
                # Only try to convert to scientific notation for large magnitudes.
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
        # For non-integer, infinite, or NaN, use default string representation.
        self.add(str(x))