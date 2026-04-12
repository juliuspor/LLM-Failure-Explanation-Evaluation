def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        if value == 0:
            self.add("0")
            return
        sign = "-" if value < 0 else ""
        s = str(abs(value))
        stripped = s.rstrip('0')
        tz = len(s) - len(stripped)
        if tz > 2:
            mantissa = stripped
            exp = tz
            self.add(sign + mantissa + "E" + str(exp))
        else:
            self.add(sign + s)
    else:
        self.add(str(x))