    def add_number(self, x: float):
        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")

        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            value = int(x)
            if value == 0:
                self.add("0")
                return
            
            mantissa = value
            exp = 0
            while mantissa % 10 == 0 and value % 10 == 0:
                mantissa //= 10
                exp += 1
                value //= 10
            
            if exp > 2:
                self.add(str(mantissa) + "E" + str(exp))
            else:
                self.add(str(mantissa * (10 ** exp)))
        else:
            self.add(str(x))