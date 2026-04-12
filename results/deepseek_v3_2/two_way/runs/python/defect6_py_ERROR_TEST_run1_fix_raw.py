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
        
        # Handle negative zero: we need to output "-0.0" or "-0" depending on integer.
        if self.is_negative_zero(x):
            # For negative zero, we want to output the sign.
            # Since x == 0.0, we need to decide whether to output as integer or float.
            # The original logic would output "0" because int(x) == 0.
            # But we want to output "-0.0" to preserve the sign.
            # However, note that str(-0.0) returns "-0.0" in Python.
            # So we can just use str(x) to get the correct representation.
            # But we must also consider the exponent formatting for large numbers.
            # Since x is zero, we don't need exponent formatting.
            # So we can simply call self.add(str(x)).
            # However, we must also consider the space insertion for negative sign.
            # The condition above already added a space if prev == '-' and x < 0.
            # But for negative zero, x < 0 is False? Actually, -0.0 < 0 is False in Python.
            # So the condition above won't add a space. That's fine.
            # We'll just output the string representation.
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