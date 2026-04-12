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

        # Allow empty country (i.e., second underscore) as in "fr__POSIX"
        # If there is a second underscore at position 3, country is empty.
        if length >= 5 and locale_str[3] == '_':
            country = ""
            if length == 5:
                # form like "fr_" followed by nothing invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Expect underscore at position 4? In format fr__VARIANT, position 4 should be start of variant or underscore? 
            # Per patterns, for empty country the string should be like ll__VVV where locale_str[2]=='_' and locale_str[3]=='_'
            if locale_str[3] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Ensure there is an underscore separating empty country and variant at position 4? Actually positions: 0-1 lang, 2 '_', 3 '_' then variant starts at 4
            # So variant starts at index 4
            variant = locale_str[4:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], country, variant)
        else:
            # country is non-empty: positions 3-4 must be uppercase letters
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")

            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])