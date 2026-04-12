@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # length must be 2 (language), 5 (language_country) or >=7 (language_country_variant)
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # For any longer string, position 2 must be '_'
    if length < 5:
        # lengths 3 and 4 are invalid (e.g., "en_" or "en_G")
        raise ValueError(f"Invalid locale format: {locale_str}")

    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now we know indices 3 and 4 exist (since length >=5)
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # For variants, we require length >=7 (i.e., at least one variant char after second underscore)
    if length < 7:
        # length == 6 is invalid (e.g., "en_GB_")
        raise ValueError(f"Invalid locale format: {locale_str}")

    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # variant is the substring from index 6 to end; it must be non-empty
    variant = locale_str[6:]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], variant)