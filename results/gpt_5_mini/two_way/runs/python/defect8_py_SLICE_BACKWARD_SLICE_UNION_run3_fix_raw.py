@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_')
        # Validate language
        if len(parts) == 0 or len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        lang = parts[0]
        if not (lang[0].islower() and lang[1].islower() and lang.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        # language only
        if len(parts) == 1:
            return Locale(lang, "")
        # language + country
        country = parts[1]
        if len(country) != 2 or not (country[0].isupper() and country[1].isupper() and country.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 2:
            return Locale(lang, country)
        # language + country + variant (variant may contain further underscores)
        variant = "_".join(parts[2:])
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)