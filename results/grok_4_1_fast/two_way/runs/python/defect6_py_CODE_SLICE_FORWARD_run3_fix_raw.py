def add_number(self, x: float):
    """
    Append a numeric literal to the output stream.

    This emits a compact, Java-like representation and may insert whitespace
    when needed to avoid creating ambiguous tokens.

    Args:
        x: The numeric value to emit.
    """
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        if value == 0:
            self.add("0")
            return
        
        mantissa = abs(value)
        if mantissa >= 100:
            exp = int(math.log10(mantissa))
            # Count trailing zeros
            trailing_zeros = 0
            temp = mantissa
            while temp % 10 == 0:
                temp //= 10
                trailing_zeros += 1
            
            if trailing_zeros > 2:
                mantissa_str = str(mantissa // (10 ** trailing_zeros))
                if x < 0:
                    self.add("-" + mantissa_str + "E" + str(trailing_zeros))
                else:
                    self.add(mantissa_str + "E" + str(trailing_zeros))
                return
        
        self.add(str(value))
    else:
        self.add(str(x))