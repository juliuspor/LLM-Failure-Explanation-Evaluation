@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # Basic validity: must be at least 2 chars (language)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # language must be two lowercase letters
        if length >= 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")

        # Exact language only
        if length == 2:
            return Locale(locale_str, "")

        # Must have separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # language_country (length == 5)
        if length == 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])

        # language_country_variant (length >= 7, with '_' at pos 5)
        if length >= 7:
            # ensure country chars exist and are uppercase letters
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])

        # Any other length is invalid
        raise ValueError(f"Invalid locale format: {locale_str}")