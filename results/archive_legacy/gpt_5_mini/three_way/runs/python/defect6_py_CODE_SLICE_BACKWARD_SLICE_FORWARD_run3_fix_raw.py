def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if math.isfinite(x) and x == int(x):
        value = int(x)
        sign = -1 if value < 0 else 1
        mantissa_abs = abs(value)
        exp = 0
        if abs(x) >= 100:
            while mantissa_abs != 0 and mantissa_abs % 10 == 0:
                candidate = (mantissa_abs // 10) * (10 ** (exp + 1))
                if candidate == abs(value):
                    mantissa_abs //= 10
                    exp += 1
                else:
                    break
        if exp > 2:
            mantissa_str = ("-" if sign < 0 else "") + str(mantissa_abs)
            self.add(mantissa_str + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))