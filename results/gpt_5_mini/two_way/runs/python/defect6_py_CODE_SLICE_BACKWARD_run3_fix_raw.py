def add_number(self, x: float):
    # Prevent misparsing of x- -4 as x--4
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle special float cases (NaN/Inf) and non-integers
    if math.isinf(x) or math.isnan(x) or x != int(x):
        # Use Python's string for non-integer floats
        self.add(str(x))
        return

    # At this point x is a finite integer value
    value = int(x)
    mantissa = abs(value)
    sign = '-' if value < 0 else ''

    # Reduce trailing zeros from mantissa and count exponent
    exp = 0
    if abs(value) >= 100 and mantissa != 0:
        while mantissa % 10 == 0:
            # If removing a trailing zero and reconstructing yields the same
            # original value when scaled back, accept the removal.
            next_mantissa = mantissa // 10
            if next_mantissa * (10 ** (exp + 1)) == abs(value):
                mantissa = next_mantissa
                exp += 1
            else:
                break

    if exp > 2:
        self.add(sign + str(mantissa) + "E" + str(exp))
    else:
        self.add(str(value))