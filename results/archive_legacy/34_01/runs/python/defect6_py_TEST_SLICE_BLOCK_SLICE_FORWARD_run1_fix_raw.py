def add_number(self, x: float):
    prev = self.get_last_char()
    need_raw_append = (x < 0 or self.is_negative_zero(x)) and prev == '-'
    if x == int(x) and not math.isinf(x) and not math.isnan(x) and not self.is_negative_zero(x):
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
            s = str(mantissa) + "E" + str(exp)
            if value < 0:
                s = "-" + s
        else:
            s = str(value)
    else:
        if self.is_negative_zero(x):
            s = "-0.0"
        else:
            s = str(x)
    if need_raw_append:
        if s.startswith("-"):
            s = s[1:]
        self.append(s)
    else:
        self.add(s)