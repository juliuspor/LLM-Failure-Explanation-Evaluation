@staticmethod
def create_number(val: Optional[str]) -> Optional[Union[int, float, Decimal]]:
    if val is None:
        return None
    if len(val) == 0:
        raise ValueError('"" is not a valid number.')
    if val.startswith("--"):
        return None

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

    # suffix handling
    if last_char in ("l", "L", "f", "F", "d", "D"):
        numeric = val[:-1]
        # recompute exponent part for suffix handling
        if exp_pos > -1 and exp_pos < len(val) - 1:
            exp = val[exp_pos + 1 : len(val) - 1]
        else:
            exp = None

        all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)

        if last_char in ("l", "L"):
            # integer type suffix
            if dec is None and exp is None:
                try:
                    return NumberUtils.create_integer(numeric)
                except ValueError:
                    try:
                        return NumberUtils.create_long(numeric)
                    except ValueError:
                        return NumberUtils.create_big_integer(numeric)
            raise ValueError(f"{val} is not a valid number.")

        # floating‑point suffixes
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

    # no suffix – handle exponent (if present)
    if exp_pos > -1 and exp_pos < len(val) - 1:
        exp = val[exp_pos + 1 :]
    else:
        exp = None

    # plain integer (no decimal, no exponent)
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

    # decimal and/or exponent present
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
