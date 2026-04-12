def add_number(self, x: float):
    # This is not pretty printing. This is to prevent misparsing of x- -4 as
    # x--4 (which is a syntax error).
    prev = self.get_last_char()
    try:
        is_numeric = isinstance(x, (int, float))
    except Exception:
        is_numeric = False

    if is_numeric:
        if x < 0 and prev == '-':
            self.add(" ")

        # Handle non-finite values explicitly first.
        if math.isnan(x):
            self.add(str(x))
            return
        if math.isinf(x):
            # Use Python's string representation for infinities ("inf"/"-inf").
            # If Java-like "Infinity" is desired, replace accordingly.
            self.add(str(x))
            return

        # Now x is a finite number. Check if it is an integer value.
        # Avoid converting extremely large floats with int() if they would
        # overflow or lose meaning; use a safe threshold.
        if x == int(x):
            value = int(x)
            mantissa = value
            exp = 0
            if abs(x) >= 100:
                while mantissa % 10 == 0 and mantissa != 0:
                    # Reconstruct check_val carefully to avoid large power-of-10 issues
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

        # Non-integer finite numeric: use default string conversion
        self.add(str(x))
    else:
        # Non-numeric types: fall back to string conversion
        self.add(str(x))