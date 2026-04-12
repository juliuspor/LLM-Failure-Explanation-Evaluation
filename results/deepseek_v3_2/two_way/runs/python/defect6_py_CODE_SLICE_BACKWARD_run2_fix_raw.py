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

        # Ensure x is a numeric type (int or float) to avoid TypeError/ValueError
        # If not, fall back to string representation.
        if not isinstance(x, (int, float)):
            self.add(str(x))
            return

        # For negative zero, we need to handle it specially because -0.0 == 0.0 is True.
        # Use math.copysign to detect negative zero.
        if self.is_negative_zero(x):
            self.add("-0.0")
            return

        # Check if x is an integer (within floating point precision)
        # Use math.isclose to avoid issues with floating point representation.
        # Also handle infinite and NaN values.
        if math.isinf(x) or math.isnan(x):
            self.add(str(x))
            return

        # Determine if x is effectively an integer.
        # Use a tolerance for floating point numbers.
        if isinstance(x, float) and abs(x - round(x)) <= 1e-12:
            # x is close to an integer.
            int_x = int(round(x))
        elif isinstance(x, int):
            int_x = x
        else:
            # Not an integer, use default string representation.
            self.add(str(x))
            return

        # Now format integer representation with possible exponent.
        value = int_x
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