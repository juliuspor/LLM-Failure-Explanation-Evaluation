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

        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            value = int(x)
            if abs(x) >= 100:
                mantissa = abs(value)
                exp = 0
                while mantissa % 10 == 0:
                    check_val = (mantissa // 10) * (10 ** (exp + 1))
                    if check_val == abs(value):
                         mantissa //= 10
                         exp += 1
                    else:
                        break
                
                sign = '-' if value < 0 else ''
                if exp > 2:
                    self.add(sign + str(mantissa) + "E" + str(exp))
                else:
                    self.add(str(value)) 
            else:
                self.add(str(value))
        else:
            self.add(str(x))