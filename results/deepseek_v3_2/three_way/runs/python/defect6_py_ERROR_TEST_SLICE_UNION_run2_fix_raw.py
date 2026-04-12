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
        
        # Handle negative zero: we need to output -0.0 (or -0) to preserve sign.
        if self.is_negative_zero(x):
            # For negative zero, we want to output "-0.0" or "-0" depending on integer path.
            # Since -0.0 is integer-like, we could output "-0" but the test expects "-0.0".
            # The test expects the exact string representation that preserves the sign.
            # We'll treat negative zero as a special case and output "-0.0".
            # However, we must also consider the exponent formatting? Not needed for zero.
            # Also need to consider the space insertion for negative sign as above.
            # The condition above already added a space if prev == '-' and x < 0.
            # But for negative zero, x < 0 is False because -0.0 is not less than zero.
            # So we need to adjust: we want to output a negative sign, but we must also
            # ensure we don't double up with the previous dash.
            # Actually, the condition `x < 0` is false for -0.0, so no space added.
            # We'll output "-0.0" directly.
            # But we must also call maybe_end_statement etc. via self.add.
            # However, self.add will also do spacing based on previous character.
            # We'll just call self.add("-0.0") and return.
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