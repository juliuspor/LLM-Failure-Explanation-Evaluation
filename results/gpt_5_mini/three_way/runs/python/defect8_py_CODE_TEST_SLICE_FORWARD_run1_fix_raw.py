@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Minimum is 2 (language). Accept longer forms; further checks validate format.
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language must be two lowercase letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if not ('a' <= ch0 <= 'z') or not ('a' <= ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")

    # must have underscore after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Cases:
    # 1) language + '_' + country (2 letters) -> total length 5
    # 2) language + '__' + variant (empty country) -> at least length 4+ (variant may be length >=1)
    # 3) language + '_' + country + '_' + variant -> at least length 7

    # Empty country: locale_str[3] == '_'
    if length >= 4 and locale_str[3] == '_':
        # variant must exist
        if length == 4:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # variant starts at index 4
        variant = locale_str[4:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], "", variant)

    # Non-empty country: need two uppercase letters at positions 3 and 4
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z') or not ('A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    country = locale_str[3:5]
    if length == 5:
        return Locale(locale_str[0:2], country)

    # expect underscore before variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    variant = locale_str[6:]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(locale_str[0:2], country, variant)