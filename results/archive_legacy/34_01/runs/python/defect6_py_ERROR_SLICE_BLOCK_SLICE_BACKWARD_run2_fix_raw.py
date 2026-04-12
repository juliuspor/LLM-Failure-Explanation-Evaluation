def add_number(self, x: float):
    self.maybe_end_statement()
    prev = self.get_last_char()
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
            numstr = str(mantissa) + "E" + str(exp)
        else:
            numstr = str(value)
    else:
        numstr = str(x)
    first = numstr[0] if len(numstr) > 0 else '\0'
    if prev == '-':
        self.append(" ")
    elif (self.is_word_char(first) or first == '\\') and self.is_word_char(prev) and prev != '-':
        self.append(" ")
    self.append(numstr)