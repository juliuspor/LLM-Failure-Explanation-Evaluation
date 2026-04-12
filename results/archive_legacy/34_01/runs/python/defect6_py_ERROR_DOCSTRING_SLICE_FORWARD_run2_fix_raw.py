def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        sign = '-' if x < 0 or self.is_negative_zero(x) else ''
        abs_value = abs(x)
        value = int(abs_value)
        mantissa = value
        exp = 0
        if abs_value >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
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
        if self.is_negative_zero(x):
            self.add("-0.0")
        else:
            self.add(str(x))