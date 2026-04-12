def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        # Avoid infinite loop when mantissa is 0. Only strip trailing zeros
        # for non-zero mantissa.
        if abs(x) >= 100 and mantissa != 0:
            while mantissa % 10 == 0:
                # Try removing one trailing zero and see if we can represent
                # the original value as mantissa * 10**exp.
                new_mantissa = mantissa // 10
                new_exp = exp + 1
                reconstructed = new_mantissa * (10 ** new_exp)
                if reconstructed == value:
                    mantissa = new_mantissa
                    exp = new_exp
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))