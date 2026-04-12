@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        if length != 2 and length != 5 and length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # basic language checks (must be two lowercase letters)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 2:
            return Locale(locale_str, "")
        # must have underscore at pos 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # find next underscore (start of variant) if any
        # possible forms: ll_CC, ll__VARIANT, ll_CC_VARIANT
        # If there is no further underscore, expect exactly 5 length (ll_CC)
        # If there is another underscore at pos 3 -> empty country
        if length >= 4 and locale_str[3] == '_':
            # form ll__variant
            variant = locale_str[4:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", variant)

        # otherwise expect country of length 2 at pos 3-4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])

        # length >=7, must have '_' at pos 5
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], variant)