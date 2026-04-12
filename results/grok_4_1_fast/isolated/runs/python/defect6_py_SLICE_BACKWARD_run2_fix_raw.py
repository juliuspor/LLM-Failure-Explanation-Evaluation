def add_number(self, x):
    prev = self.get_last_char()
    if isinstance(x, (int, float)) and x < 0 and prev == '-':
        self.add(" ")

    if not isinstance(x, (int, float)):
        self.add(str(x))
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