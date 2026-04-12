    def add_number(self, x: float):
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")

        # Check if x is an exact integer within the range where float->int is exact.
        # For IEEE 754 double, integers up to 2^53 are represented exactly.
        # Use is_integer() which returns True for float values that are mathematically integers.
        if abs(x) <= 2**53 and x.is_integer() and not math.isinf(x) and not math.isnan(x):
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