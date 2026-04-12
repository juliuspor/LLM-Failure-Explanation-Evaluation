def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Use math.isinf and math.isnan (math is imported at module level).
    try:
        is_inf = math.isinf(x)
        is_nan = math.isnan(x)
    except Exception:
        # Fallback in case x is not a float-like value
        is_inf = x == float('inf') or x == float('-inf')
        is_nan = x != x

    if x == int(x) and not is_inf and not is_nan:
        value = int(x)
        mantissa = value
        exp = 0
        # Avoid infinite loop for zero. Only trim trailing zeros for non-zero mantissa.
        if abs(x) >= 100:
            while mantissa != 0 and mantissa % 10 == 0:
                # Compute what the value would be if we removed one trailing zero
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