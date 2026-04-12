def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    try:
        negative_check = (x < 0)
    except TypeError:
        # If x isn't numeric, fall back to default string conversion.
        self.add(str(x))
        return

    if negative_check and prev == '-':
        self.add(" ")

    # Import the needed functions locally to avoid relying on module-level imports.
    from math import isinf, isnan

    try:
        integral = int(x)
    except (TypeError, ValueError, OverflowError):
        # Can't convert to int reliably, fall back to generic string.
        self.add(str(x))
        return

    if x == integral and not isinf(x) and not isnan(x):
        value = integral
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

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))