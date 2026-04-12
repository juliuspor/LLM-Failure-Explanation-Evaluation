def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle finite integer-valued floats specially (but not NaN/Inf)
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0

        # Factor out powers of 10 from the absolute value
        abs_m = abs(mantissa)
        while abs_m != 0 and abs_m % 10 == 0:
            abs_m //= 10
            exp += 1

        # Reapply sign to mantissa
        if mantissa < 0:
            mantissa = -abs_m
        else:
            mantissa = abs_m

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))