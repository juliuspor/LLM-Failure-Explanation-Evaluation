    def add_number(self, x: float):
        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if prev == '-' and str(x).startswith('-'):
            self.add(" ")

        try:
            num = float(x)
        except (ValueError, TypeError):
            self.add(str(x))
            return

        if math.isinf(num) or math.isnan(num):
            self.add(str(num))
        elif num == int(num):
            value = int(num)
            mantissa = value
            exp = 0
            if abs(num) >= 100:
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
            self.add(str(num))