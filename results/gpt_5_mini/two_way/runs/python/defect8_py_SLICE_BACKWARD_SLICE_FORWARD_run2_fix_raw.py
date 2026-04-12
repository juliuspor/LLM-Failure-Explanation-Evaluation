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

        # For lengths other than 2, the minimum valid length is 5 (ll_CC) or 7 (ll_CC_v)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Validate language part (first two chars)
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Expect underscore at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Handle the ll_CC (length == 5) case
        if length == 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])

        # For length >= 7, expect ll_CC_v... where position 5 is '_' and variant follows
        if length >= 7:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], variant)

        # Any other cases are invalid
        raise ValueError(f"Invalid locale format: {locale_str}")