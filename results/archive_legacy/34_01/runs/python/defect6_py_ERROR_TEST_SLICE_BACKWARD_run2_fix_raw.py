def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

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
            num_text = str(mantissa) + "E" + str(exp)
        else:
            num_text = str(value)
    else:
        if self.is_negative_zero(x):
            num_text = "-0.0"
        else:
            num_text = str(x)

    self.add(num_text)