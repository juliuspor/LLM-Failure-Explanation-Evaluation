def add_number(self, x: float):
    prev = self.get_last_char()
    if self.is_negative_zero(x):
        numstr = "-0.0"
    elif x == int(x) and not math.isinf(x) and not math.isnan(x):
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
            numstr = str(mantissa) + "E" + str(exp)
        else:
            numstr = str(value)
    else:
        numstr = str(x)
    if x < 0 and prev == '-':
        self.add(" ")
    self.add(numstr)