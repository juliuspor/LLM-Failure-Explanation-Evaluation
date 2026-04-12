@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Valid lengths: 2 ("ll"), 5 ("ll_CC"), >=7 ("ll_CC_xxx")
    if length == 2:
        # verify language is two lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # For lengths >=5 ensure there's an underscore at position 2 and at least positions 3 and 4 exist
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now safe to access ch3 and ch4
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length >= 6: must have underscore at position 5 for variant forms and at least one char in variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length == 6:
        # Nothing after the underscore -> invalid
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])