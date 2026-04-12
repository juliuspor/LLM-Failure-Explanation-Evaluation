def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    # Treat negative zero as negative for spacing purposes.
    is_neg = (x < 0) or (x == 0.0 and math.copysign(1.0, x) < 0)
    if is_neg and prev == '-':
        self.add(" ")

    # Handle integer-valued floats specially, but preserve sign of -0.0.
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        # Preserve negative zero explicitly.
        if x == 0.0 and math.copysign(1.0, x) < 0:
            # Emit a negative zero literal.
            self.add("-0.0")
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
        self.add(str(x))