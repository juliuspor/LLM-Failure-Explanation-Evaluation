def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle negative zero explicitly
    if self.is_negative_zero(x):
        self.add("-0")
        return

    # Finite integer values
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = abs(value)
        exp = 0

        # Reduce trailing zeros for large integers (>=100)
        if mantissa >= 100:
            # Only divide while mantissa is divisible by 10
            while mantissa != 0 and mantissa % 10 == 0:
                # Check that reconstructing gives the original absolute value
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break

        # Restore sign to mantissa if original was negative
        if value < 0:
            mantissa = -mantissa

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # Non-integer or special floats
        self.add(str(x))