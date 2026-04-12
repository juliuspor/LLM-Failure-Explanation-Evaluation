@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        ls = locale_str.strip()
        if len(ls) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Normalize separator to underscore
        ls = ls.replace('-', '_')

        # Split into at most 3 parts: language, country, variant
        parts = ls.split('_', 2)

        # Validate language
        language = parts[0]
        if len(language) != 2 or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = language.lower()

        country = ""
        variant = ""

        if len(parts) >= 2:
            country = parts[1]
            # country may be empty (e.g., 'fr__POSIX')
            if country != "":
                if len(country) != 2 or not country.isalpha():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = country.upper()

        if len(parts) == 3:
            variant = parts[2]
            if variant == "":
                raise ValueError(f"Invalid locale format: {locale_str}")

        return Locale(language, country, variant)