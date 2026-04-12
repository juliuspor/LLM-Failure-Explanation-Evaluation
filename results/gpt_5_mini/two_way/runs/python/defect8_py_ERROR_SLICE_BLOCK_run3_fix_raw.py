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

        # parts has at least 2 elements: country (may be empty) and possible variant
        country = parts[1]
        variant = ""
        if len(parts) == 3:
            variant = parts[2]

        # If country is present (non-empty), it must be two uppercase letters
        if country:
            if len(country) != 2 or not country.isupper() or not country.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            # Empty country, variant may be present
            if variant == "":
                # Form was like 'fr_' which is invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "", variant)