def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Preserve negative zero: int(-0.0) == 0 and would lose the sign.
    is_neg_zero = self.is_negative_zero(x)

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        # If it's negative zero, avoid converting to int because that loses sign.
        if is_neg_zero:
            value = 0
            mantissa = value
            exp = 0
            # treat negative zero like zero for formatting but ensure sign is shown
            if abs(x) >= 100:
                while mantissa % 10 == 0:
                    check_val = (mantissa // 10) * (10 ** (exp + 1))
                    if check_val == value:
                        mantissa //= 10
                        exp += 1
                    else:
                        break

            if exp > 2:
                # emit negative sign explicitly
                self.add("-" + str(mantissa) + "E" + str(exp))
            else:
                self.add("-0")
        else:
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
        # For non-integer floats, rely on str(x) which preserves sign for -0.0
        # but ensure negative zero is represented as '-0' rather than '-0.0' if desired.
        if is_neg_zero:
            # represent negative zero as -0.0 to be explicit about float nature
            self.add(str(x))
        else:
            self.add(str(x))