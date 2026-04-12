@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language: first two chars must be lowercase a-z
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If only language
    if length == 2:
        return Locale(locale_str, "")

    # Must have underscore after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Handle possible empty country (underscore at position 3)
    # Determine country and variant based on underscores
    # Cases:
    # en_US -> length ==5, country at 3-4
    # en__POSIX -> country empty, variant starts at 4
    # en_US_POSIX -> country at 3-4, variant starts at 6

    # If no more characters after 'lang_'
    if length == 3:
        # "en_" is invalid
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Check if country is empty
    if locale_str[3] == '_':
        country = ""
        # Variant starts at position 4 (after the second underscore)
        variant = locale_str[4:]
        if len(variant) == 0:
            # No variant provided (string like 'en__') is invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], country, variant)
    else:
        # Expect two uppercase letters for country
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5]
        if length == 5:
            return Locale(locale_str[0:2], country)
        # Must have underscore before variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], country, variant)