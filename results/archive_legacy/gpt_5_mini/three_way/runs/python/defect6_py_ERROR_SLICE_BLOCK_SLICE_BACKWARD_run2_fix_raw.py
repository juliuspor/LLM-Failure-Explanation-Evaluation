def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        sign_is_negative = math.copysign(1.0, x) < 0.0
        value = int(x)
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
        sign = "-" if sign_is_negative else ""
        if exp > 2:
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(sign + str(abs(value)))
    else:
        self.add(str(x))