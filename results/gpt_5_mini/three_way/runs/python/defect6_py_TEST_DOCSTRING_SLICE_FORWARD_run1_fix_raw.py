def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()

    # Handle negative zero explicitly to preserve the sign in output.
    if self.is_negative_zero(x):
        if prev == '-':
            self.add(" ")
        # Represent negative zero as -0.0 to make the sign explicit.
        self.add("-0.0")
        return

    if x < 0 and prev == '-':
        self.add(" ")

    # Treat only true integers (excluding infinities and NaN) other than
    # negative zero (handled above).
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
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
        self.add(str(x))