def add_number(self, x: float):
    prev = self.get_last_char()
    if self.is_negative_zero(x):
        if prev == '-':
            self.add(" ")
        self.add("-0.0")
        return
    if x < 0 and prev == '-':
        self.add(" ")
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        sign = "-" if value < 0 else ""
        mantissa = abs(value)
        exp = 0
        if abs(x) >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break
        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(sign + str(mantissa))
    else:
        self.add(str(x))