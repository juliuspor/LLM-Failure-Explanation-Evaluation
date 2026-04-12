@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        parts = locale_str.split('_', 2)  # at most 3 parts: language, country, variant
        # Validate language
        if len(parts[0]) != 2 or not parts[0].islower() or not parts[0].isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")

        language = parts[0]
        country = ''
        variant = ''

        if len(parts) == 1:
            return Locale(language, country, variant)

        # parts has at least 2 elements (there was an underscore)
        country_part = parts[1]
        # If there is a third part, that's the variant (may be empty if string had double underscore)
        if len(parts) == 3:
            variant = parts[2]

        # country_part may be empty (e.g., "fr__POSIX") or should be 2 uppercase letters
        if country_part == '':
            country = ''
        else:
            if len(country_part) != 2 or not country_part.isupper() or not country_part.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = country_part

        return Locale(language, country, variant)