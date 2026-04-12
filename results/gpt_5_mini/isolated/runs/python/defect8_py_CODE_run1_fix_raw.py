@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # Accept lengths of 2 (language), 5 (language_country) or >=7 (language_country_variant)
        if not (length == 2 or length == 5 or length >= 7):
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Validate language: first two chars must be letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not (ch0.isalpha() and ch1.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Normalize language to lower-case when creating Locale
        language = locale_str[0:2].lower()
        if length == 2:
            return Locale(language, "")
        # Must have underscore separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Validate country: positions 3 and 4 must be letters
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not (ch3.isalpha() and ch4.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5].upper()
        if length == 5:
            return Locale(language, country)
        # For variant, must have underscore at position 5
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        return Locale(language, country, variant)