@staticmethod
def create_number(val: Optional[str]) -> Optional[Union[int, float, Decimal]]:
    if val is None:
        return None
    if len(val) == 0:
        raise ValueError('"" is not a valid number.')
    if val.startswith("--"):
        return None

    # Handle hex (0x or -0x or +0x) upfront: must be integer
    if val.startswith(("0x", "-0x", "+0x")):
        return NumberUtils.create_integer(val)

    last_char = val[-1]

    # Determine exponent position robustly
    dec_pos = val.find('.')
    e_pos = val.find('e')
    E_pos = val.find('E')
    if e_pos == -1:
        exp_pos = E_pos
    elif E_pos == -1:
        exp_pos = e_pos
    else:
        exp_pos = min(e_pos, E_pos)

    # Split mantissa and decimal part
    if dec_pos > -1:
        if exp_pos > -1 and exp_pos < dec_pos:
            # exponent before decimal point is invalid
            raise ValueError(f"{val} is not a valid number.")
        if exp_pos > -1:
            dec = val[dec_pos + 1:exp_pos]
        else:
            dec = val[dec_pos + 1:]
        mant = val[:dec_pos]
    else:
        dec = None
        if exp_pos > -1:
            mant = val[:exp_pos]
        else:
            mant = val

    # If last char is a type qualifier, validate core
    if not last_char.isdigit():
        # Core is value without qualifier
        core = val[:-1]

        # For hex with qualifier (e.g., 0x1fL) ensure hex goes to integer
        if core.startswith(("0x", "-0x", "+0x")):
            # Only allow integer qualifier L
            if last_char in ("l", "L"):
                return NumberUtils.create_integer(core)
            raise ValueError(f"{val} is not a valid number.")

        # Exponent part (without qualifier)
        if exp_pos > -1 and exp_pos < len(core) - 1:
            exp = core[exp_pos + 1:]
        else:
            exp = None

        all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)

        if last_char in ("l", "L"):
            # Long: only accept integer form (no decimal point, no exponent)
            if dec is None and exp is None and ((char_at(core, 0) == "-" and NumberUtils.is_digits(core[1:])) or NumberUtils.is_digits(core)):
                try:
                    return NumberUtils.create_long(core)
                except ValueError:
                    return NumberUtils.create_big_integer(core)
            raise ValueError(f"{val} is not a valid number.")

        if last_char in ("f", "F"):
            # Float qualifier: try float, then double/Decimal
            try:
                f = NumberUtils.create_float(core)
                if math.isfinite(f) and not (f == 0.0 and not all_zeros):
                    return f
            except Exception:
                pass
            # fall through to double/decimal

        if last_char in ("d", "D", "f", "F"):
            try:
                d = NumberUtils.create_double(core)
                if math.isfinite(d) and not (d == 0.0 and not all_zeros):
                    return d
            except Exception:
                pass
            try:
                return NumberUtils.create_big_decimal(core)
            except InvalidOperation:
                raise ValueError(f"{val} is not a valid number.")

        raise ValueError(f"{val} is not a valid number.")

    # No type qualifier on last char
    if exp_pos > -1 and exp_pos < len(val) - 1:
        exp = val[exp_pos + 1:]
    else:
        exp = None

    # If no decimal and no exponent, try integer parsing
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
    except Exception:
        pass
    try:
        d = NumberUtils.create_double(val)
        if math.isfinite(d) and not (d == 0.0 and not all_zeros):
            return d
    except Exception:
        pass
    try:
        return NumberUtils.create_big_decimal(val)
    except InvalidOperation as exc:
        raise ValueError(f"{val} is not a valid number.") from exc