def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        if hasattr(self, 'append') and callable(getattr(self, 'append')):
            self.append(" ")
        else:
            self.code += " "
    self.maybe_end_statement()
    s = None
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
            s = str(mantissa) + "E" + str(exp)
        else:
            s = str(value)
    else:
        s = str(x)
    if hasattr(self, 'append') and callable(getattr(self, 'append')):
        self.append(s)
    else:
        self.code += s