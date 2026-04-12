def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        # Use the existing '-' as the sign and append the absolute value directly
        ax = -x
        if ax == int(ax) and not math.isinf(ax) and not math.isnan(ax):
            value = int(ax)
            mantissa = value
            exp = 0
            if abs(ax) >= 100:
                while mantissa % 10 == 0:
                    check_val = (mantissa // 10) * (10 ** (exp + 1))
                    if check_val == value:
                        mantissa //= 10
                        exp += 1
                    else:
                        break
            if exp > 2:
                self.append(str(mantissa) + "E" + str(exp))
            else:
                self.append(str(value))
        else:
            self.append(str(ax))
        return

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