def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")
    neg = x < 0 or self.is_negative_zero(x)
    ax = -x if neg else x
    if ax == int(ax) and not math.isinf(ax) and not math.isnan(ax):
        value = int(ax)
        mantissa = value
        exp = 0
        if abs(ax) >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == value:
                    mantissa //= 10
                    exp += 1
                else:
                    break
        if exp > 2:
            s = str(mantissa) + "E" + str(exp)
        else:
            s = str(value)
    else:
        s = str(ax)
    if neg:
        self.append("-")
        self.add(s)
    else:
        self.add(s)
