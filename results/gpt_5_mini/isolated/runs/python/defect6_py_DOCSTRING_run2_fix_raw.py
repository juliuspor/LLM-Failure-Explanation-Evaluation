def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle NaN and infinities explicitly
    if math.isinf(x) or math.isnan(x):
        self.add(str(x))
        return

    # Handle negative zero distinctly
    if self.is_negative_zero(x):
        self.add("-0")
        return

    # If x is an integer-valued float, attempt compact representation
    if x == int(x):
        value = int(x)

        # Only try scientific-style shortening for sufficiently large absolute values
        if abs(value) >= 100:
            mantissa = value
            exp = 0
            # Reduce by factors of 10 while exactly divisible
            while mantissa % 10 == 0:
                mantissa //= 10
                exp += 1

            if exp > 2:
                self.add(str(mantissa) + "E" + str(exp))
                return

        # Fallback: plain integer string
        self.add(str(value))
    else:
        # Non-integer floats: use default string representation
        self.add(str(x))