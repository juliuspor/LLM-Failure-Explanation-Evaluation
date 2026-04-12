@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        if len(parts[0]) != 2 or not parts[0].isalpha() or parts[0].lower() != parts[0]:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if len(parts) == 1:
            return Locale(language, "")
        if len(parts) == 2:
            country_or_variant = parts[1]
            if country_or_variant == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country_or_variant) == 2 and country_or_variant.isalpha() and country_or_variant.upper() == country_or_variant:
                return Locale(language, country_or_variant)
            return Locale(language, "", country_or_variant)
        country = parts[1]
        variant = parts[2]
        if country == "":
            if variant == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "", variant)
        if len(country) != 2 or not country.isalpha() or country.upper() != country:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)