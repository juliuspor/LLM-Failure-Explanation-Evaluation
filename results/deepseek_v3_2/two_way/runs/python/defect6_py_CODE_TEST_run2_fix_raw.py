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

        # Handle negative zero: -0.0 should be emitted as '-0.0' or '-0'.
        if self.is_negative_zero(x):
            # We need to output a negative zero.
            # Determine if we should output as integer or float.
            # Since -0.0 == 0.0, we cannot rely on x == int(x).
            # We'll output '-0.0' to preserve the sign and float nature.
            # However, if the previous character is '-', we already added a space.
            # We'll just add '-0.0' as a string.
            self.add('-0.0')
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