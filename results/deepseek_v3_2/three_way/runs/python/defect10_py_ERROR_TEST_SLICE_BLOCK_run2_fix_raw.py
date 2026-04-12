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

        # Handle the case where mant or dec might be empty after splitting.
        # For example, val = "l" -> mant = "" (since no dec or exp), dec = None.
        # Then numeric = val[:-1] = "" and char_at(numeric, 0) will raise IndexError.
        # We need to ensure that before calling char_at, we check length.
        # But the main issue is that single-letter inputs like 'l' or 'L' are not numbers.
        # The Java implementation would throw NumberFormatException.
        # We should detect early that if the string consists only of a non-digit suffix,
        # it's invalid.
        # However, the existing logic already checks last_char.isdigit() and then processes.
        # For 'l', last_char is 'l' (not digit), so it goes into the non-digit branch.
        # In that branch, numeric = val[:-1] = "". Then char_at(numeric, 0) is called.
        # That's where the IndexError occurs. We need to avoid calling char_at on empty string.
        # Instead, we should check if numeric is empty and raise ValueError.
        # Also, we need to ensure that the condition for 'l' or 'L' handles empty numeric.
        # Let's modify the branch for last_char in ('l','L'):
        #   if dec is None and exp is None and (
        #       (len(numeric) > 0 and char_at(numeric, 0) == "-" and NumberUtils.is_digits(numeric[1:]))
        #       or NumberUtils.is_digits(numeric)
        #   )
        # But note: numeric could be empty, so we must check length.
        # Actually, the condition should be: numeric is not empty and either (numeric[0]=='-' and is_digits(numeric[1:])) or is_digits(numeric).
        # We'll adjust.
        # Also, for other suffixes (f, F, d, D), numeric might be empty, leading to create_float("") which raises ValueError.
        # That's fine because we catch ValueError and fall through.
        # But we should also guard against empty numeric in the 'l'/'L' branch to avoid IndexError.
        # Let's implement the fix.

        if not last_char.isdigit():
            if exp_pos > -1 and exp_pos < len(val) - 1:
                exp = val[exp_pos + 1 : len(val) - 1]
            else:
                exp = None

            numeric = val[:-1]
            all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)

            if last_char in ("l", "L"):
                if dec is None and exp is None:
                    # Check if numeric is empty or not a valid integer.
                    if len(numeric) == 0:
                        raise ValueError(f"{val} is not a valid number.")
                    # Now check if numeric is a valid integer (with optional sign).
                    if (numeric[0] == "-" and NumberUtils.is_digits(numeric[1:])) or NumberUtils.is_digits(numeric):
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