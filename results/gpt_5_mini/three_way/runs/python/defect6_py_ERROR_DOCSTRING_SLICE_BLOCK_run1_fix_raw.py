def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle integer-like values (excluding inf/nan)
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)

        # Preserve signed zero: emit -0 for negative zero
        if value == 0:
            # Emit "-0" for negative zero, otherwise "0"
            if self.is_negative_zero(x):
                self.add("-0")
            else:
                self.add("0")
            return

        mantissa = value
        exp = 0
        # Only strip trailing zeros while mantissa is non-zero
        if abs(x) >= 100:
            while mantissa != 0 and mantissa % 10 == 0:
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