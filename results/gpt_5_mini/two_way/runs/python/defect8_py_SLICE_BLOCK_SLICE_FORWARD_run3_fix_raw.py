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
        # For forms longer than 2, we require at least positions 2,3,4 to exist
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Check separator at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Validate country letters at 3 and 4
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        # length >= 6
        # For variant form we expect an underscore at position 5 and at least one char in variant
        if length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # variant may be any length >=1
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])