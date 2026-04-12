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
        # We'll allow digits, decimal point, exponent, signs, and suffix letters.
        # But we must ensure that suffix letters are only at the end and are valid.
        # However, the existing logic already handles suffixes, but we need to ensure
        # that strings like "l" or "L" alone are rejected.
        # The original code had a bug where a single letter like "l" would pass
        # because it would be caught in the suffix handling but the numeric part would be empty.
        # Let's add a check: if the string consists only of a suffix letter, it's invalid.
        # Actually, the original code already does some checks, but we need to ensure
        # that the numeric part is present. The bug is that for input "l", the code
        # goes into the branch where last_char is not a digit, and then checks if last_char
        # is 'l' or 'L'. It then sets numeric = val[:-1] which is empty string.
        # Then it checks if dec is None and exp is None and ((char_at(numeric, 0) == "-" and NumberUtils.is_digits(numeric[1:])) or NumberUtils.is_digits(numeric)).
        # Since numeric is empty, char_at will raise IndexError, which is not caught and
        # propagates as IndexError, not ValueError. That's the bug.
        # We need to handle the case where numeric is empty (or the whole string is just a suffix).
        # Let's refactor the suffix handling to be more robust.
        # But to keep changes minimal, we can add a check for empty numeric before calling char_at.
        # However, the original code also has other issues: for "f" or "F" alone, it will try
        # to create_float("") which raises ValueError, but then falls through to double/decimal
        # and eventually raises ValueError. That's okay because ValueError is raised.
        # But for "l" alone, the IndexError is not caught. So we need to catch IndexError
        # and convert to ValueError.
        # Alternatively, we can restructure the logic to avoid char_at call on empty string.
        # Let's do a minimal fix: wrap the char_at call in a try-except IndexError and raise ValueError.
        # However, the char_at function already raises IndexError with a custom message.
        # We can catch IndexError in the create_number method and raise ValueError.
        # But the char_at function is used elsewhere? Only in create_number. So we can change char_at
        # to return a sentinel? Better to adjust the logic in create_number.
        # Let's change the condition: if numeric is empty, then it's invalid.
        # Actually, the condition already includes NumberUtils.is_digits(numeric). For empty string,
        # is_digits returns False. So the condition will be false, and we go to the raise ValueError.
        # Wait: the condition is:
        # if last_char in ("l", "L"):
        #     if dec is None and exp is None and (
        #         (char_at(numeric, 0) == "-" and NumberUtils.is_digits(numeric[1:]))
        #         or NumberUtils.is_digits(numeric)
        #     ):
        #         ...
        #     else:
        #         raise ValueError(...)
        # So if numeric is empty, char_at(numeric, 0) will raise IndexError before evaluating the OR.
        # So we need to avoid calling char_at on empty string. Let's restructure that condition.
        # We'll check if numeric is empty, then it's invalid. Also, if numeric starts with '-', we need to check the rest.
        # Let's rewrite that block.
        # But note: the original code also has a similar issue for other suffixes? For 'f' and 'd', it doesn't use char_at.
        # So we only need to fix the 'l'/'L' branch.
        # Let's do a targeted fix.

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
                    # Check if numeric is a valid integer (possibly with sign).
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