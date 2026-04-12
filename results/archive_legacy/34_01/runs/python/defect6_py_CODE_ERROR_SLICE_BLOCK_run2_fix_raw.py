def add_number(self, x: float):
    prev = self.get_last_char()
    sign_negative = math.copysign(1.0, x) < 0
    if sign_negative and prev == '-':
        self.add(" ")
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        if value == 0 and sign_negative:
            self.add("-0")
            return
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