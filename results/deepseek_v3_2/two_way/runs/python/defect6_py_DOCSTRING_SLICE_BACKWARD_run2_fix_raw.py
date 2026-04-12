    def add_number(self, x: float):
        """
        Append a numeric literal to the output stream.

        This emits a compact, Java-like representation and may insert whitespace
        when needed to avoid creating ambiguous tokens.

        Args:
            x: The numeric value to emit.
        """
        # Ensure x is a float for numeric operations
        try:
            x_float = float(x)
        except (ValueError, TypeError):
            # If conversion fails, treat as a string literal
            self.add(str(x))
            return

        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if x_float < 0 and prev == '-':
            self.add(" ")

        if x_float == int(x_float) and not math.isinf(x_float) and not math.isnan(x_float):
            value = int(x_float)
            mantissa = value
            exp = 0
            if abs(x_float) >= 100:
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
            self.add(str(x_float))