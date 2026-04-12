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
    exp_pos = -1
    if e_pos == -1:
        exp_pos = E_pos
    elif E_pos == -1:
        exp_pos = e_pos
    else:
        exp_pos = min(e_pos, E_pos)

    # Extract mantissa (part before decimal or exponent)
    if dec_pos > -1 and (exp_pos == -1 or dec_pos < exp_pos):
        mant = val[:dec_pos]
        dec = val[dec_pos + 1:exp_pos] if exp_pos > -1 else val[dec_pos + 1:]
    else:
        mant = val[:exp_pos] if exp_pos > -1 else val
        dec = None

    if not last_char.isdigit():
        numeric = val[:-1]
        if exp_pos > -1 and exp_pos < len(numeric) - 1:
            exp_part = numeric[exp_pos + 1:]
        else:
            exp_part = None
        all_zeros = NumberUtils._is_all_zeros(mant) and (exp_part is None or NumberUtils._is_all_zeros(exp_part))

        if last_char in ("l", "L"):
            if dec is None and exp_pos == -1 and (
                (char_at(numeric, 0) == "-" and NumberUtils.is_digits(numeric[1:]))
                or NumberUtils.is_digits(numeric)
            ):
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
            # Fall through to double/decimal

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

    # Digit case
    if exp_pos > -1 and exp_pos < len(val) - 1:
        exp = val[exp_pos + 1:]
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

    all_zeros = NumberUtils._is_all_zeros(mant) and (exp is None or NumberUtils._is_all_zeros(exp))
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