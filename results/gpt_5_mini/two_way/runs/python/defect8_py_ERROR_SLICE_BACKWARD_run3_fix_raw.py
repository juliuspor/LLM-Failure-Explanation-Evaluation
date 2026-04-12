@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        parts = locale_str.split('_')
        # parts length must be between 1 and 3 (extra underscores invalid)
        if len(parts) == 0 or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")

        language = parts[0]
        if not (1 < len(language) <= 3 and language.isalpha() and language.islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")

        # default values
        country = ""
        variant = ""

        if len(parts) == 1:
            return Locale(language, country, variant)

        if len(parts) == 2:
            # Could be language_country or language__variant (empty country)
            # If original had two segments, treat second as country if length 2 and alpha uppercase/lower
            second = parts[1]
            if second == "":
                # empty country with no variant (e.g., "fr_") - invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(second) == 2 and second.isalpha():
                country = second.upper()
                return Locale(language, country, variant)
            else:
                # treat as variant with empty country
                variant = second
                return Locale(language, country, variant)

        # len(parts) == 3
        # parts[1] is country (may be empty), parts[2] is variant (may be empty invalid)
        country_part = parts[1]
        variant_part = parts[2]

        if country_part != "":
            if not (len(country_part) == 2 and country_part.isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = country_part.upper()
        else:
            country = ""

        if variant_part == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = variant_part

        return Locale(language, country, variant)