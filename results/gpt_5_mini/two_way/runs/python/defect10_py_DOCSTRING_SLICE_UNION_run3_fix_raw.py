@staticmethod
def create_number(val: Optional[str]) -> Optional[Union[int, float, Decimal]]:
    if val is None:
        return None
    if len(val) == 0:
        raise ValueError('"" is not a valid number.')
    if val.startswith("--"):
        return None
    # handle hex prefixes with optional sign
    if val.startswith(("0x", "-0x", "+0x")):
        return NumberUtils.create_integer(val)

    last_char = val[-1]
    dec_pos = val.find(".")
    # find exponent position robustly
    e_pos = val.find("e")
    E_pos = val.find("E")
    if e_pos == -1:
        exp_pos = E_pos
    elif E_pos == -1:
        exp_pos = e_pos
    else:
        exp_pos = min(e_pos, E_pos)

    # determine mantissa and decimal parts safely
    if dec_pos > -1:
        if exp_pos > -1 and exp_pos < dec_pos:
            raise ValueError(f"{val} is not a valid number.")
        if exp_pos > -1:
            dec = val[dec_pos + 1:exp_pos]
            mant = val[:dec_pos]
        else:
            dec = val[dec_pos + 1:]
            mant = val[:dec_pos]
    else:
        dec = None
        if exp_pos > -1:
            mant = val[:exp_pos]
        else:
            mant = val

    # helper to check exponent substring when last char is a type qualifier
    if not last_char.isdigit():
        if exp_pos > -1 and exp_pos < len(val) - 1:
            exp = val[exp_pos + 1:len(val) - 1]
        else:
            exp = None

        numeric = val[:-1]
        all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)

        if last_char in ("l", "L"):
            # ensure numeric is a valid integer literal
            if dec is None and exp is None:
                if len(numeric) > 0:
                    if numeric[0] == "-":
                        if NumberUtils.is_digits(numeric[1:]):
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
            except (ValueError, TypeError):
                pass
            # fall through

        if last_char in ("d", "D", "f", "F"):
            try:
                d = NumberUtils.create_double(numeric)
                if math.isfinite(d) and not (d == 0.0 and not all_zeros):
                    return d
            except (ValueError, TypeError):
                pass
            try:
                return NumberUtils.create_big_decimal(numeric)
            except InvalidOperation:
                pass
            raise ValueError(f"{val} is not a valid number.")

        raise ValueError(f"{val} is not a valid number.")

    # last char is digit
    if exp_pos > -1 and exp_pos < len(val) - 1:
        exp = val[exp_pos + 1:]
    else:
        exp = None

    # if no decimal point or exponent, try integer types
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
    except (ValueError, TypeError):
        pass
    try:
        d = NumberUtils.create_double(val)
        if math.isfinite(d) and not (d == 0.0 and not all_zeros):
            return d
    except (ValueError, TypeError):
        pass
    try:
        return NumberUtils.create_big_decimal(val)
    except InvalidOperation as exc:
        raise ValueError(f"{val} is not a valid number.") from exc