def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if not math.isinf(x) and not math.isnan(x) and x == int(x):
        value = int(x)
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            # Strip trailing zeros from mantissa and count how many tens we removed
            while mantissa % 10 == 0 and mantissa != 0:
                # If we remove one trailing zero from mantissa, that corresponds
                # to increasing the exponent by 1 (i.e., value = mantissa * 10**exp)
                mantissa //= 10
                exp += 1

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))