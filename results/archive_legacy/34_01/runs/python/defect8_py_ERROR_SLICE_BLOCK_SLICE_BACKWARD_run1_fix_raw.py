@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length not in (2, 5) and length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length >= 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if not (ch0.isalpha() and ch1.isalpha() and ch0.islower() and ch1.islower()):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if not (ch3.isalpha() and ch4.isalpha() and ch3.isupper() and ch4.isupper()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])
        if locale_str[3] == '_':
            return Locale(locale_str[0:2], "", locale_str[4:])
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not (ch3.isalpha() and ch4.isalpha() and ch3.isupper() and ch4.isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])