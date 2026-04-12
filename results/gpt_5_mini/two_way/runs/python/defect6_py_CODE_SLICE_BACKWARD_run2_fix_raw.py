def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Use float.is_integer() to check for integral floats and math.isfinite to
    # exclude inf/nan. This avoids NameError if math is not present in some env,
    # but math is available; still using math.isfinite for clarity.
    try:
        is_finite = math.isfinite(x)
    except Exception:
        # Fallback if math doesn't provide isfinite for some reason
        is_finite = not (math.isinf(x) or math.isnan(x))

    if is_finite and float(x).is_integer():
        value = int(x)
        mantissa = abs(value)
        exp = 0
        if abs(x) >= 100:
            # Strip trailing zeros from mantissa while preserving numeric value
            while mantissa != 0 and mantissa % 10 == 0:
                # compute what the value would be if we removed one trailing zero
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break

        # Restore sign for mantissa if original value was negative
        if value < 0:
            mantissa = -mantissa

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # Use repr for a compact, unambiguous float representation
        self.add(str(x))
