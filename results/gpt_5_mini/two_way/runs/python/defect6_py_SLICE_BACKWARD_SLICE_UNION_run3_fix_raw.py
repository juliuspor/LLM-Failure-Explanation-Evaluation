def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle NaN and infinities explicitly
    if math.isnan(x) or math.isinf(x):
        self.add(str(x))
        return

    # Handle negative zero explicitly
    if self.is_negative_zero(x):
        self.add(str(x))
        return

    # If x is an integer-valued float
    # Avoid converting extremely large floats to int because that can be expensive
    # or error in some environments. Use a safe cutoff for direct int conversion.
    SAFE_INT_CUTOFF = 1e18

    try:
        is_int = (x == int(x))
    except Exception:
        # Fallback: if conversion to int fails, treat as non-integral for formatting
        is_int = False

    if is_int and abs(x) <= SAFE_INT_CUTOFF:
        value = int(x)
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            # Strip trailing zeros from the integer representation by dividing
            # by 10 while possible. This loop is safe because value is bounded.
            while mantissa % 10 == 0 and mantissa != 0:
                mantissa //= 10
                exp += 1

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
        return

    # For very large integer-valued floats or non-integers, fall back to a
    # compact decimal/scientific formatting using Python's formatting which
    # avoids huge integer allocations.
    # Prefer to avoid unnecessary trailing zeros in fractional part.
    s = format(x, '.15g')
    self.add(s)