@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Only valid lengths are 2 (language), 5 (language_country), or >=7 (language_country_variant)
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # For lengths other than 2, we expect at least 5 characters (language + '_' + country)
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language first two chars
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Expect underscore at position 2 and country at 3-4
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Ensure we have country characters
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length >= 7 expected: underscore at pos 5 then variant starting at 6
    if length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])