def add_number(self, x: float):
    prev = self.get_last_char()
    if (x < 0 or self.is_negative_zero(x)) and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        is_neg_zero = self.is_negative_zero(x)
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
        sign = "-" if is_neg_zero else ""
        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(sign + str(value))
    else:
        self.add(str(x))