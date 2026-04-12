@staticmethod
def create_number(val: Optional[str]) -> Optional[Union[int, float, Decimal]]:
    if val is None:
        return None
    if len(val) == 0:
        raise ValueError('\"\" is not a valid number.')
    if val.startswith("--"):
        return None

    # Handle hex with optional sign
    sign_prefix = ''
    rest = val
    if rest[0] in ('+', '-') and len(rest) > 1:
        sign_prefix = rest[0]
        rest = rest[1:]
    if rest.startswith(('0x', '0X')):
        return NumberUtils.create_integer(val)

    last_char = val[-1]
    dec_pos = val.find('.')
    e_pos = val.find('e')
    E_pos = val.find('E')
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
            dec = val[dec_pos + 1:exp_pos]
        else:
            dec = val[dec_pos + 1:]
        mant = val[:dec_pos]
    else:
        if exp_pos > -1:
            mant = val[:exp_pos]
        else:
            mant = val
        dec = None

    def _is_all_zeros_local(s: Optional[str]) -> bool:
        if s is None:
            return True
        if len(s) == 0:
            return True
        for ch in s:
            if ch != '0':
                return False
        return True

    if not last_char.isdigit():
        if exp_pos > -1 and exp_pos < len(val) - 1:
            exp = val[exp_pos + 1:len(val) - 1]
        else:
            exp = None

        numeric = val[:-1]
        all_zeros = _is_all_zeros_local(mant) and _is_all_zeros_local(exp)

        if last_char in ('l', 'L'):
            if dec is None and exp is None:
                num = numeric
                if len(num) > 0 and num[0] in ('+', '-'):
                    sign = num[0]
                    num_body = num[1:]
                else:
                    num_body = num
                if len(num_body) > 0 and NumberUtils.is_digits(num_body):
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
            except (ValueError, TypeError):
                pass

        if last_char in ('d', 'D', 'f', 'F'):
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

    all_zeros = _is_all_zeros_local(mant) and _is_all_zeros_local(exp)
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
