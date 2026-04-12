@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    length = len(locale_str)
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    region = locale_str[3:5]
    if len(region) != 2 or region[0] < 'A' or region[0] > 'Z' or region[1] < 'A' or region[1] > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length == 5:
        return Locale(locale_str[0:2], region)
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    variant = locale_str[6:]
    return Locale(locale_str[0:2], region, variant)