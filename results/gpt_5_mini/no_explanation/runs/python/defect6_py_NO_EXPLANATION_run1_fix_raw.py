def add_number(self, x: float):
    prev = self.get_last_char()
    # Prevent misparsing of x- -4 as x--4
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle negative zero explicitly
    if self.is_negative_zero(x):
        # Emit -0
        self.add("-0")
        return

    # If x is an integer value (not inf/nan), try compact representation
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        sign = "" if value >= 0 else "-"
        mantissa = abs(value)
        exp = 0
        # Reduce trailing zeros from mantissa while preserving exact value
        if abs(value) >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                # check if mantissa * (10**exp) equals original absolute value
                if mantissa // 10 * (10 ** (exp + 1)) == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break

        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            # regular integer
            self.add(str(value))
    else:
        # For non-integers, use a string that preserves value reasonably.
        # Use repr to avoid locale issues and to keep full precision when needed.
        self.add(repr(float(x)))