def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x is not None and isinstance(x, (int, float)) and x < 0 and prev == '-':
        self.add(" ")

    # Ensure x is a numeric finite value before calling int(x)
    if isinstance(x, (int, float)) and math.isfinite(x) and x == int(x):
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
        # Fallback: use str() for non-integer, non-finite, or non-numeric values
        self.add(str(x))