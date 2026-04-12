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
            # Remove trailing zeros from mantissa while preserving the exact value
            # by increasing the exponent accordingly.
            while mantissa % 10 == 0 and mantissa != 0:
                new_mantissa = mantissa // 10
                new_exp = exp + 1
                # Reconstruct the number from new_mantissa and new_exp and
                # ensure it equals the original integer value.
                if new_mantissa * (10 ** new_exp) == value:
                    mantissa = new_mantissa
                    exp = new_exp
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))