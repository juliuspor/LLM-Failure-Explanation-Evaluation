@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        # Split into at most 3 parts: language, country, variant
        parts = locale_str.split('_', 2)
        if len(parts) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")

        language = parts[0]
        country = ''
        variant = ''

        if len(language) != 2 or not language.islower() or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")

        if len(parts) > 1:
            country = parts[1]
        if len(parts) > 2:
            variant = parts[2]

        # Validate country if present (must be exactly 2 uppercase letters)
        if country:
            if len(country) != 2 or not country.isupper() or not country.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")

        # Variant may be empty or any value; when present ensure it does not contain separators violations
        # (no further validation required beyond presence)

        return Locale(language, country, variant)