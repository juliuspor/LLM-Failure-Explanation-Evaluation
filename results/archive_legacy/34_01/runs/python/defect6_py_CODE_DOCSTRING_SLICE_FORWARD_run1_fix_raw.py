def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if isinstance(x, float) and x.is_integer() and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        sign = -1 if value < 0 else 1
        unsigned = abs(value)
        mantissa = unsigned
        exp = 0
        while mantissa != 0 and mantissa % 10 == 0:
            mantissa //= 10
            exp += 1
        mantissa *= sign
        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))