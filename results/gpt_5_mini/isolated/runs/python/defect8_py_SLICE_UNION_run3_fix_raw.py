@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        # Validate language
        if len(parts[0]) != 2 or not parts[0].islower() or not parts[0].isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if len(parts) == 1:
            return Locale(language, "")
        # parts has at least language and country/variant
        country = parts[1]
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 2:
            return Locale(language, country)
        # parts == 3 -> variant present (can be empty? Java allows non-empty)
        variant = parts[2]
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)