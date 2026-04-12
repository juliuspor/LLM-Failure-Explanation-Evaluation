def add_number(self, x: float):
    prev = self.get_last_char()
    if math.copysign(1.0, x) < 0.0 and prev == '-':
        self.add(" ")
    if self.is_negative_zero(x):
        self.add("-0.0")
        return
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            while mantissa % 10 == 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == value:
                    mantissa //= 10
                    exp += 1
                else:
                    break
        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))