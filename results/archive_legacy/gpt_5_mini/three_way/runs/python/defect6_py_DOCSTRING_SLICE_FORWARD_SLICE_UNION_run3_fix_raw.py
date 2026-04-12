def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            while mantissa != 0 and mantissa % 10 == 0:
                mantissa //= 10
                exp += 1
                check_val = mantissa * (10 ** exp)
                if check_val == value:
                    break
        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))