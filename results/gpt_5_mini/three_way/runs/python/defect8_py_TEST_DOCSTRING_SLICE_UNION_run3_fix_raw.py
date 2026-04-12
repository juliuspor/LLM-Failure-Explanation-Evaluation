@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # language only: xx
        if length == 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")

        # must start with language and underscore
        if length < 4 or locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # validate language
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")

        # forms now: xx_... with length >=4
        # check for empty country: xx__variant
        if locale_str[3] == '_':
            # variant after position 3
            variant = locale_str[4:]
            if len(variant) == 0:
                # No country and no variant is invalid (xx__)
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", variant)

        # country should be two uppercase letters
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")

        # country only: xx_CC
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])

        # must be xx_CC_... for variants
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], variant)