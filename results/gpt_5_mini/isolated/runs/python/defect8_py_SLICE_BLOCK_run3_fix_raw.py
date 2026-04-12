@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # valid lengths: 2 (language), 5 (language_country), >=7 (language_country_variant)
        if length == 2:
            # validate language letters
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        # for longer forms, ensure minimum structure
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # position 2 must be underscore
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # ensure we have chars at 3 and 4 for country
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        # accept either upper or lower case letters for country
        if not (('A' <= ch3 <= 'Z' or 'a' <= ch3 <= 'z') and ('A' <= ch4 <= 'Z' or 'a' <= ch4 <= 'z')):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = (ch3 + ch4).upper()
        if length == 5:
            return Locale(locale_str[0:2], country)
        # now length >= 7 for variant form
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], country, variant)