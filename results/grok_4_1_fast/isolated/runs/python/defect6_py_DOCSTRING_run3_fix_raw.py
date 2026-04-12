    def add_number(self, x: float):
        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")

        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            value = int(x)
            if abs(x) >= 100:
                mantissa = abs(value)
                exp = 0
                while mantissa % 10 == 0 and mantissa > 0:
                    mantissa //= 10
                    exp += 1
                if exp > 2:
                    sign = '-' if value < 0 else ''
                    self.add(sign + str(mantissa) + "E" + str(exp))
                    return
            self.add(str(value)) 
        else:
            self.add(str(x))