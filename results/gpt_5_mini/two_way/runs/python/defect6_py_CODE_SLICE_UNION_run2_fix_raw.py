def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle non-finite values first to avoid int() on inf/nan
    if math.isinf(x) or math.isnan(x):
        self.add(str(x))
        return

    # If x is an integer value, try to produce compact representation
    if x == int(x):
        value = int(x)
        mantissa = value
        exp = 0

        if abs(x) >= 100:
            # Strip trailing zeros from mantissa while tracking exponent
            while mantissa != 0 and mantissa % 10 == 0:
                # compute what the value would be if we removed another 10
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