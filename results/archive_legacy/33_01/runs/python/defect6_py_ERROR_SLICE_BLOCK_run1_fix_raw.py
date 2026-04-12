def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")
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
            value_str = str(mantissa) + "E" + str(exp)
        else:
            value_str = str(value)
    else:
        value_str = str(x)
    first = value_str[0] if len(value_str) > 0 else '\0'
    last = prev
    if self.is_word_char(last) and not self.is_word_char(first):
        self.append(" ")
    self.add(value_str)