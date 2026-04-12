def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        abs_val = abs(value)
        mantissa = abs_val
        exp = 0
        if abs(value) >= 100:
            while mantissa != 0 and mantissa % 10 == 0:
                mantissa //= 10
                exp += 1
        if exp > 2:
            if value < 0:
                self.add("-" + str(mantissa) + "E" + str(exp))
            else:
                self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))