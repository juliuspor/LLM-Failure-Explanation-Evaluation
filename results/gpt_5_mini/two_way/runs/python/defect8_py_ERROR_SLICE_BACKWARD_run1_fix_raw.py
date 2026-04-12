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

        # Handle cases like 'fr__POSIX' (empty country, variant present)
        # or standard 'en_GB' / 'en_GB_variant'
        # If position 3 is '_' then country is empty and variant starts at pos 3+1?
        # According to examples, 'fr__POSIX' has '_' at pos2 and pos3, variant starts at pos4
        # In our indexing: 0 1 2 3 4 ... so for 'fr__POSIX', pos2='_' pos3='_' variant starts at 4.
        if length >= 5 and locale_str[3] == '_':
            # country is empty, variant starts at position 4
            if length == 4:
                # 'xx_' is invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", locale_str[4:])

        # Otherwise expect two-letter uppercase country at positions 3 and 4
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