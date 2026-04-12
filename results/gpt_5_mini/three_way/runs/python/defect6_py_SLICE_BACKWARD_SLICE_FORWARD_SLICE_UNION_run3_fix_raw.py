def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            # Remove trailing zeros from mantissa and count how many were removed
            while mantissa % 10 == 0 and mantissa != 0:
                # If we removed one trailing zero, that corresponds to multiplying
                # the exponent by 10 (i.e., incrementing exp by 1).
                mantissa //= 10
                exp += 1

            # Verify that reconstructing mantissa * 10**exp equals original value
            # If not, roll back the last removal(s). This preserves exact integer values.
            check_val = mantissa * (10 ** exp)
            while check_val != value and exp > 0:
                # undo one step
                mantissa *= 10
                exp -= 1
                check_val = mantissa * (10 ** exp)

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))