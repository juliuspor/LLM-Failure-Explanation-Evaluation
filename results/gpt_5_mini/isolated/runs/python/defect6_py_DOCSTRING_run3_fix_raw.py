def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle integers that are not infinite or NaN
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        sign = '-' if value < 0 else ''
        mantissa = abs(value)
        exp = 0

        # Reduce trailing zeros from mantissa and count exponent
        if mantissa != 0 and abs(x) >= 100:
            while mantissa % 10 == 0:
                mantissa //= 10
                exp += 1

        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # For non-integer or special floats, just use Python's str
        self.add(str(x))