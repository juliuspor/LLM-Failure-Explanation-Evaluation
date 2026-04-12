@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # Accept lengths: 2 (language), 5 (language_country), or >=7 (language__variant or language_country_variant)
        if not (length == 2 or length == 5 or length >= 7):
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # must have separator at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Handle empty country (double underscore) or two-letter country
        # Check if country is empty
        if locale_str[3] == '_':
            # empty country, variant must follow and be at least one character
            if length < 4 + 1:
                raise ValueError(f"Invalid locale format: {locale_str}")
            # variant starts at position 4
            variant = locale_str[4:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", variant)
        else:
            # expect two uppercase letters for country at positions 3 and 4
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            # length >= 7: must have underscore at position 5
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], variant)