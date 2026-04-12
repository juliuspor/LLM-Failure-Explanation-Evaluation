@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        parts = locale_str.split('_')
        # language only
        if len(parts) == 1:
            lang = parts[0]
            if len(lang) != 2 or not lang.islower() or not lang.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, "")

        # language_country
        if len(parts) == 2:
            lang, country = parts
            if len(lang) != 2 or not lang.islower() or not lang.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isupper() or not country.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country)

        # language_country_variant (variant may contain underscores, so join remaining)
        if len(parts) >= 3:
            lang = parts[0]
            country = parts[1]
            variant = '_'.join(parts[2:])
            if len(lang) != 2 or not lang.islower() or not lang.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isupper() or not country.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country, variant)

        # Fallback
        raise ValueError(f"Invalid locale format: {locale_str}")