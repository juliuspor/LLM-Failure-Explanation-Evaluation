@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Basic validation: must have at least a 2-letter language
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language (first two chars)
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If only language present
    if length == 2:
        return Locale(locale_str, "")

    # From here, expect an underscore separator
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If exactly 3 chars or 4 chars, invalid
    if length == 3 or length == 4:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # At position 3 and 4 we may have country or may be underscores if empty country
    # If there is a second underscore at position 3, treat country as empty and rest as variant
    if locale_str[3] == '_':
        # Format like ll__variant (empty country)
        # Variant must exist after the second underscore
        if length <= 4:
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[4:]
        if not variant:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], "", variant)

    # Otherwise parse country from positions 3-4
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    country = locale_str[3:5]

    if length == 5:
        return Locale(locale_str[0:2], country)

    # If more, expect underscore then variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant = locale_str[6:]
    if not variant:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], country, variant)