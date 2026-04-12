    @classmethod
    def to_locale(cls, locale_str: str) -> Locale:
        """
        Obtains the list of languages supported for a given country.
        """
        if locale_str is None:
            return None
        length = len(locale_str)
        if length == 2:
            # Just language code
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "", "")
        elif length == 5:
            # Language and country code
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z' and 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], "")
        elif length >= 7:
            # Language, country, and variant
            if locale_str[2] != '_' or locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z' and 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            if not variant:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], variant)
        else:
            # Length 0,1,3,4,6
            raise ValueError(f"Invalid locale format: {locale_str}")