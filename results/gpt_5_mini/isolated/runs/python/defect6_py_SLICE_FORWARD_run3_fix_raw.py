def add_number(self, x: float):
    prev = self.get_last_char()
    if x < 0 and prev == '-':
        self.add(" ")

    # Handle integers exactly representable and not inf/nan
    if x == int(x) and not math.isinf(x) and not math.isnan(x):
        value = int(x)
        mantissa = value
        exp = 0
        # For large absolute values, strip trailing zeros to produce shorter form
        if abs(value) >= 100:
            # Work with a copy for checking so we don't lose original mantissa prematurely
            while mantissa != 0 and mantissa % 10 == 0:
                # candidate represents what the value would be if we removed one more 10
                candidate = (mantissa // 10) * (10 ** (exp + 1))
                # If candidate equals original value, we can consume another trailing zero
                if candidate == value:
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