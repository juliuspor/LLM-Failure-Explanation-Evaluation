def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        if self.is_negative_zero(x):
            value_str = "-0"
            mantissa = 0
            exp = 0
        else:
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
                value_str = str(mantissa) + "E" + str(exp)
            else:
                value_str = str(value)
        self.add(value_str)
    else:
        if self.is_negative_zero(x):
            self.add("-0.0")
        else:
            self.add(str(x))