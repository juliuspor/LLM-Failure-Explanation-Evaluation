@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Must be at least 2
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Check language letters
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Only language ("en")
    if length == 2:
        return Locale(locale_str, "")

    # From here length >= 3: must have '_' at pos 2
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If length is 3 or 4 that's invalid (incomplete country)
    if length == 3 or length == 4:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now length >=5, check country letters at pos 3 and 4
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length >= 6: must have '_' at pos 5 to have variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Variant may be empty or any string; if empty, that's invalid in original semantics but allow empty? Keep original: slice from 6
    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])