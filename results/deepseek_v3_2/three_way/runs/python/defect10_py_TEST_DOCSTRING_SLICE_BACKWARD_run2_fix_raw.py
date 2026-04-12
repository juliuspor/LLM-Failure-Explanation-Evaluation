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

        # Check for trailing qualifiers
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

        # Determine exponent part if present
        if exp_pos > -1 and exp_pos < len(val) - 1:
            exp = val[exp_pos + 1 :]
        else:
            exp = None

        # Handle trailing qualifiers
        if not last_char.isdigit():
            # For qualifiers, the numeric part is everything except the last character
            numeric = val[:-1]
            # Determine exponent part for qualifier case (if exponent exists before qualifier)
            if exp_pos > -1 and exp_pos < len(val) - 1:
                exp = val[exp_pos + 1 : -1]
            else:
                exp = None
            all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)

            if last_char in ("l", "L"):
                # Long qualifier: no decimal point, no exponent, numeric part must be digits (with optional sign)
                if dec is None and exp is None:
                    if (numeric.startswith("-") and NumberUtils.is_digits(numeric[1:])) or NumberUtils.is_digits(numeric):
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
                # Fall through to double/decimal cases

            if last_char in ("d", "D", "f", "F"):
                # Note: 'f' already handled above, but we keep for completeness
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

            # If last character is not a digit and not a known qualifier, it's invalid
            raise ValueError(f"{val} is not a valid number.")

        # No trailing qualifier
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