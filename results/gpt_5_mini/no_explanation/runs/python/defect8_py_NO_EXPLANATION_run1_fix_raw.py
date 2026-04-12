@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Accept forms: ll, ll_CC, ll_CC_variant (where variant length >=1)
    if not (length == 2 or length == 5 or length >= 7):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language: two lowercase letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")

    # Must have underscore at position 2
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # length >= 7 -> must have underscore at position 5 and variant after position 6
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant = locale_str[6:]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], variant)