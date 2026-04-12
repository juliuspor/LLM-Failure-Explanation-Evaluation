@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # language must be two lowercase letters
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z') or not ('a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # must have at least one separator at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Handle language__variant (empty country)
        if length >= 4 and locale_str[3] == '_':
            # variant follows starting at index 4
            if length == 4:
                # "xx__" is invalid (empty variant)
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", locale_str[4:])
        # Otherwise expect country in positions 3-4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('A' <= ch3 <= 'Z') or not ('A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        # length > 5, expect '_' at position 5 and variant after
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 6:
            # "xx_YY_" is invalid (empty variant)
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])