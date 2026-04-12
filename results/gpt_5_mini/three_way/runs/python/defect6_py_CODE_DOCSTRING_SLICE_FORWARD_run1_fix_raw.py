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
        if abs(x) >= 100:
            # Preserve the original integer value to make safe divisibility checks
            original_value = value
            # Reduce trailing zeros from mantissa while ensuring that scaling back
            # by 10**(exp+1) would still equal the original value. Use modulus
            # checks to avoid large intermediate multiplications that could overflow.
            while mantissa % 10 == 0:
                next_exp = exp + 1
                # Check if original_value is divisible by 10**next_exp
                if original_value % (10 ** next_exp) == 0:
                    mantissa //= 10
                    exp = next_exp
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))