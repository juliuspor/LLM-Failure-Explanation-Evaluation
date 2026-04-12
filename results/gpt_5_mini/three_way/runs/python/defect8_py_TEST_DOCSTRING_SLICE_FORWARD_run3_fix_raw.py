@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        # Split into at most 3 parts: language, country, variant
        parts = locale_str.split('_', 2)

        # Language must be present and 2-3 lowercase letters (accepting ISO codes)
        language = parts[0]
        if len(language) < 2 or len(language) > 3 or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")

        # No more parts -> language only
        if len(parts) == 1:
            if len(language) != 2 and len(language) != 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "")

        # Handle country (may be empty for forms like 'fr__POSIX')
        country = parts[1]
        variant = ""
        if len(parts) == 3:
            variant = parts[2]

        # Validate country if present
        if country:
            if len(country) not in (2, 3) or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")

        # If variant exists, it may be any value; ensure separator rules were followed
        # Construct Locale: language, country (may be empty), variant (may be empty)
        return Locale(language, country, variant)