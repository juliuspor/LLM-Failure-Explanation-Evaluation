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
        
        # Handle negative zero: we want to output "-0.0" or "-0" etc.
        if self.is_negative_zero(x):
            # For negative zero, we need to output a minus sign.
            # The logic below for integer detection will treat -0.0 as integer 0,
            # so we must handle it before that.
            # We'll output "-0.0" (or "-0" if integer formatting would apply).
            # However, we also need to consider scientific notation for large exponents.
            # Since -0.0 is zero, we can just output "-0.0".
            # But we must also consider the case where we might want "-0E0"? Not typical.
            # We'll follow the same logic as positive zero but with a minus sign.
            # However, note that the condition x == int(x) holds for -0.0 (int(-0.0) is 0).
            # So we need to bypass the integer path.
            # We'll treat it as a non-integer to output "-0.0".
            # But we also need to consider the space insertion above: if prev is '-', we added a space.
            # That's fine.
            # We'll just output "-0.0" directly.
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