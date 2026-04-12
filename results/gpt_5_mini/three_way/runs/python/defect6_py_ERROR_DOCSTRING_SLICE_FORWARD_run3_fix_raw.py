def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Preserve negative zero: detect sign bit before any int conversion
    is_neg_zero = self.is_negative_zero(x)

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        # If it's negative zero, avoid converting to int since that loses the sign.
        if is_neg_zero:
            # Use float string to preserve '-0.0'
            self.add(str(x))
            return

        value = int(x)
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            while mantissa % 10 == 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == value:
                    mantissa //= 10
                    exp += 1
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # Non-integer floats (including negative zero handled above) — use
        # Python's str to preserve representation such as '-0.0'.
        self.add(str(x))