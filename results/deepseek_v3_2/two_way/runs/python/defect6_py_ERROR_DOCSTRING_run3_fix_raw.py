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
        elif self.is_negative_zero(x) and prev == '-':
            # If x is -0.0, we need to ensure we don't create '--'.
            # But note: x < 0 is False for -0.0, so we handle separately.
            self.add(" ")

        # Handle negative zero: we want to output '-0' or '-0.0' etc.
        if self.is_negative_zero(x):
            # For negative zero, we need to output the negative sign.
            # The rest of the formatting should follow the same logic as positive zero.
            # We'll treat it as a special case.
            # Determine if we should output as integer or float.
            # Since it's zero, we can just output '-0' if integer representation is used.
            # However, the original code would output '0' because x == int(x) is true.
            # So we override.
            # We also need to consider scientific notation? For zero, exp is irrelevant.
            # But the original code might try to output 0E0? That would be weird.
            # Let's just output '-0'.
            # But wait: what about -0.0? The test expects '-0.0'? The test failure says -0.0.
            # Actually, the test expects '-0.0' as a string? The test likely expects the exact string '-0.0'.
            # However, the function add_number is called with a float -0.0, and str(-0.0) returns '-0.0'.
            # But the original code would have used str(x) only for non-integer case.
            # Since -0.0 == int(-0.0) is True (0 == 0), it would go into the integer branch and output '0'.
            # So we need to treat negative zero specially.
            # We'll output '-0' if the integer representation is used, but we also need to consider that
            # the original code might output '0E0' for large numbers? Not for zero.
            # Let's just output str(x) for negative zero, which is '-0.0'.
            # However, we must also consider the whitespace added above.
            self.add(str(x))
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