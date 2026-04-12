def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.maybe_end_statement()
        if len(self.code) == 0 or self.code[-1] != ' ':
            self.code += ' '
    else:
        self.maybe_end_statement()
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
            newcode = str(mantissa) + "E" + str(exp)
        else:
            newcode = str(value)
    else:
        newcode = str(x)
    if len(newcode) == 0:
        return
    c = newcode[0]
    if (self.is_word_char(c) or c == '\\') and self.is_word_char(self.get_last_char()):
        self.code += ' '
    self.code += newcode