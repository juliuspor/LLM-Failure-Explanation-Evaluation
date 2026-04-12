def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            m = abs(value)
            e = 0
            if m != 0:
                while m % 10 == 0:
                    m //= 10
                    e += 1
            if value < 0:
                mantissa = -m
            else:
                mantissa = m
            exp = e
        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))