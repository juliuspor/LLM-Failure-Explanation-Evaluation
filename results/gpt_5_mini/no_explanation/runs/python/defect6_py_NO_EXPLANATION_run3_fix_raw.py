def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle integers (including large ones) which are exactly representable
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        sign = "" if value >= 0 else "-"
        abs_val = abs(value)

        mantissa = abs_val
        exp = 0
        # Remove trailing zeros from mantissa, increasing exponent accordingly
        while mantissa != 0 and mantissa % 10 == 0:
            mantissa //= 10
            exp += 1

        if exp > 2:
            # Use scientific-style integer with uppercase E
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            # No exponent, emit the integer normally
            self.add(str(value))
    else:
        # For non-integers, including negative zero, use default string form
        # Preserve -0.0 correctly by checking sign
        if self.is_negative_zero(x):
            self.add("-0.0")
        else:
            self.add(str(x))