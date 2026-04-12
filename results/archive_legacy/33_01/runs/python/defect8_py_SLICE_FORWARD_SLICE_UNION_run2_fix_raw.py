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
        return Locale(locale_str[0:2], "")
    if length == 5:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z' or ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5])
    if length >= 7:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z' or ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
    raise ValueError(f"Invalid locale format: {locale_str}")