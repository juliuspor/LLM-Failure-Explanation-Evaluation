    def add_number(self, x: float):
        """
        Append a numeric literal to the output stream.

        This emits a compact, Java-like representation and may insert whitespace
        when needed to avoid creating ambiguous tokens.

        Args:
            x: The numeric value to emit.
        """
        # Ensure x is a float to avoid type errors
        try:
            x_float = float(x)
        except (TypeError, ValueError):
            # If conversion fails, fall back to string representation
            self.add(str(x))
            return
        
        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if x_float < 0 and prev == '-':
            self.add(" ")

        # Check if x is effectively an integer (within floating precision)
        if math.isfinite(x_float) and not math.isnan(x_float):
            x_int = int(x_float)
            if x_float == x_int:
                mantissa = x_int
                exp = 0
                # Use absolute value for scaling
                abs_mantissa = abs(mantissa)
                if abs_mantissa >= 100:
                    while abs_mantissa % 10 == 0:
                        check_val = (mantissa // 10) * (10 ** (exp + 1))
                        if check_val == mantissa:
                            mantissa //= 10
                            exp += 1
                            abs_mantissa = abs(mantissa)
                        else:
                            break
                
                if exp > 2:
                    self.add(str(mantissa) + "E" + str(exp))
                else:
                    self.add(str(mantissa))
                return
        
        # For non-integer, infinite, or NaN values
        self.add(str(x_float))