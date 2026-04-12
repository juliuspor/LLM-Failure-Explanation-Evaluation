@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # Valid lengths: 2 (language), 5 (language_country), >=7 (language_country_variant)
        if length == 2:
            # language only: must be 2 lowercase letters
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")

        # For other lengths, minimum expected is 5 (xx_YY)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Ensure separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Validate language letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Now handle country and optional variant
        # Country must be two uppercase letters at positions 3 and 4
        if length >= 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])

        # length >= 6: expect '_' at position 5 and variant after that
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Variant may be empty string technically, but require at least one char after underscore
        if length == 6:
            # no characters after second underscore
            raise ValueError(f"Invalid locale format: {locale_str}")

        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])