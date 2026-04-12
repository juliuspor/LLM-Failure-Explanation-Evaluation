@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # valid lengths are 2 (language), 5 (language_country), or >=7 (language_country_variant)
        if length == 2:
            # simple language code
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")

        # For longer forms, position 2 must be '_'
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # validate language
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # now ensure we have at least two chars for country
        if length >= 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")

            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])

        # length >= 6 here, country validated; position 5 must be '_' and variant follows
        if length < 7:
            # length 6 is invalid because variant must have at least 1 char after underscore
            raise ValueError(f"Invalid locale format: {locale_str}")
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # variant may be any string (including characters of any case)
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])