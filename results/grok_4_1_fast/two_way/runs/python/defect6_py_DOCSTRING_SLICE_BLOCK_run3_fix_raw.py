    def add_number(self, x: float):
        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")

        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            value_str = str(int(x))
            trailing_zeros = 0
            for i in range(len(value_str) - 1, -1, -1):
                if value_str[i] == '0':
                    trailing_zeros += 1
                else:
                    break
            mantissa_str = value_str[:-trailing_zeros] if trailing_zeros > 0 else value_str
            exp = trailing_zeros
            
            if exp > 2:
                self.add(mantissa_str + "E" + str(exp))
            else:
                self.add(value_str)
        else:
            self.add(str(x))