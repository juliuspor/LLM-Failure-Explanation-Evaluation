@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        # Split on underscore to handle language, country, variant (variant may contain underscores)
        parts = locale_str.split('_')
        # Validate language
        if len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not (parts[0][0].islower() and parts[0][1].islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")

        language = parts[0]

        # Only language
        if len(parts) == 1:
            return Locale(language, "")

        # Language + country (country may be empty when pattern like 'fr__POSIX')
        country = parts[1]
        if country:
            if len(country) != 2 or not (country[0].isupper() and country[1].isupper()):
                raise ValueError(f"Invalid locale format: {locale_str}")

        # Variant may include underscores, so join remaining parts
        if len(parts) >= 3:
            variant = '_'.join(parts[2:])
            return Locale(language, country, variant)
        else:
            return Locale(language, country)