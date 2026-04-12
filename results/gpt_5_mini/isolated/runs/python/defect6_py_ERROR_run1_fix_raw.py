def add_number(self, x: float):
    # Preserve negative zero and emit compact numeric literals.
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle negative zero specially: we must keep its sign
    if self.is_negative_zero(x):
        # Emit -0 to preserve sign (as integer form)
        self.add("-0")
        return

    # If it's an integer (and not inf/nan), try compact representation
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = abs(value)
        exp = 0
        if abs(x) >= 100:
            # Remove trailing zeros from mantissa while tracking exponent,
            # but operate on absolute mantissa so sign is preserved separately.
            while mantissa != 0 and mantissa % 10 == 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break

        sign = '-' if value < 0 else ''
        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(sign + str(abs(value)))
    else:
        # For non-integers or special values, rely on Python's str(), but
        # ensure negative zero was already handled above.
        self.add(str(x))