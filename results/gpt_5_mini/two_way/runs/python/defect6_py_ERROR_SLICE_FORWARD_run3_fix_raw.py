def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Preserve negative zero: don't coerce to int because int(-0.0) == 0 and loses sign
    if x == int(x) and not math.isinf(x) and not math.isnan(x) and not self.is_negative_zero(x):
        value = int(x)
        mantissa = abs(value)
        exp = 0
        if abs(x) >= 100:
            # Reduce trailing zeros from mantissa while preserving the equivalence
            while mantissa != 0 and mantissa % 10 == 0:
                # Check if removing a trailing zero and increasing exponent keeps the same value
                # Use integer arithmetic to avoid floating point issues
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break

        if exp > 2:
            s = ("-" if value < 0 else "") + str(mantissa) + "E" + str(exp)
            self.add(s)
        else:
            self.add(str(value))
    else:
        # For negative zero and all non-integral numbers, use str(x) which preserves '-0.0'
        self.add(str(x))