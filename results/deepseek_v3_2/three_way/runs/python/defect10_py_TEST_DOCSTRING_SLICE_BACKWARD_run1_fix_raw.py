    @staticmethod
    def create_number(val: Optional[str]) -> Optional[Union[int, float, Decimal]]:
        """
        Parse a Java-style numeric string into a Python number.

        This mirrors the structure of Apache Commons Lang's
        `NumberUtils#createNumber`, supporting decimal, hexadecimal (`0x...`),
        scientific notation, and optional type qualifiers (for example `L`,
        `F`, or `D`).

        Args:
            val: String to parse. If None, returns None.

        Returns:
            An `int`, `float`, or `Decimal` depending on the input.

        Raises:
            ValueError: If `val` cannot be parsed as a number.
        """
        if val is None:
            return None
        if len(val) == 0:
            raise ValueError('"" is not a valid number.')
        if val.startswith("--"):
            # Mirrors Java's special-case behavior.
            return None
        if val.startswith(("0x", "-0x", "+0x")):
            return NumberUtils.create_integer(val)

        # Check for invalid characters early.
        # We'll allow digits, signs, decimal point, exponent, and qualifiers.
        # But we need to ensure that the string is not just letters.
        # The original Java implementation does a lot of validation in the loop.
        # We'll replicate that by using the is_number method.
        # However, note that is_number returns True for valid numbers, but we need to handle qualifiers.
        # The test expects ValueError for "l", "L", "f", "F", "junk", "bobL".
        # Let's first check if the string consists only of letters (no digits) and is not a valid qualifier.
        # But the existing logic already handles qualifiers at the end.
        # The bug might be that the method does not raise ValueError for strings like "l" because it passes the last_char check.
        # Actually, for "l", last_char is 'l', which is not a digit, so it goes into the non-digit branch.
        # In that branch, it checks if last_char in ("l", "L"). It is, so it goes into that block.
        # Inside that block, it checks if dec is None and exp is None and ((char_at(numeric, 0) == "-" and NumberUtils.is_digits(numeric[1:])) or NumberUtils.is_digits(numeric)).
        # For "l", numeric = "" (since val[:-1] is empty). char_at(numeric, 0) will raise IndexError? Wait, char_at is called only if numeric is not empty? Actually, the condition is:
        # if last_char in ("l", "L"):
        #     if dec is None and exp is None and (
        #         (char_at(numeric, 0) == "-" and NumberUtils.is_digits(numeric[1:]))
        #         or NumberUtils.is_digits(numeric)
        #     ):
        # For "l", numeric = "", so char_at(numeric, 0) will raise IndexError because numeric is empty. But the condition is evaluated left-to-right, and char_at is called only if the first part of the OR is evaluated? Actually, the entire condition is evaluated, and char_at is called regardless because it's inside the expression. However, Python evaluates the OR lazily, but the char_at call is inside a subexpression that must be evaluated if the first part of the OR is considered. But the condition is a single OR between two subconditions: (char_at(numeric,0)=="-" and ...) OR NumberUtils.is_digits(numeric). Since numeric is empty, NumberUtils.is_digits(numeric) returns False (because empty string returns False). Then the first subcondition is evaluated: char_at(numeric,0) will raise IndexError. So the method will crash with IndexError, not ValueError. That's the bug! The test expects ValueError, not IndexError.
        # So we need to guard against empty numeric before calling char_at.
        # Also, for "junk", last_char is 'k', which is not in (l,L,f,F,d,D), so it goes to the final "raise ValueError" in the non-digit branch. That should raise ValueError. But wait: for "junk", last_char is 'k', not a digit, so it goes to the non-digit branch. It checks last_char in ("l", "L") -> false, then last_char in ("f", "F") -> false, then last_char in ("d", "D", "f", "F") -> false (but note f,F already checked). Actually the code has two separate checks: one for f/F and one for d/D/f/F? Let's examine: after l/L, there is a block for f/F, then a block for d/D/f/F. That's redundant. But for "junk", last_char is 'k', so it falls through to the final "raise ValueError". That should work.
        # However, the test also includes "bobL". For "bobL", last_char is 'L', so it goes into the l/L block. numeric = "bob". dec and exp are None. Now we check: (char_at(numeric,0)=="-" and NumberUtils.is_digits(numeric[1:])) OR NumberUtils.is_digits(numeric). numeric is "bob", not digits, and first char is not '-', so both false. Then we raise ValueError. That's fine.
        # So the main issue is the IndexError for single-letter qualifiers like "l". Also, we need to ensure that for "f" and "d" similar issues are handled.
        # Let's fix by checking if numeric is empty before calling char_at. Also, we should ensure that the condition for l/L handles empty numeric correctly.
        # Additionally, the condition for f/F and d/D/f/F also uses numeric, but they call create_float/create_double with numeric, which for empty string will raise ValueError (since float('') raises ValueError). That's fine because we catch ValueError and fall through. However, for "f", numeric is empty, so create_float('') raises ValueError, we catch and pass, then we go to the d/D/f/F block? Wait, the code after the f/F block does not break; it falls through to the d/D/f/F block. That's okay.
        # But we also need to consider that the condition for l/L should not raise IndexError. So we need to adjust the condition.
        # Let's rewrite the l/L block to safely check.
        # Also, note that the condition for l/L includes char_at(numeric,0). We can replace that with numeric.startswith('-')
        # We'll also need to ensure that the rest after '-' is digits.
        # Let's implement the fix.

        last_char = val[-1]
        dec_pos = val.find(".")
        e_pos = val.find("e")
        E_pos = val.find("E")
        if e_pos == -1:
            exp_pos = E_pos
        elif E_pos == -1:
            exp_pos = e_pos
        else:
            exp_pos = min(e_pos, E_pos)

        if dec_pos > -1:
            if exp_pos > -1:
                if exp_pos < dec_pos:
                    raise ValueError(f"{val} is not a valid number.")
                dec = val[dec_pos + 1 : exp_pos]
            else:
                dec = val[dec_pos + 1 :]
            mant = val[:dec_pos]
        else:
            if exp_pos > -1:
                mant = val[:exp_pos]
            else:
                mant = val
            dec = None

        if not last_char.isdigit():
            if exp_pos > -1 and exp_pos < len(val) - 1:
                exp = val[exp_pos + 1 : len(val) - 1]
            else:
                exp = None

            numeric = val[:-1]
            all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)

            if last_char in ("l", "L"):
                if dec is None and exp is None:
                    # Check if numeric is a valid integer (optional sign followed by digits)
                    if len(numeric) == 0:
                        raise ValueError(f"{val} is not a valid number.")
                    if numeric[0] == "-":
                        if len(numeric) > 1 and NumberUtils.is_digits(numeric[1:]):
                            try:
                                return NumberUtils.create_long(numeric)
                            except ValueError:
                                return NumberUtils.create_big_integer(numeric)
                    else:
                        if NumberUtils.is_digits(numeric):
                            try:
                                return NumberUtils.create_long(numeric)
                            except ValueError:
                                return NumberUtils.create_big_integer(numeric)
                raise ValueError(f"{val} is not a valid number.")

            if last_char in ("f", "F"):
                try:
                    f = NumberUtils.create_float(numeric)
                    if math.isfinite(f) and not (f == 0.0 and not all_zeros):
                        return f
                except ValueError:
                    pass
                # Fall through to the double/decimal cases.

            if last_char in ("d", "D", "f", "F"):
                try:
                    d = NumberUtils.create_double(numeric)
                    if math.isfinite(d) and not (d == 0.0 and not all_zeros):
                        return d
                except ValueError:
                    pass
                try:
                    return NumberUtils.create_big_decimal(numeric)
                except InvalidOperation:
                    pass
                raise ValueError(f"{val} is not a valid number.")

            raise ValueError(f"{val} is not a valid number.")

        if exp_pos > -1 and exp_pos < len(val) - 1:
            exp = val[exp_pos + 1 :]
        else:
            exp = None

        if dec is None and exp is None:
            try:
                return NumberUtils.create_integer(val)
            except ValueError:
                pass
            try:
                return NumberUtils.create_long(val)
            except ValueError:
                pass
            return NumberUtils.create_big_integer(val)

        all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)
        try:
            f = NumberUtils.create_float(val)
            if math.isfinite(f) and not (f == 0.0 and not all_zeros):
                return f
        except ValueError:
            pass
        try:
            d = NumberUtils.create_double(val)
            if math.isfinite(d) and not (d == 0.0 and not all_zeros):
                return d
        except ValueError:
            pass
        try:
            return NumberUtils.create_big_decimal(val)
        except InvalidOperation as exc:
            raise ValueError(f"{val} is not a valid number.") from exc