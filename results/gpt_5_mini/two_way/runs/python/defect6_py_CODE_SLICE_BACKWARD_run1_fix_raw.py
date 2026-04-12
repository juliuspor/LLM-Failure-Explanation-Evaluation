def add_number(self, x: float):
    prev = self.get_last_char()
    # Avoid misparsing of x- -4 as x--4
    if isinstance(x, (int, float)):
        if x < 0 and prev == '-':
            self.add(" ")

        # Handle integers (including floats that are whole numbers), infinities, and NaNs
        if not math.isinf(x) and not math.isnan(x) and float(x).is_integer():
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
            return

        # For other numeric values (floats, infinities, NaNs)
        # Use Python's str for representation
        self.add(str(x))
    else:
        # Not a numeric input: convert safely to string
        # Preserve heuristic about spacing when previous char was '-'
        if isinstance(x, str) and len(x) > 0 and x[0] == '-' and prev == '-':
            self.add(" ")
        self.add(str(x))