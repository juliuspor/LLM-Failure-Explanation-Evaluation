def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.maybe_end_statement()
        self.append(" ")
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        if abs(value) >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                mantissa //= 10
                exp += 1
        if exp > 2:
            num_str = str(mantissa) + "E" + str(exp)
        else:
            num_str = str(value)
    else:
        if self.is_negative_zero(x):
            num_str = "-0.0"
        else:
            num_str = str(x)
    self.maybe_end_statement()
    self.append(num_str)