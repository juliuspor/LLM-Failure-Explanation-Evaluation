def add_number(self, x: float):
    prev = self.get_last_char()
    # Avoid misparsing of x- -4 as x--4
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle -0.0 specially if needed
    if self.is_negative_zero(x):
        # Represent negative zero as '-0'
        self.add("-0")
        return

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        # Only attempt to factor powers of 10 from the absolute mantissa
        abs_mant = abs(mantissa)
        if abs_mant >= 100:
            while abs_mant % 10 == 0:
                # Check if removing one trailing zero and increasing exponent
                # still reconstructs the original value
                candidate = abs_mant // 10
                if candidate * (10 ** (exp + 1)) == abs_mant * (10 ** exp):
                    # This check is equivalent to candidate * 10^(exp+1) == value's absolute
                    # but simpler is to just update mantissa and exp based on abs
                    abs_mant = candidate
                    exp += 1
                else:
                    break
            # Restore sign to mantissa
            mantissa = abs_mant if value >= 0 else -abs_mant

        if exp > 2:
            # Use scientific-like notation with uppercase E
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))