def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(' ')

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        if abs(x) >= 100:
            exp = int(math.floor(math.log10(abs(x))))
            mantissa = value // (10 ** exp)
            if exp > 2:
                self.add(str(mantissa) + 'E' + str(exp))
                return
        self.add(str(value))
    else:
        self.add(str(x))