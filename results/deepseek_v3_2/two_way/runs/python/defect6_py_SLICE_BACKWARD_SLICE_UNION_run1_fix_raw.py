    def add_number(self, x: float):
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")
        
        if math.isinf(x) or math.isnan(x):
            self.add(str(x))
            return
        
        if x == 0.0:
            if math.copysign(1, x) < 0:
                self.add("-0")
            else:
                self.add("0")
            return
        
        if x == math.floor(x):
            value = int(x)
            mantissa = value
            exp = 0
            if abs(value) >= 100:
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