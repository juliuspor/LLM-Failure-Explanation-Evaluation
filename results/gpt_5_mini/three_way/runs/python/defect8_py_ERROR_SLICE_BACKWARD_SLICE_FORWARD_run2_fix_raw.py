@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # minimal language length is 2
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # language must be two lowercase letters
        if length < 2 or locale_str[0] < 'a' or locale_str[0] > 'z' or locale_str[1] < 'a' or locale_str[1] > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # only language (2 chars)
        if length == 2:
            return Locale(locale_str[0:2], "")
        # must have an underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # find next underscore if any (separates country and variant)
        # country may be empty (e.g., 'fr__POSIX')
        # Locale formats supported: ll, ll_CC, ll__VAR, ll_CC_VAR
        # extract country (positions 3 and 4 if present)
        # If no more characters after the underscore -> invalid
        if length == 3:
            # string ends with 'll_'
            raise ValueError(f"Invalid locale format: {locale_str}")
        # if there is another underscore at pos 3, country is empty
        if locale_str[3] == '_':
            country = ""
            # variant starts at pos 4
            variant = locale_str[4:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], country, variant)
        # otherwise expect two-letter country code at pos 3 and 4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5]
        if length == 5:
            return Locale(locale_str[0:2], country)
        # if more, expect underscore then variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], country, variant)