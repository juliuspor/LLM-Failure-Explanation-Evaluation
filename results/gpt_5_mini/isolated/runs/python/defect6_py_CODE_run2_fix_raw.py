def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        # Only try to factor powers of 10 when magnitude is large enough
        if abs(value) >= 100 and value != 0:
            # Repeatedly try to remove a trailing zero while ensuring we can
            # reconstruct the original value as (mantissa_without_zero) * 10**(exp+1)
            while True:
                candidate = mantissa // 10
                if candidate == 0:
                    break
                check_val = candidate * (10 ** (exp + 1))
                if check_val == value:
                    mantissa = candidate
                    exp += 1
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))