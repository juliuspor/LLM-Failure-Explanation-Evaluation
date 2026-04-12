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

        # Determine if x is an integer without relying on float equality.
        # Use math.isfinite to exclude inf and nan.
        if math.isfinite(x):
            # Check if x is an integer by comparing to its rounded value.
            # Use a tolerance of 1e-12 relative? Actually, we want exact integer representation.
            # Since x is a float, we can check if it's an integer by seeing if floor(x) == x.
            # However, due to floating point errors, we need to be careful.
            # We'll use the common method: abs(x - round(x)) <= abs(x) * 1e-12.
            # But for large numbers, the relative error may be larger.
            # Alternatively, we can convert to integer only if the float representation is exact.
            # Python's float.is_integer() method does exactly that.
            if x.is_integer():
                # x is an integer-valued float.
                # Convert to int safely.
                value = int(x)
                mantissa = value
                exp = 0
                # Only try to factor powers of 10 for numbers with absolute value >= 100.
                if abs(value) >= 100:
                    # Use integer arithmetic to avoid floating point errors.
                    while mantissa % 10 == 0:
                        # Check if dividing by 10 and multiplying by 10^exp+1 yields the same value.
                        # Actually, we can just keep dividing until non-zero remainder.
                        # But we need to ensure we don't overshoot: we want the largest exponent such that
                        # mantissa * 10^exp == value.
                        # We'll compute by repeatedly dividing by 10 and incrementing exp.
                        # Since we already know mantissa % 10 == 0, we can do:
                        mantissa //= 10
                        exp += 1
                if exp > 2:
                    self.add(str(mantissa) + "E" + str(exp))
                else:
                    self.add(str(value))
                return
        # For non-integer, infinite, or NaN, use default string representation.
        self.add(str(x))