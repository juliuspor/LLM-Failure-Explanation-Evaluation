@staticmethod
def create_number(val: Optional[str]) -> Optional[Union[int, float, Decimal]]:
    if val is None:
        return None
    if len(val) == 0:
        raise ValueError('"" is not a valid number.')

    # single-char non-digit should raise
    if len(val) == 1 and not val[0].isdigit():
        raise ValueError(f"{val} is not a valid number.")

    if val.startswith("--"):
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

    # Handle trailing type qualifiers
    if not last_char.isdigit():
        # ensure there's at least something before the qualifier
        numeric = val[:-1]
        if len(numeric) == 0:
            raise ValueError(f"{val} is not a valid number.")

        # compute exp and dec parts for the numeric substring if needed
        # determine exp for numeric substring
        n_e_pos = numeric.find('e')
        n_E_pos = numeric.find('E')
        if n_e_pos == -1:
            n_exp_pos = n_E_pos
        elif n_E_pos == -1:
            n_exp_pos = n_e_pos
        else:
            n_exp_pos = min(n_e_pos, n_E_pos)

        # validate that numeric (before qualifier) is a valid number body
        # allow leading sign
        num_check = numeric
        if num_check.startswith(('+', '-')):
            if len(num_check) == 1:
                raise ValueError(f"{val} is not a valid number.")
            num_check = num_check[1:]

        # For hex-prefixed numbers, delegate to integer creator
        if num_check.startswith(('0x', '0X')):
            # but a qualifier after hex is invalid
            raise ValueError(f"{val} is not a valid number.")

        # simple validation: ensure at least one digit exists in numeric
        has_digit = any(ch.isdigit() for ch in num_check)
        if not has_digit:
            raise ValueError(f"{val} is not a valid number.")

        # Recompute mant/dec/exp for use in zero checks
        if dec is None:
            # dec was computed from original val; recompute from numeric
            if n_exp_pos > -1:
                n_dec = None
                n_mant = numeric[:n_exp_pos]
            else:
                # may contain a decimal
                n_dp = numeric.find('.')
                if n_dp > -1:
                    n_dec = numeric[n_dp+1:]
                    n_mant = numeric[:n_dp]
                else:
                    n_dec = None
                    n_mant = numeric
        else:
            n_dec = dec
            n_mant = mant

        all_zeros = NumberUtils._is_all_zeros(n_mant) and NumberUtils._is_all_zeros(n_exp_pos and numeric[n_exp_pos+1:] or None)

        if last_char in ('l', 'L'):
            # only valid if integer style
            if n_dec is None and (n_exp_pos == -1):
                # allow leading sign
                to_parse = numeric
                if to_parse.startswith(('+', '-')):
                    if not NumberUtils.is_digits(to_parse[1:]):
                        raise ValueError(f"{val} is not a valid number.")
                else:
                    if not NumberUtils.is_digits(to_parse):
                        raise ValueError(f"{val} is not a valid number.")

                try:
                    return NumberUtils.create_long(numeric)
                except ValueError:
                    return NumberUtils.create_big_integer(numeric)
            raise ValueError(f"{val} is not a valid number.")

        if last_char in ('f', 'F'):
            try:
                f = NumberUtils.create_float(numeric)
                if math.isfinite(f) and not (f == 0.0 and not all_zeros):
                    return f
            except ValueError:
                pass
            # fall through to double/decimal

        if last_char in ('d', 'D', 'f', 'F'):
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

    # No trailing qualifier
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