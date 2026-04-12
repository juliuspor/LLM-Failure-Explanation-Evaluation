@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length != 2 and length != 5 and length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language (first two chars must be lowercase letters)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")

    # From here length >= 5 or >=7 depending; position 2 must be '_'
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Handle the case language__variant (empty country)
    # That means positions 2 and 3 are '_' and variant starts at pos 4
    if length >= 4 and locale_str[3] == '_':
        # Variant may be empty or non-empty; variant starts at pos 4
        variant = locale_str[4:]
        return Locale(locale_str[0:2], "", variant)

    # Otherwise, expect a two-letter country at positions 3 and 4
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length > 5: expect '_' at position 5 separating country and variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])