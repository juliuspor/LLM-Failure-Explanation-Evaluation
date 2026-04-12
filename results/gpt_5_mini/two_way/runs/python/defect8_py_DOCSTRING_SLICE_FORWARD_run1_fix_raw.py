@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Valid forms: ll, ll_CC, ll_CC_variant (ll=2 letters, CC=2 letters)
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # For lengths >=3 must have '_' at position 2
    if length < 5 or locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now we expect at least positions 3 and 4 for country
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length >= 6: expect underscore at position 5
    if length < 7 or locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # variant is remainder starting at position 6 and must be non-empty
    variant = locale_str[6:]
    if not variant:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], variant)