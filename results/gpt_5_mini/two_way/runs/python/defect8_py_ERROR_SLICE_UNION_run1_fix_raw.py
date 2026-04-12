@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length != 2 and length != 5 and length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        else:
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Handle case with empty country: 'll__VARIANT'
            # If positions 3-4 are letters -> country present
            if length >= 5 and locale_str[3] >= 'A' and locale_str[3] <= 'Z' and locale_str[4] >= 'A' and locale_str[4] <= 'Z':
                # country present
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            else:
                # country empty, expect another '_' then variant
                if locale_str[3] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # format is 'll__variant'
                if length == 3:
                    # just 'll_' which is invalid
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], "", locale_str[4:])