    @classmethod
    def to_locale(cls, locale_str: Optional[str]) -> Optional[Locale]:
        """
        Convert a locale string to a Locale object.
        """
        if locale_str is None:
            return None
        length = len(locale_str)
        # Valid lengths: 2 (language), 5 (language_country), or >=7 (language_country_variant)
        if length not in (2, 5) and length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # length >=5
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        # length >=7
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        third_part = locale_str[6:]
        if not third_part:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], third_part)