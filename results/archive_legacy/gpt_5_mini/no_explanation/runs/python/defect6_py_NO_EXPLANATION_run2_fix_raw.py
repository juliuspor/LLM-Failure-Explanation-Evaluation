def add_number(self, x: float):
    prev = self.get_last_char()
    # prevent misparsing of x- -4 as x--4
    if x < 0 and prev == '-':
        self.add(" ")

    # Preserve negative zero as "-0" or "-0.0"? In JS, -0 is allowed; but maintain as "-0" for integers
    if self.is_negative_zero(x):
        # emit -0
        self.add("-0")
        return

    # Check for exact integer value and finite
    if math.isfinite(x) and x == int(x):
        value = int(x)
        # Try to emit compact form, possibly with exponent if many trailing zeros
        mantissa = value
        exp = 0
        # Only consider factoring powers of 10 for sufficiently large abs(value)
        if abs(value) >= 100:
            # reduce mantissa while divisible by 10 and reconstructible
            while mantissa % 10 == 0:
                # if we remove one trailing zero, new value would be mantissa//10 * 10**(exp+1)
                # compute reconstructed and compare to original value
                candidate = (mantissa // 10) * (10 ** (exp + 1))
                if candidate == value:
                    mantissa //= 10
                    exp += 1
                else:
                    break
        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        # For non-integers or non-finite values, just use Python's representation
        # For infinities and NaN, str() gives 'inf', 'nan' — keep that
        self.add(str(x))