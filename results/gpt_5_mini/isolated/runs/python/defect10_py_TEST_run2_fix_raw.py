@staticmethod
def create_number(val: Optional[str]) -> Optional[Union[int, float, Decimal]]:
    if val is None:
        return None
    s = val.strip()
    if len(s) == 0:
        raise ValueError('"" is not a valid number.')
    if s.startswith("--"):
        return None
    # Handle hex (0x, -0x, +0x) early
    if s.startswith(("0x", "-0x", "+0x")):
        return NumberUtils.create_integer(s)

    last_char = s[-1]
    dec_pos = s.find(".")
    e_pos = s.find("e")
    E_pos = s.find("E")
    if e_pos == -1:
        exp_pos = E_pos
    elif E_pos == -1:
        exp_pos = e_pos
    else:
        exp_pos = min(e_pos, E_pos)

    if dec_pos > -1:
        if exp_pos > -1:
            if exp_pos < dec_pos:
                raise ValueError(f"{s} is not a valid number.")
            dec = s[dec_pos + 1 : exp_pos]
        else:
            dec = s[dec_pos + 1 :]
        mant = s[:dec_pos]
    else:
        if exp_pos > -1:
            mant = s[:exp_pos]
        else:
            mant = s
        dec = None

    # If last char is not digit, it may be a type qualifier
    if not last_char.isdigit():
        if len(s) == 1:
            raise ValueError(f"{s} is not a valid number.")
        # numeric part without the type qualifier
        numeric = s[:-1]
        if len(numeric) == 0:
            raise ValueError(f"{s} is not a valid number.")

        all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(
            (s[exp_pos + 1 : len(s) - 1]) if exp_pos > -1 and exp_pos < len(s) - 1 else None
        )

        if last_char in ("l", "L"):
            # Only integer (no decimal or exponent) allowed
            if dec is None and exp_pos == -1:
                try:
                    return NumberUtils.create_integer(numeric)
                except ValueError:
                    return NumberUtils.create_big_integer(numeric)
            raise ValueError(f"{s} is not a valid number.")

        if last_char in ("f", "F"):
            try:
                f = NumberUtils.create_float(numeric)
                if math.isfinite(f) and not (f == 0.0 and not all_zeros):
                    return f
            except (ValueError, TypeError):
                pass
            # fall through to double/decimal handling

        if last_char in ("d", "D", "f", "F"):
            try:
                d = NumberUtils.create_double(numeric)
                if math.isfinite(d) and not (d == 0.0 and not all_zeros):
                    return d
            except (ValueError, TypeError):
                pass
            try:
                return NumberUtils.create_big_decimal(numeric)
            except (InvalidOperation, ValueError):
                pass
            raise ValueError(f"{s} is not a valid number.")

        raise ValueError(f"{s} is not a valid number.")

    # last char is a digit
    if exp_pos > -1 and exp_pos < len(s) - 1:
        exp = s[exp_pos + 1 :]
    else:
        exp = None

    # No decimal point or exponent -> integer types
    if dec is None and exp is None:
        try:
            return NumberUtils.create_integer(s)
        except ValueError:
            pass
        try:
            return NumberUtils.create_long(s)
        except ValueError:
            pass
        return NumberUtils.create_big_integer(s)

    all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)
    try:
        f = NumberUtils.create_float(s)
        if math.isfinite(f) and not (f == 0.0 and not all_zeros):
            return f
    except (ValueError, TypeError):
        pass
    try:
        d = NumberUtils.create_double(s)
        if math.isfinite(d) and not (d == 0.0 and not all_zeros):
            return d
    except (ValueError, TypeError):
        pass
    try:
        return NumberUtils.create_big_decimal(s)
    except InvalidOperation as exc:
        raise ValueError(f"{s} is not a valid number.") from exc