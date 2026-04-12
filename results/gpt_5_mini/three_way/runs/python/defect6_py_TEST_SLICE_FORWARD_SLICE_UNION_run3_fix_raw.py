def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        # Only try to factor out powers of 10 when abs(value) >= 100
        if abs(value) >= 100:
            # Use integer arithmetic: repeatedly divide by 10 while divisible and
            # reconstructing mantissa * 10**exp equals original value.
            while mantissa % 10 == 0:
                # prospective mantissa and exponent
                next_mantissa = mantissa // 10
                next_exp = exp + 1
                # reconstruct value from next_mantissa and next_exp
                try:
                    check_val = next_mantissa * (10 ** next_exp)
                except OverflowError:
                    break
                if check_val == value:
                    mantissa = next_mantissa
                    exp = next_exp
                else:
                    break

        if exp > 2:
            self.add(str(mantissa) + "E" + str(exp))
        else:
            self.add(str(value))
    else:
        self.add(str(x))