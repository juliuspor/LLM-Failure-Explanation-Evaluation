    def add_number(self, x: float):
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")
        
        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            int_val = int(x)
            abs_val = abs(int_val)
            if abs_val == 0:
                self.add("0")
                return
            
            mantissa = abs_val
            exp = 0
            while mantissa % 10 == 0:
                # Remove one trailing zero
                mantissa //= 10
                exp += 1
                # Stop if mantissa becomes 0 (should not happen because abs_val > 0)
                if mantissa == 0:
                    mantissa = 1
                    break
            
            # Build the numeric string
            if exp > 2:
                num_str = str(mantissa) + "E" + str(exp)
            else:
                # Reconstruct the integer without exponent
                num_str = str(abs_val)
            
            # Add sign if negative
            if int_val < 0:
                num_str = "-" + num_str
            
            self.add(num_str)
        else:
            self.add(str(x))