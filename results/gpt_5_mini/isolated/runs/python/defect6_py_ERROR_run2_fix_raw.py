def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle integer-valued numbers that are not inf or nan
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        # Preserve sign of zero
        if value == 0 and self.is_negative_zero(x):
            # Emit negative zero explicitly
            self.add("-0")
            return

        mantissa = abs(value)
        exp = 0
        if abs(x) >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                # Check if removing a trailing zero and shifting exponent preserves value
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break

        if exp > 2:
            # Restore sign for mantissa
            sign = '-' if x < 0 else ''
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # For non-integer or special cases, ensure negative zero preserved
        if x == 0.0 and self.is_negative_zero(x):
            self.add("-0.0" if isinstance(x, float) and ('.' in str(x) or 'e' in str(x).lower()) else "-0")
        else:
            self.add(str(x))