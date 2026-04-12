@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Must be at least 2 characters for language
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language (first two chars must be lowercase letters)
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Language only
    if length == 2:
        return Locale(locale_str, "")

    # From here on length >= 3, expect '_' at position 2
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Need at least 5 chars for language_country form (e.g. en_GB)
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # From here on length >= 6, expect '_' at position 5 and variant after it
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant = locale_str[6:]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], variant)