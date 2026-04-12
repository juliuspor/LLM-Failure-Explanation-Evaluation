@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # For lengths greater than 2, position 2 must be the separator
    if length < 4 or locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now lengths 4 and above have an underscore at index 2.
    # Expecting country at 3-4 for length >=5
    if length == 4:
        # Too short to contain a 2-letter country
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate country letters exist
    if length >= 5:
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length >=6 -> expect underscore at position 5 and variant after
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Variant may be empty or any length >=0, but original logic expects >=7 for non-empty variant
    variant = locale_str[6:]
    return Locale(locale_str[0:2], locale_str[3:5], variant)