def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Preserve sign for negative zero
    is_neg = math.copysign(1.0, x) < 0

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(abs(x))
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == value:
                    mantissa //= 10
                    exp += 1
                else:
                    break

        sign = "-" if is_neg and (value == 0) else ("-" if is_neg else "")

        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            # For integers, ensure negative zero becomes -0.0 if original was -0.0
            if value == 0 and is_neg:
                # represent negative zero as -0.0
                self.add("-0.0")
            else:
                self.add(sign + str(value))
    else:
        # For non-integer floats, rely on str(x) which preserves -0.0
        self.add(str(x))