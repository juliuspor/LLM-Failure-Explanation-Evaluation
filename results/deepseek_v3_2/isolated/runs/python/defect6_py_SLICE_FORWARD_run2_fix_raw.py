    def add_number(self, x: float):
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")
        
        if not math.isfinite(x):
            # Handle infinity and NaN
            self.add(str(x))
            return
        
        if x == int(x):
            value = int(x)
            if value == 0:
                # Handle zero, including negative zero
                if self.is_negative_zero(x):
                    self.add("-0")
                else:
                    self.add("0")
                return
            
            mantissa = value
            exp = 0
            # Avoid infinite loop when mantissa becomes 0
            while mantissa != 0 and mantissa % 10 == 0:
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