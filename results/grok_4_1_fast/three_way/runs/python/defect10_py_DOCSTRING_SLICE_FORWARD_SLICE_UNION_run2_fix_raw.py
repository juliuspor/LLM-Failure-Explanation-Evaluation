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
    numeric = val[:-1] if not last_char.isdigit() else val
    
    # Find exponent position
    e_pos = val.find("e")
    E_pos = val.find("E")
    exp_pos = max(e_pos, E_pos) if e_pos > -1 or E_pos > -1 else -1
    
    # Check for decimal point
    dec_pos = val.find(".")
    has_dec = dec_pos > -1
    
    # Handle type qualifiers
    if not last_char.isdigit():
        if last_char in ("l", "L"):
            if not has_dec and exp_pos == -1:
                if (char_at(numeric, 0) == "-" and NumberUtils.is_digits(numeric[1:])) or NumberUtils.is_digits(numeric):
                    try:
                        return NumberUtils.create_long(numeric)
                    except ValueError:
                        return NumberUtils.create_big_integer(numeric)
            raise ValueError(f"{val} is not a valid number.")
        
        if last_char in ("f", "F"):
            try:
                f = NumberUtils.create_float(numeric)
                if math.isfinite(f):
                    return f
            except ValueError:
                pass
        
        if last_char in ("d", "D", "f", "F"):
            try:
                d = NumberUtils.create_double(numeric)
                if math.isfinite(d):
                    return d
            except ValueError:
                pass
            try:
                return NumberUtils.create_big_decimal(numeric)
            except InvalidOperation:
                pass
            raise ValueError(f"{val} is not a valid number.")
        
        raise ValueError(f"{val} is not a valid number.")

    # No qualifier - try integer first
    if not has_dec and exp_pos == -1:
        try:
            return NumberUtils.create_integer(val)
        except ValueError:
            pass
        try:
            return NumberUtils.create_long(val)
        except ValueError:
            pass
        return NumberUtils.create_big_integer(val)

    # Floating point or decimal
    all_zeros = NumberUtils._is_all_zeros(val.replace('.', '').replace('e', '').replace('E', ''))
    
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