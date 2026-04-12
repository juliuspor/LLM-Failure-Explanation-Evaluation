@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Language only: 2 letters
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # Must at least be of the form aa_BB (length >=5) for country or aa_BB_xxx (>=7) for variant
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Check separator after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate country code positions exist and are uppercase letters
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Language + country only
    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # Variant form must have another '_' at position 5 and at least one variant char
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])