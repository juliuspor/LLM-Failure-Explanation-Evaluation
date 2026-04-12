def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Determine if x is an integer value and not infinite or NaN without using math module
    try:
        is_inf = abs(x) == float('inf')
    except Exception:
        is_inf = False
    is_nan = x != x

    if x == int(x) and not is_inf and not is_nan:
        value = int(x)
        mantissa = value
        exp = 0
        if abs(x) >= 100:
            while mantissa % 10 == 0 and mantissa != 0:
                # check if removing a trailing zero and scaling back yields the same value
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