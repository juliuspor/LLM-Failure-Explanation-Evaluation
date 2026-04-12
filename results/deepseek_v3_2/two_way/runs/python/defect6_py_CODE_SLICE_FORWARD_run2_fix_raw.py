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

        if x == int(x) and not math.isinf(x) and not math.isnan(x):
            value = int(x)
            mantissa = value
            exp = 0
            if abs(x) >= 100:
                # Use absolute value for zero-stripping to avoid issues with negative multiples.
                abs_mantissa = abs(mantissa)
                while abs_mantissa % 10 == 0:
                    # Tentatively remove a zero and see if the reconstruction matches.
                    trial_mantissa = mantissa // 10
                    trial_exp = exp + 1
                    check_val = trial_mantissa * (10 ** trial_exp)
                    if check_val == value:
                        mantissa = trial_mantissa
                        exp = trial_exp
                        abs_mantissa = abs(mantissa)
                    else:
                        break
            
            if exp > 2:
                self.add(str(mantissa) + "E" + str(exp))
            else:
                self.add(str(value))
        else:
            self.add(str(x))