    def add_number(self, x: float):
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")

        # Check if x is mathematically an integer without precision loss
        # Use Decimal for high precision integer detection
        try:
            from decimal import Decimal, InvalidOperation
            d = Decimal(str(x))  # Convert via string to avoid float precision issues
            if d == d.to_integral_value():
                # It's an integer
                value = int(d)  # Safe conversion now
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
        except (InvalidOperation, ValueError):
            # Fallback to original logic if Decimal fails
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