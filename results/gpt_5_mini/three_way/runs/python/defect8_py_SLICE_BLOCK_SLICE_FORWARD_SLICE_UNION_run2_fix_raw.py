@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # Allowed forms: "ll" (2), "ll_CC" (5), "ll_CC_variant" (>=7)
        if length == 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")

        # For any longer form, must have at least pattern ll_CC (length >=5)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Validate language letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Position 2 must be '_'
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Ensure there are country letters at 3 and 4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")

        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])

        # For variants, position 5 must be '_', and there must be at least one char after
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")

        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])