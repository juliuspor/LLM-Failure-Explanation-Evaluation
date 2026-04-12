def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = abs(value)
        exp = 0
        if abs(x) >= 100:
            # Strip trailing zeros from mantissa and count them as exponent
            while mantissa % 10 == 0 and mantissa != 0:
                # Check whether removing another factor of 10 and adding to
                # exponent would still represent the same value when
                # reconstructed.
                check_mant = mantissa // 10
                check_val = check_mant * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa = check_mant
                    exp += 1
                else:
                    break

        if exp > 2:
            # Restore sign for mantissa if original value was negative
            if value < 0:
                mantissa = -mantissa
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))