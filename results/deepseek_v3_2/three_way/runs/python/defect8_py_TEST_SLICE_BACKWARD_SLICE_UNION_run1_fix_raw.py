    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        """
        Parse a locale string into a Locale object.
        Handles formats: language, language_country, language_country_variant, language__variant.
        """
        if locale_str is None:
            return None
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Validate first two characters as lowercase letters (language code)
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "", "")
        # Must have an underscore after the language code
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 3:
            # Only language and underscore (e.g., "en_") - treat as language only
            return Locale(locale_str[0:2], "", "")
        # Check for double underscore pattern: language__variant
        if locale_str[3] == '_':
            # country is empty, variant is everything after the double underscore
            variant = locale_str[4:] if length > 4 else ""
            return Locale(locale_str[0:2], "", variant)
        # Otherwise we have a country code (two uppercase letters)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5]
        if length == 5:
            return Locale(locale_str[0:2], country, "")
        # Check for variant after another underscore
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:] if length > 6 else ""
        return Locale(locale_str[0:2], country, variant)