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

    # More than 2 chars: expect an underscore after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If only language + underscore and nothing else -> invalid
    if length == 3:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Case: language + __ + variant (empty country)
    if locale_str[3] == '_':
        # variant must follow and be non-empty
        variant = locale_str[4:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], "", variant)

    # Otherwise expect two-letter country at positions 3 and 4
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # More than 5: expect underscore before variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant = locale_str[6:]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], variant)