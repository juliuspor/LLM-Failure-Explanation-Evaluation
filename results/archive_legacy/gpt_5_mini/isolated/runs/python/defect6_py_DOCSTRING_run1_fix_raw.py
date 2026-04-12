def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        s = str(abs(value))
        i = len(s)
        while i > 0 and s[i - 1] == '0':
            i -= 1
        exp = len(s) - i
        if exp > 0:
            mantissa = s[:i] if i > 0 else '0'
            if value < 0:
                mantissa = '-' + mantissa
            if exp > 2:
                self.add(mantissa + "E" + str(exp))
            else:
                self.add(str(value))
        else:
            self.add(str(value))
    else:
        self.add(str(x))