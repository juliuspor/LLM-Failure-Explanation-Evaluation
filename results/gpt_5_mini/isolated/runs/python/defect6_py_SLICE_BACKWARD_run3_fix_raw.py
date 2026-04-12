def add_number(self, x: float):
    # Defensive: ensure x is a numeric value before using numeric-only functions.
    # If x is not a number, just append its string representation.
    if not isinstance(x, (int, float)):
        self.add(str(x))
        return

    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle integers (including floats that are whole numbers) and exclude
    # infinities/NaN from integer handling.
    try:
        is_inf = math.isinf(x)
        is_nan = math.isnan(x)
    except TypeError:
        # In case an unexpected type slips through, fall back to string.
        self.add(str(x))
        return

    if not is_inf and not is_nan and x == int(x):
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
        # For floats that are not whole numbers or for NaN/inf, just use str(x).
        self.add(str(x))
