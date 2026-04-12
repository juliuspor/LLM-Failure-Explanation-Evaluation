def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        # Remove trailing zeros from mantissa and count how many tens we removed
        if mantissa != 0 and abs(value) >= 100:
            # Work with absolute mantissa for divisibility
            sign = -1 if mantissa < 0 else 1
            mant = abs(mantissa)
            while mant % 10 == 0:
                mant //= 10
                exp += 1
            mantissa = mant * sign

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))