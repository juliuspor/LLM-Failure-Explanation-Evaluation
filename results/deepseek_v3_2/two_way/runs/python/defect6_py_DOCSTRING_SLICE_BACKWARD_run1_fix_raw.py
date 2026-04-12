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

        # Check if x is an integer value (within floating point precision)
        # Use math.isfinite to exclude inf and nan.
        if math.isfinite(x) and abs(x - round(x)) <= 1e-12 * max(1.0, abs(x)):
            # x is effectively an integer
            value = int(round(x))  # round to nearest integer, handles -0.5 etc.
            # But we need to preserve sign for zero: -0.0 should be emitted as -0?
            # However, Python's int conversion of -0.0 gives 0.
            # We'll handle negative zero separately.
            if self.is_negative_zero(x):
                self.add("-0")
                return
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
        else:
            self.add(str(x))