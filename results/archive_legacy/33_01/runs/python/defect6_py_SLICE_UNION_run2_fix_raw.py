def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        try:
            self.add(" ")
        except Exception:
            try:
                list.append(self, " ")
            except Exception:
                if hasattr(self, 'code'):
                    self.code += " "
                else:
                    raise

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

    try:
        self.add(s)
    except Exception:
        try:
            list.append(self, s)
        except Exception:
            if hasattr(self, 'code'):
                self.code += s
            else:
                raise