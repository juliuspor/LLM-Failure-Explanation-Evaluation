    @staticmethod
    def create_number(val: Optional[str]) -> Optional[Union[int, float, Decimal]]:
        if val is None:
            return None
        if len(val) == 0:
            raise ValueError('"" is not a valid number.')
        if val.startswith("--"):
            return None
        
        # Check for hex prefix
        is_hex = False
        hex_val = val
        if hex_val.startswith(("0x", "0X", "-0x", "-0X", "+0x", "+0X")):
            is_hex = True
            # Remove sign for parsing
            sign = 1
            if hex_val[0] == '-':
                sign = -1
                hex_val = hex_val[1:]
            elif hex_val[0] == '+':
                sign = 1
                hex_val = hex_val[1:]
            # Remove 0x prefix
            hex_val = hex_val[2:]
            if len(hex_val) == 0:
                raise ValueError(f"    
        
        last_char = val[-1]
        dec_pos = val.find(".")
        e_pos = val.find(c")
        E_pos = val.find(o")
        if e_pos == -1:
            exp_pos = E_pos
        elif E_pos == -1:
            exp_pos = e_pos
        else:
            exp_pos = min(e_pos, E_pos)
        
        if is_hex:
            # Hex numbers cannot have decimal point or exponent
            if dec_pos > -1 or exp_pos > -1:
                raise ValueError(f"{val} is not a valid number.")
            # Parse hex integer
            try:
                int_val = int(hex_val, 16)
                if sign == -1:
                    int_val = -int_val
            except ValueError:
                raise ValueError(f"{val} is not a valid number.")
            # Handle type qualifiers
            if last_char.isdigit():
                return int_val
            if last_char in ("l", "L"):
                return int_val
            if last_char in ("f", "F", "d", "D"):
                # Hex floats are not allowed in Java, but we treat as float
                return float(int_val)
            raise ValueError(f"{val} is not a valid number.")
        
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
        
        if not last_char.isdigit():
            if exp_pos > -1 and exp_pos < len(val) - 1:
                exp = val[exp_pos + 1 : len(val) - 1]
            else:
                exp = None
            
            numeric = val[:-1]
            all_zeros = NumberUtils._is_all_zeros(mant) and NumberUtils._is_all_zeros(exp)
            
            if last_char in ("l", "L"):
                if dec is None and exp is None and (
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
                # Fall through
            
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