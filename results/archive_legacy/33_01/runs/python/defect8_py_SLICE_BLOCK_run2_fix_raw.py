@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    if isinstance(locale_str, (bytes, bytearray)):
        locale_str = locale_str.decode('utf-8')
    length = len(locale_str)
    if length != 2 and length != 5 and length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if not (isinstance(ch0, str) and isinstance(ch1, str)):
        ch0 = chr(ch0) if isinstance(ch0, int) else str(ch0)
        ch1 = chr(ch1) if isinstance(ch1, int) else str(ch1)
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length == 2:
        return Locale(locale_str, "")
    else:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not (isinstance(ch3, str) and isinstance(ch4, str)):
            ch3 = chr(ch3) if isinstance(ch3, int) else str(ch3)
            ch4 = chr(ch4) if isinstance(ch4, int) else str(ch4)
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])