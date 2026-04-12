def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")
    if self.is_negative_zero(x):
        self.add("-0.0")
        return
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        sign = "-" if value < 0 else ""
        mantissa = abs(value)
        exp = 0
        if abs(x) >= 100:
            while mantissa != 0 and mantissa % 10 == 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == abs(value):
                    mantissa //= 10
                    exp += 1
                else:
                    break
        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(sign + str(abs(value)))
    else:
        s = str(x)
        if x < 0 and not s.startswith("-"):
            s = "-" + s
        self.add(s)