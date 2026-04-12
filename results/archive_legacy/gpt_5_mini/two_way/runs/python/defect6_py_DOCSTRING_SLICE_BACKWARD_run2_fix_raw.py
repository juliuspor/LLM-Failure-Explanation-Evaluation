def add_number(self, x: float):
    prev = self.get_last_char()
    try:
        if hasattr(x, "item"):
            scalar = x.item()
        elif isinstance(x, (int, float)):
            scalar = x
        else:
            scalar = None
    except Exception:
        scalar = None
    if scalar is None:
        try:
            if not isinstance(x, (str, bytes)) and hasattr(x, "__len__") and len(x) != 1:
                self.add(str(x))
                return
        except Exception:
            pass
        try:
            scalar = float(x)
        except Exception:
            self.add(str(x))
            return
    if scalar < 0 and prev == '-':
        self.add(" ")
    if isinstance(scalar, (int, float)) and math.isfinite(scalar) and scalar == int(scalar):
        value = int(scalar)
        mantissa = value
        exp = 0
        if abs(scalar) >= 100:
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
        self.add(str(scalar))