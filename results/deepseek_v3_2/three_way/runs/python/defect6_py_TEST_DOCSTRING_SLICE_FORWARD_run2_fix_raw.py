    def add_number(self, x: float):
        """
        Append a numeric literal to the output stream.

        This emits a compact, Java-like representation and may insert whitespace
        when needed to avoid creating ambiguous tokens.

        Args:
            x: The numeric value to emit.
        """
        # This is not pretty printing. This is to prevent misparsing of x- -4 as
        # x--4 (which is a syntax error).
        prev = self.get_last_char()
        if x < 0 and prev == '-':
            self.add(" ")
        
        # Handle negative zero: we need to output "-0.0" or "-0" etc.
        # Use is_negative_zero to detect negative zero.
        if self.is_negative_zero(x):
            # For negative zero, we must output a negative sign.
            # We'll treat it as a special case.
            # Determine if we should output integer or float representation.
            # Since x is 0.0, we can output "-0.0" or "-0" if integer.
            # The original logic for integer detection: if x == int(x) and not math.isinf(x) and not math.isnan(x)
            # For negative zero, x == int(x) is True (0 == 0), and not inf/nan.
            # So we follow the same logic but ensure negative sign.
            # However, the integer representation of -0 is "-0".
            # We'll mimic the same logic but prepend a negative sign.
            # Actually, we can just output "-0.0" to be safe, but the original code might output "0" for integer zero.
            # Let's replicate the original logic but with negative sign.
            # We'll compute the absolute value and then add sign.
            abs_x = abs(x)  # 0.0
            if abs_x == int(abs_x) and not math.isinf(abs_x) and not math.isnan(abs_x):
                value = int(abs_x)  # 0
                mantissa = value
                exp = 0
                if abs_x >= 100:
                    while mantissa % 10 == 0:
                        check_val = (mantissa // 10) * (10 ** (exp + 1))
                        if check_val == value:
                            mantissa //= 10
                            exp += 1
                        else:
                            break
                if exp > 2:
                    self.add("-" + str(mantissa) + "E" + str(exp))
                else:
                    self.add("-" + str(value))
            else:
                self.add("-" + str(abs_x))
            return
        
        # Original logic for non-negative-zero numbers
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