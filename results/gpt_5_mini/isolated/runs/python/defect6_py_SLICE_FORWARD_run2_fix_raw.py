def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle negative zero explicitly
    if self.is_negative_zero(x):
        self.add("-0")
        return

    # If x is an exact integer (and not inf/nan), format specially
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = abs(value)
        exp = 0

        # Handle zero as special case
        if mantissa == 0:
            self.add("0")
            return

        # Remove trailing zeros to form mantissa * 10^exp
        while mantissa % 10 == 0:
            mantissa //= 10
            exp += 1

        if exp > 2:
            # Preserve sign for the mantissa
            sign = "-" if value < 0 else ""
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # For non-integers or special floats, just use Python's repr
        # to get a compact representation, but avoid '-0.0'
        s = repr(x)
        if s == '-0.0':
            s = '0.0'
        self.add(s)