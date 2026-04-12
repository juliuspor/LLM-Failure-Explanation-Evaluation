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

        # Use a tolerance for floating-point comparison to determine if x is effectively an integer.
        # We consider x an integer if it is finite, not NaN, and within a small epsilon of its integer part.
        if not math.isinf(x) and not math.isnan(x):
            # Check if x is close to an integer.
            # Use a relative epsilon scaled by the magnitude of x.
            eps = abs(x) * 1e-10
            if eps < 1e-12:
                eps = 1e-12
            closest_int = round(x)
            if abs(x - closest_int) <= eps:
                # x is effectively an integer.
                value = int(closest_int)  # Use the rounded integer.
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
        # For non-integer, infinite, or NaN values, use the default string representation.
        self.add(str(x))