@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        parts = locale_str.split('_', 2)
        # Validate language
        language = parts[0]
        if len(language) != 2 or not (language.islower() and language.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")

        country = ""
        variant = ""

        if len(parts) >= 2:
            country_part = parts[1]
            if country_part:
                if len(country_part) != 2 or not (country_part.isupper() and country_part.isalpha()):
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = country_part
            else:
                # empty country (e.g., 'fr__POSIX') -> country remains ''
                country = ""

        if len(parts) == 3:
            variant = parts[2]
            if variant == "":
                # variant must not be empty when explicitly present
                raise ValueError(f"Invalid locale format: {locale_str}")

        return Locale(language, country, variant)