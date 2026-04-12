def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Emit integer-like numbers without decimal if it's an exact integer and not inf/nan
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        abs_value = abs(value)
        mantissa = abs_value
        exp = 0
        # For large numbers, try to factor out powers of 10 to emit in E notation
        if abs_value >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                mantissa //= 10
                exp += 1
        # Emit with exponent if it's sufficiently large
        if exp > 2:
            # restore sign if needed
            sign = "-" if value < 0 else ""
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # Non-integer or special floats: emit default Python repr
        self.add(str(x))