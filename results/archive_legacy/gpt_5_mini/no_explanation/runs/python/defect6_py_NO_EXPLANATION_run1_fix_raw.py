def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle integers (including large ints) that are exact
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        if value == 0:
            # Preserve sign for negative zero? Python int( -0.0 ) == 0, negative zero handled separately
            self.add(str(value))
            return

        sign = '-' if value < 0 else ''
        mantissa = abs(value)
        exp = 0
        # Remove trailing zeros from mantissa, counting exponent
        while mantissa % 10 == 0:
            mantissa //= 10
            exp += 1

        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # Non-integers or special floats
        self.add(str(x))