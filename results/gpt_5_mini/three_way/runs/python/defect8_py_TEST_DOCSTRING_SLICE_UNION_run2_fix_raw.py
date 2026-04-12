@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # language must be two lowercase letters
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # only language
        if length == 2:
            return Locale(locale_str, "")

        # must have an underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # If string is only "xx_" it's invalid
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Handle empty country: pattern xx__variant
        if locale_str[3] == '_':
            # variant must exist after the double underscore
            if length == 4:
                raise ValueError(f"Invalid locale format: {locale_str}")
            # variant is the remainder
            return Locale(locale_str[0:2], "", locale_str[4:])

        # Otherwise, expect two-letter country starting at positions 3 and 4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # language_country only
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])

        # must have underscore before variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 6:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])