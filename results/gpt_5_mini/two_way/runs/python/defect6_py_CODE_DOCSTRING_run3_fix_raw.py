def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle special floats explicitly
    if not hasattr(math, 'isinf') or not hasattr(math, 'isnan'):
        is_inf = False
        is_nan = False
    else:
        is_inf = math.isinf(x)
        is_nan = math.isnan(x)

    # Integer-valued floats (and not inf/nan)
    if x == int(x) and not is_inf and not is_nan:
        value = int(x)
        sign = -1 if value < 0 else 1
        mantissa = abs(value)
        exp = 0
        if mantissa >= 100:
            # Strip trailing zeros from the absolute mantissa
            while mantissa % 10 == 0 and mantissa != 0:
                # compute reconstructed value from candidate mantissa and exponent
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break

        if exp > 2:
            # restore sign on mantissa if needed
            if sign < 0:
                self.add("-" + str(mantissa) + "E" + str(exp))
            else:
                self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))