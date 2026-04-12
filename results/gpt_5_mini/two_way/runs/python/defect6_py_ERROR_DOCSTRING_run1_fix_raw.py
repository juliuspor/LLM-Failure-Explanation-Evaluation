def add_number(self, x: float):
    prev = self.get_last_char()
    # Preserve negative zero: if x is -0.0 and previous char is '-', add a space to avoid "x--0"
    if self.is_negative_zero(x) and prev == '-':
        self.add(" ")

    # For integer-valued (but not inf/nan) numbers, try to emit compact integer form
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        # Handle negative zero specially: don't normalize -0.0 to 0
        if self.is_negative_zero(x):
            # emit a negative zero literal. Use -0 to match integer path compactness
            self.add("-0")
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
        # Non-integer path: ensure negative zero is preserved
        if self.is_negative_zero(x):
            # Use a standard floating negative zero representation
            self.add("-0.0")
        else:
            self.add(str(x))