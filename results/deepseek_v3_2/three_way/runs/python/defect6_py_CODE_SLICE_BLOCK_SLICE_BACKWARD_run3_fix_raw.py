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

        # Determine if x is an integer value, considering floating-point precision.
        # Use tolerance for large numbers.
        # First, check if x is finite and not NaN.
        if math.isfinite(x):
            # Check if x is mathematically an integer.
            # Use abs(x) to handle negative numbers.
            # For large floats, we compare with the nearest integer.
            # Use a relative tolerance? Since we care about integer equality,
            # we can check if the fractional part is negligible.
            # However, for very large numbers, the fractional part may be lost.
            # Instead, we can check if rounding to integer gives back the same value.
            # But we need to avoid rounding errors causing false positives.
            # A common approach: check if floor(x) == ceil(x) within tolerance.
            # But we can also use: abs(x - round(x)) <= abs(x) * sys.float_info.epsilon * 10
            # However, we want to treat numbers like 1e23 as integers for formatting.
            # The original code used x == int(x). That fails for large integers.
            # We can use: x.is_integer() method for float.
            # But note: x.is_integer() returns True if the float is an integer value.
            # For large floats, it may still return True if the value is exactly integer.
            # However, for numbers like 1e23, float(1e23).is_integer() returns True.
            # Wait: In Python, float(1e23).is_integer() returns True because 1e23 is exactly representable? Not necessarily.
            # Actually, 1e23 is not exactly representable in binary floating point, but .is_integer() returns True if the value is integer in the mathematical sense, i.e., fractional part is zero.
            # Since floating point cannot represent fractional part for such large numbers, .is_integer() may still return True.
            # Let's test: (1e23).is_integer() -> True. So we can use that.
            # However, .is_integer() is only available for float. x is float.
            # So we can use x.is_integer().
            if x.is_integer():
                # x is an integer value.
                value = int(x)  # Convert to integer (may be huge, but Python int is arbitrary precision).
                mantissa = value
                exp = 0
                # For large integers, we want to output scientific notation if it's compact.
                # The original loop tried to factor out powers of ten.
                # We'll keep that logic but apply to the integer value.
                # However, we must be careful with negative numbers: value is negative if x<0.
                # Use abs for factoring powers of ten.
                abs_mantissa = abs(mantissa)
                if abs_mantissa >= 100:
                    # Factor out trailing zeros.
                    while abs_mantissa % 10 == 0:
                        # Check if dividing by 10 and increasing exponent gives same value.
                        # Since we are working with integers, we can compute directly.
                        # But we need to ensure we don't lose sign.
                        # We'll compute new_mantissa = mantissa // 10
                        # and new_exp = exp + 1
                        # and check if new_mantissa * (10 ** new_exp) == value.
                        # However, for large numbers, 10**new_exp may be huge, but Python can handle.
                        # Alternatively, we can check if mantissa % 10 == 0 and then divide.
                        # But we must stop when mantissa % 10 != 0.
                        # The original code had a check that might be unnecessary.
                        # We'll simplify: while mantissa % 10 == 0: mantissa //= 10; exp += 1
                        # But we need to ensure we don't factor out zeros that are not trailing? Actually, modulo 10 only checks last digit.
                        # So it's fine.
                        # However, we must handle negative mantissa: -1200 % 10 == 0? In Python, -1200 % 10 gives 0 (because remainder has sign of divisor). So it's safe.
                        # Let's implement:
                        mantissa //= 10
                        exp += 1
                        abs_mantissa = abs(mantissa)
                # Now decide format.
                if exp > 2:
                    self.add(str(mantissa) + "E" + str(exp))
                else:
                    # Reconstruct the integer from mantissa and exp? Actually, we have mantissa and exp.
                    # But if exp>0, we have factored out trailing zeros. So we need to output mantissa * 10^exp.
                    # However, if exp <=2, we output the original integer value.
                    # But we have changed mantissa and exp. So we need to reconstruct? Or we can output str(value).
                    # Simpler: we can compute the string representation of value directly.
                    # But the original code used str(value) for the else branch.
                    # We'll keep that: output str(value).
                    # However, note that we may have changed mantissa and exp. So we need to use the original value.
                    # Actually, we have value stored. So we can use that.
                    self.add(str(value))
            else:
                # x is not an integer.
                self.add(str(x))
        else:
            # x is inf or nan.
            self.add(str(x))
