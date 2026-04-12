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
    has_qualifier = not last_char.isdigit()
    numeric = val[:-1] if has_qualifier else val

    # Find exponent position (first 'e' or 'E')
    exp_pos = -1
    for i, c in enumerate(numeric):
        if c.lower() == 'e':
            exp_pos = i
            break

    # Find decimal position
    dec_pos = numeric.find(".")

    # Extract mantissa and fractional/exponent parts for all_zeros check
    if dec_pos > -1:
        mant = numeric[:dec_pos]
        if exp_pos > -1 and exp_pos > dec_pos:
            dec_part = numeric[dec_pos + 1:exp_pos]
            exp_part = numeric[exp_pos + 1:]
        else:
            dec_part = numeric[dec_pos + 1:]
            exp_part = None
    else:
        mant = numeric
        dec_part = None
        if exp_pos > -1:
            exp_part = numeric[exp_pos + 1:]
        else:
            exp_part = None

    all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(dec_part) and NumberUtils._is_all_zeros(exp_part)

    if has_qualifier:
        if last_char in ("l", "L"):
            if dec_pos == -1 and exp_pos == -1 and (
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

    # No qualifier - try integer first, then float/decimal
    if dec_pos == -1 and exp_pos == -1:
        try:
            return NumberUtils.create_integer(val)
        except ValueError:
            pass
        try:
            return NumberUtils.create_long(val)
        except ValueError:
            pass
        return NumberUtils.create_big_integer(val)

    # Has decimal or exponent - try float -> double -> decimal
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