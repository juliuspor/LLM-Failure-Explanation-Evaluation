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

        # Handle negative zero: we must output -0.0 (or -0) to preserve sign.
        if self.is_negative_zero(x):
            # Use str(x) to get '-0.0' (or '-0' depending on Python's representation).
            # But we want a compact representation: if integer branch would output "0",
            # we need to output "-0". However, note that in JavaScript, -0 is a valid number.
            # We'll output "-0" if the integer branch would have output "0".
            # However, we also need to consider scientific notation? For -0, no.
            # So we can just output "-0". But to be consistent with the integer branch,
            # we should output "-0" (without decimal). However, the original test expects "-0.0".
            # The test likely expects "-0.0" because str(-0.0) in Python is '-0.0'.
            # Let's use str(x) to get the exact representation.
            # But note: str(-0.0) in Python gives '-0.0', which is fine.
            # However, the integer branch would output "0" for 0.0, but for negative zero we want "-0.0".
            # So we should treat negative zero as a special case and output "-0.0".
            # Alternatively, we could output "-0" but the test expects "-0.0".
            # Since the bug is about losing the negative sign, we can simply output str(x).
            # But note: the integer branch also does scientific notation for large numbers.
            # Negative zero is not large, so we can just output str(x).
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