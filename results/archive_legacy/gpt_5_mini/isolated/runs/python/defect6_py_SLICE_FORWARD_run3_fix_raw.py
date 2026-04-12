def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        sign = -1 if value < 0 else 1
        abs_value = abs(value)
        mantissa = abs_value
        exp = 0
        if abs(x) >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                mantissa //= 10
                exp += 1
            if exp > 2:
                mantissa_signed = str(mantissa * sign)
                self.add(mantissa_signed + "E" + str(exp))
            else:
                self.add(str(value))
        else:
            self.add(str(value))
    else:
        self.add(str(x))