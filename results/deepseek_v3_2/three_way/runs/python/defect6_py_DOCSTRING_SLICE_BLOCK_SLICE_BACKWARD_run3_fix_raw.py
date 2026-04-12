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

        # Check if x is an integer within floating-point precision.
        # Use tolerance to avoid precision issues for large floats.
        # Determine if x is mathematically an integer.
        # We'll consider x integer if it's finite and not NaN and the absolute difference
        # between x and the nearest integer is negligible.
        if not math.isinf(x) and not math.isnan(x):
            # For large numbers, we can check if rounding to nearest integer yields the same value.
            # Use a relative epsilon? Actually, for integer values, we can check if x is within 1e-12 of an integer.
            # But for very large numbers, the ULP may be >1, so we need to check if x is already an integer.
            # Better: try to convert to integer using int(x) and see if the float representation of that integer equals x.
            # However, due to rounding, int(x) might be off by one for large numbers.
            # Use math.floor(x+0.5) to get nearest integer.
            nearest_int = int(math.floor(x + 0.5))
            if abs(x - nearest_int) <= abs(x) * 1e-12:  # relative tolerance
                value = nearest_int
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
        # Fallback for non-integer, infinite, or NaN.
        self.add(str(x))