@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # language must be two lower-case letters
        if length >= 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # From here on length >= 3
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Must have at least two characters for country
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        # length >= 6 -> may have variant but separator at pos 5 required
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Variant may be empty or longer; slicing from 6 is safe even if length==6 (results in empty string)
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])