def add_number(self, x: float):
    # Ensure x is a numeric value (convert from string if necessary)
    try:
        x_num = float(x)
    except (TypeError, ValueError):
        raise TypeError("add_number expects a numeric value")

    prev = self.get_last_char()
    # Prevent misparsing of x- -4 as x--4
    if x_num < 0 and prev == '-':
        self.add(" ")

    # Handle exact integers (and exclude infinities/NaNs)
    if x_num == int(x_num) and not math.isinf(x_num) and not math.isnan(x_num):
        value = int(x_num)
        mantissa = value
        exp = 0
        if abs(value) >= 100:
            # Remove trailing zeros from integer and count decimal exponent
            while mantissa % 10 == 0 and mantissa != 0:
                # check whether shifting is safe (reconstructing should match)
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
        # For non-integer floats, just use a standard conversion that
        # preserves typical Python float representation.
        # Handle negative zero explicitly to preserve sign if needed.
        if self.is_negative_zero(x_num):
            self.add("-0.0")
        else:
            self.add(str(x_num))