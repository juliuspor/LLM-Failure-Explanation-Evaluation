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

        # Only attempt to factor out powers of 10 for sufficiently large
        # numbers to keep representations compact.
        if abs(value) >= 100 and mantissa != 0:
            # Remove trailing zeros from mantissa and count how many were removed
            while mantissa % 10 == 0:
                mantissa //= 10
                exp += 1

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # For non-integer-like floats, or special values, just use Python's
        # string representation.
        self.add(str(x))