def add_number(self, x: float):
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
            number_str = str(mantissa) + "E" + str(exp)
        else:
            number_str = str(value)
    else:
        number_str = str(x)

    if prev == '-' and len(number_str) > 0 and number_str[0].isdigit():
        self.append(number_str)
    else:
        self.add(number_str)