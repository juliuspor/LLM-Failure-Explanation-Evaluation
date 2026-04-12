def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle special float values first
    if math.isinf(x) or math.isnan(x):
        self.add(str(x))
        return

    # If x is an integer value (including negative integers)
    if x == int(x):
        value = int(x)
        mantissa = value
        exp = 0
        # For large absolute values try to emit in scientific-like form
        if abs(value) >= 100:
            # Remove trailing zeros from the integer mantissa
            while mantissa != 0 and mantissa % 10 == 0:
                mantissa //= 10
                exp += 1

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # Non-integer floats: emit the Python/JS-like representation
        self.add(str(x))