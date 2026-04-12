@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)

    # Accept lengths: 2 (language), 5 (language_country), or >=7 (language_country_variant)
    if length == 2:
        # language only: must be two lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    if length == 5:
        # expected form: ll_CC
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z' and 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5])

    if length >= 7:
        # expected form: ll_CC_variant (variant may be any length >=1)
        if locale_str[2] != '_' or locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z' and 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        # variant may contain underscores; take substring from index 6 to end
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], variant)

    # Any other lengths are invalid
    raise ValueError(f"Invalid locale format: {locale_str}")