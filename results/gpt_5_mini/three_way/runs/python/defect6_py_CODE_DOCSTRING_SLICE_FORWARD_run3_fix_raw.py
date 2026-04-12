def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle integer-like floats (no fractional part) and not inf/nan
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        # Preserve sign separately to avoid issues with negative integer division
        sign = '-' if x < 0 or (x == 0.0 and math.copysign(1.0, x) < 0) else ''
        value = abs(int(x))
        mantissa = value
        exp = 0

        # Try to strip trailing zeros from the absolute integer representation
        # Work only while mantissa is non-zero and divisible by 10.
        while mantissa != 0 and mantissa % 10 == 0:
            # Compute what the value would be if we removed one more zero
            # and scaled by the next exponent; use integer arithmetic on
            # positive numbers so // behaves as expected.
            check_val = (mantissa // 10) * (10 ** (exp + 1))
            # Compare against absolute integer value; if equal, accept reduction
            if check_val == value:
                mantissa //= 10
                exp += 1
            else:
                break

        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            # Reattach sign for the plain integer form
            self.add(sign + str(value))
    else:
        # For non-integer floats, negatives, nan, inf etc, rely on Python's
        # string conversion which is adequate for most cases. Handle negative
        # zero explicitly to preserve the sign.
        if x == 0.0 and math.copysign(1.0, x) < 0:
            # negative zero
            self.add("-0.0")
        else:
            self.add(str(x))