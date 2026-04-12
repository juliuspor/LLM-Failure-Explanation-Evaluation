def add_number(self, x: float):
    prev = self.get_last_char()
    # avoid misparsing x--4
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle exact integers (but not inf/nan)
    if x == int(x) and not math.isinf(x) and not math.isnan(x) and not self.is_negative_zero(x):
        value = int(x)
        mantissa = abs(value)
        exp = 0
        # factor out trailing zeros to potentially use scientific notation
        if mantissa >= 100:
            while mantissa % 10 == 0:
                mantissa //= 10
                exp += 1
        # restore sign to mantissa when formatting with no exponent
        if exp > 2:
            # use uppercase E and include sign if negative
            sign = '-' if value < 0 else ''
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # For non-integers or special cases, just use python str()
        # Preserve negative zero representation if present
        if self.is_negative_zero(x):
            self.add("-0.0")
        else:
            self.add(str(x))