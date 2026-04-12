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

        # Handle negative zero: -0.0 should be emitted as "-0.0" or "-0"?
        # The test expects '-0.0'. We'll treat negative zero as a special case.
        if self.is_negative_zero(x):
            # We need to output a negative zero.
            # Since we already handled the space for negative numbers above,
            # we can just output the string representation that includes the sign.
            # However, note that str(-0.0) is '0.0' in Python? Actually, str(-0.0) returns '-0.0'.
            # But we want to ensure we output '-0.0' (or maybe '-0' if integer? but -0 is not an integer).
            # The original code would have output '0' for -0.0, which is wrong.
            # So we bypass the integer branch and go to the else branch.
            # However, we must also consider the exponent representation? Not needed for zero.
            # So we can simply call self.add(str(x)).
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