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

        # Check if x is integral, accounting for floating-point precision
        # Use tolerance for large floats where int conversion may lose precision
        try:
            int_x = int(x)
            # Check if x is effectively integral: difference less than 1e-12 relative
            if abs(x - int_x) <= max(1e-12 * abs(x), 1e-12) and not math.isinf(x) and not math.isnan(x):
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
            else:
                self.add(str(x))
        except (OverflowError, ValueError):
            # Fallback for values that cannot be safely converted to int
            self.add(str(x))