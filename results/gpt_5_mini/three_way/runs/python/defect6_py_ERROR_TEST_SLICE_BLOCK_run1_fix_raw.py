def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle exact integers (including signed zero) that are not inf/nan
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        # Preserve negative zero when x is -0.0
        if value == 0 and self.is_negative_zero(x):
            # represent as -0 to preserve sign for integer representation
            self.add("-0")
            return

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
        # For non-integer floats, str(x) preserves the sign of negative zero
        # in Python (prints '-0.0'), so just use it.
        self.add(str(x))