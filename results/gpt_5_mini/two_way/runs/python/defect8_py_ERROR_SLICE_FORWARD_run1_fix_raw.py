@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        # Split into parts by underscore
        parts = locale_str.split('_')

        # Validate language
        if len(parts) == 0 or len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if not (language[0].islower() and language[1].islower() and language.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Handle cases based on number of parts
        if len(parts) == 1:
            return Locale(language, "")
        elif len(parts) == 2:
            country = parts[1]
            if len(country) == 0:
                # empty country -> treat as language only
                return Locale(language, "")
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country)
        else:
            # 3 or more parts: language, country (may be empty), variant (rest joined with '_')
            country = parts[1]
            variant = '_'.join(parts[2:])
            if len(country) != 0 and (len(country) != 2 or not country.isalpha() or not country.isupper()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)