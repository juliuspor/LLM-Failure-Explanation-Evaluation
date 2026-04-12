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
            # Remove trailing zeros from mantissa and count them in exp, but
            # only while reconstructing the value equals the original value.
            while mantissa % 10 == 0 and mantissa != 0:
                # If we removed one zero, the reconstructed value would be
                # (mantissa // 10) * (10 ** (exp + 1)). Compare to original.
                candidate_mantissa = mantissa // 10
                candidate_value = candidate_mantissa * (10 ** (exp + 1))
                if candidate_value == value:
                    mantissa = candidate_mantissa
                    exp += 1
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))