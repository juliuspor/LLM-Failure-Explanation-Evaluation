@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language (first two chars)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")

    # From here length >= 3, next char must be '_'
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If length == 3 it's invalid (language + single underscore)
    if length == 3:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now handle two main forms after the initial language and underscore:
    # 1) language + '_' + country (2 letters) -> total length == 5
    # 2) language + '_' + country + '_' + variant -> length >= 7, country may be empty (i.e., language + '__' + variant)

    # Ensure we have at least positions 3 and 4 to check country when length >=5
    if length >= 5:
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        # country may be letters A-Z when present; if both '_' then it's empty country handled below
        if ch3 == '_' and ch4 == '_':
            # empty country, variant must follow starting at index 4 (since locale_str[3] is '_', locale_str[4] is '_')
            # variant will start at index 4+1 = 5, but since we had language(0-1), '_'(2), '_'(3), variant starts at 4? adjust:
            # positions: 0,1 language; 2 '_'; 3 '_' (empty country placeholder); 4 onwards variant -> so variant starts at index 4
            variant = locale_str[4:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", variant)
        else:
            # country is expected in positions 3 and 4 and must be uppercase A-Z
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = locale_str[3:5]

            if length == 5:
                return Locale(locale_str[0:2], country)

            # length >= 6: expect '_' at position 5 then variant at 6+
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], country, variant)

    # If we reach here, it's an invalid format
    raise ValueError(f"Invalid locale format: {locale_str}")