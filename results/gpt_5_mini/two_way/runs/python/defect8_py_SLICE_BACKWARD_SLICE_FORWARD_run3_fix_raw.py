@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # minimal valid lengths: 2 (language), 5 (language_country), 7+ (language_country_variant)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # validate language letters
        if length >= 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # for lengths >=3, expect underscore at pos 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # need at least positions 3 and 4 for country
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        # length > 5: expect another underscore at pos 5
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # variant may be empty or longer; allow empty variant (but original Java disallows empty?)
        # If length == 6, variant is empty string
        if length == 6:
            return Locale(locale_str[0:2], locale_str[3:5], "")
        # length >=7: safe to slice from pos 6 onward
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])