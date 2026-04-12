@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # language must be exactly 2 letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language
    if length >= 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
    else:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Only language
    if length == 2:
        return Locale(locale_str[0:2], "")

    # Must have '_' after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Ensure there are at least two characters for country
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Language + country
    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # There must be another '_' before variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Variant must be present (at least one char)
    if length <= 6:
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant = locale_str[6:]
    return Locale(locale_str[0:2], locale_str[3:5], variant)