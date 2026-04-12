def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle negative zero specially
    if self.is_negative_zero(x):
        self.add("-0")
        return

    # If x is an integer (and not inf/nan), format without decimal point
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        # Reduce trailing zeros from mantissa while preserving original value
        if abs(value) >= 100:
            while mantissa % 10 == 0:
                next_mantissa = mantissa // 10
                # Check whether next_mantissa * 10**(exp+1) still equals value
                if next_mantissa * (10 ** (exp + 1)) == value:
                    mantissa = next_mantissa
                    exp += 1
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # For non-integer floats, just use standard repr to avoid locale issues
        self.add(str(x))