def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        original_value = value
        mantissa = value
        exp = 0
        # Avoid infinite loop when mantissa is 0. Only strip trailing zeros
        # while mantissa is non-zero and divisible by 10.
        if abs(x) >= 100:
            while mantissa != 0 and mantissa % 10 == 0:
                # If removing a trailing zero still represents the same
                # original value when scaled by 10**(exp+1), accept the
                # reduction. Compute check_val from the reduced mantissa and
                # prospective exponent.
                next_mantissa = mantissa // 10
                check_val = next_mantissa * (10 ** (exp + 1))
                if check_val == original_value:
                    mantissa = next_mantissa
                    exp += 1
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))