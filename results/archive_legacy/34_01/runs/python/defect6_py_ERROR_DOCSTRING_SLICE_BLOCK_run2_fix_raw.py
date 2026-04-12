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
            s = str(mantissa) + "E" + str(exp)
        else:
            s = str(value)
    else:
        s = str(x)

    if len(s) > 0:
        first = s[0]
        starts_word = (first == '-' and len(s) > 1 and self.is_word_char(s[1])) or self.is_word_char(first) or first == '\\'
        if starts_word and self.is_word_char(prev):
            self.append(" ")
    self.append(s)