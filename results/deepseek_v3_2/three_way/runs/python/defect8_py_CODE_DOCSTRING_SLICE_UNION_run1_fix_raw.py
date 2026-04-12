    @classmethod
    def to_locale(cls, locale_str: str) -> Locale:
        """
        Converts a string to a Locale.

        This method expects the string to be in the format:
          language[_country[_variant]]
        where language is 2-3 lowercase letters and country is 2 uppercase letters.
        If the string is empty or None, returns None.
        """
        if locale_str is None:
            return None
        if not locale_str:
            return Locale("", "", "")
        parts = locale_str.split('_')
        language = parts[0].lower() if parts[0] else ""
        country = ""
        variant = ""
        if len(parts) >= 2:
            country = parts[1].upper() if parts[1] else ""
        if len(parts) >= 3:
            variant = '_'.join(parts[2:])  # keep underscores in variant
        return Locale(language, country, variant)