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

        sign = '-' if x < 0 else ''
        abs_value = abs(x)

        if abs_value == int(abs_value) and not math.isinf(abs_value) and not math.isnan(abs_value):
            value = int(abs_value)
            mantissa = value
            exp = 0
            if abs_value >= 100:
                while mantissa % 10 == 0:
                    check_val = (mantissa // 10) * (10 ** (exp + 1))
                    if check_val == value:
                         mantissa //= 10
                         exp += 1
                    else:
                        break
            
            if exp > 2:
                self.add(sign + str(mantissa) + "E" + str(exp))
            else:
                self.add(sign + str(value))
        else:
            self.add(str(x))