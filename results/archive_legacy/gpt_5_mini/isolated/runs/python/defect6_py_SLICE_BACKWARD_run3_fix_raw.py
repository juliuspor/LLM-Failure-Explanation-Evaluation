def add_number(self, x: float):
    try:
        if isinstance(x, bool):
            self.add(str(int(x)))
            return
        if isinstance(x, int):
            value = x
            if abs(value) >= 100:
                mantissa = value
                exp = 0
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
                self.add(str(value))
            return
        if isinstance(x, float):
            prev = self.get_last_char()
            if x < 0 and prev == '-':
                self.add(" ")
            if x.is_integer() and not math.isinf(x) and not math.isnan(x):
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
            return
    except Exception:
        pass
    try:
        length = len(x)
    except Exception:
        self.add(str(x))
        return
    if length == 1:
        try:
            single = x[0]
            self.add(str(single))
            return
        except Exception:
            self.add(str(x))
            return
    self.add(str(x))