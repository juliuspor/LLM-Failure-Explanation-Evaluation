@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        # Basic length checks: language must be at least 2 chars
        if len(locale_str) < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Split into at most 3 parts: language, country, variant (variant may contain underscores)
        parts = locale_str.split('_', 2)

        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Only language
        if len(parts) == 1:
            return Locale(language, "")

        # Language + country (country may be empty when input like 'fr__POSIX')
        country = parts[1]
        # If only two parts provided, treat second as country (must be 2 uppercase letters if non-empty)
        if len(parts) == 2:
            if country == "":
                # Empty country is invalid for a two-part form
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country)

        # Three parts: language, country (may be empty), variant (may be empty)
        variant = parts[2]
        if country != "":
            # Validate country when present
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            # Empty country, so variant is specified directly after second underscore
            if variant == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "", variant)