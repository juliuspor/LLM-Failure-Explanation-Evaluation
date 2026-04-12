@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)

    # language only: "en"
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # must be at least language + '_' + country (5) to proceed
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # common check: underscore at position 2
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # country must be two uppercase letters at positions 3 and 4
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language + country only: "en_GB"
    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # variant forms must have another underscore at position 5
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # variant may be any non-empty string following the second underscore
    if length == 6:
        # empty variant is not allowed
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])