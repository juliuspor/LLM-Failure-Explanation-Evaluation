@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    if isinstance(locale_str, (bytes, bytearray)):
        try:
            locale_str = locale_str.decode('ascii')
        except Exception:
            raise ValueError(f"Invalid locale format: {locale_str}")
    if not isinstance(locale_str, str):
        raise ValueError(f"Invalid locale format: {locale_str}")
    length = len(locale_str)
    if length == 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")
    if length == 5:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z') or not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5])
    if length >= 7:
        if locale_str[2] != '_' or locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z') or not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
    raise ValueError(f"Invalid locale format: {locale_str}")