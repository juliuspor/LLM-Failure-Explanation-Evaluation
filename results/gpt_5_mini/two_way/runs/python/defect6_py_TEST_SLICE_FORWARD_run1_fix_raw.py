def add_number(self, x: float):
    # Ensure negative zero is preserved
    if self.is_negative_zero(x):
        # Emit a canonical negative zero representation
        self.add("-0.0")
        return

    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Use is_integer to detect integer-valued floats without converting to int
    if (not math.isinf(x)) and (not math.isnan(x)) and float(x).is_integer():
        value = int(x)  # safe now; sign handled above for -0.0
        mantissa = abs(value)
        exp = 0
        if abs(x) >= 100:
            # Strip trailing zeros from mantissa while tracking exponent
            while mantissa % 10 == 0 and mantissa != 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break

        sign = "-" if value < 0 else ""
        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(sign + str(abs(value)))
    else:
        # For non-integers or infinities/nan, use Python's default formatting which
        # preserves sign (negative zero handled above).
        self.add(str(x))
