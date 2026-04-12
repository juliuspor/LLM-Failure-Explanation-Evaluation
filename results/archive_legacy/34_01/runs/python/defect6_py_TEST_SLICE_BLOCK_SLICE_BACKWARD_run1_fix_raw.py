def add_number(self, x: float):
    sign = ""
    if x < 0 or self.is_negative_zero(x):
        sign = "-"
    ax = abs(x)
    if ax == int(ax) and not math.isinf(ax) and not math.isnan(ax):
        value = int(ax)
        mantissa = value
        exp = 0
        if abs(ax) >= 100:
            while mantissa % 10 == 0:
                check_val = (mantissa // 10) * (10 ** (exp + 1))
                if check_val == value:
                    mantissa //= 10
                    exp += 1
                else:
                    break
        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(sign + str(value))
    else:
        self.add(sign + str(ax))