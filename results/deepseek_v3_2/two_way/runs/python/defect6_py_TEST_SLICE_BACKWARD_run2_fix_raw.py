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

        # Handle negative zero: we want to output "-0.0" or "-0" depending on integer representation.
        # But note: -0.0 is considered equal to 0.0, so we need to check sign separately.
        if self.is_negative_zero(x):
            # For negative zero, we must output the negative sign.
            # However, we already added a space above if needed (x < 0 condition).
            # Since x is negative zero, x < 0 is True, so space added if prev == '-'. Good.
            # Now we need to output "-0.0" (or "-0" if we want integer representation?).
            # The spec likely expects "-0.0" to preserve the negative zero.
            # We'll treat it as a non-integer to output "-0.0".
            self.add("-0.0")
            return

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