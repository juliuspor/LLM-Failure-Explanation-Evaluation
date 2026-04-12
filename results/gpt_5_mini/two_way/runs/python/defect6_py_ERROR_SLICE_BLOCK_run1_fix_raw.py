def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Detect negative zero: x == 0.0 but has negative sign bit
    is_neg_zero = (x == 0.0 and math.copysign(1.0, x) < 0)

    if x == int(x) and not math.isinf(x) and not math.isnan(x) and not is_neg_zero:
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
        # For negative zero and other non-integer floats, use str(x) to preserve sign
        self.add(str(x))