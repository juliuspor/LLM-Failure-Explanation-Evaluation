def add_number(self, x: float):
    prev = self.get_last_char()
    # Prevent merging with a preceding '-' for negative numbers (e.g., x--4)
    if x < 0 and prev == '-':
        self.add(" ")

    # If previous char is a word char or digit, insert a space to avoid merging
    if self.is_word_char(prev) or prev.isdigit():
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
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))