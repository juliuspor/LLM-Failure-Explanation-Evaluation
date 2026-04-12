def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if self.is_negative_zero(x):
        self.add("-0.0")
        return

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = abs(value)
        exp = 0
        if mantissa >= 100:
            while mantissa % 10 == 0:
                mantissa //= 10
                exp += 1
                if mantissa * (10 ** exp) != abs(value):
                    mantissa *= 10
                    exp -= 1
                    break
        
        if exp > 2:
            sign = '-' if value < 0 else ''
            self.add(sign + str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))