def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        if abs(value) >= 100:
            mantissa = abs(value)
            exp = 0
            while mantissa % 10 == 0:
                mantissa //= 10
                exp += 1
            sign = '-' if value < 0 else ''
            if exp > 2:
                self.add(f'{sign}{mantissa}e{exp}')
                return
        self.add(str(value))
    else:
        self.add(str(x))