def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    # ensure we insert a space if negative number follows a minus sign
    if math.copysign(1.0, x) < 0 and prev == '-':
        self.add(" ")

    # Handle integers (including negative zero) specially for compact representation
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        # Distinguish negative zero
        if self.is_negative_zero(x):
            # Emit -0.0 to preserve sign of negative zero
            self.add("-0.0")
            return

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
        # Non-integer or special cases: preserve negative zero here as well
        if self.is_negative_zero(x):
            self.add("-0.0")
        else:
            self.add(str(x))