@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        if len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        lang = parts[0]
        if not (lang[0] >= 'a' and lang[0] <= 'z' and lang[1] >= 'a' and lang[1] <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 1:
            return Locale(lang, "")
        country = parts[1]
        if country != "":
            if len(country) != 2 or not (country[0] >= 'A' and country[0] <= 'Z' and country[1] >= 'A' and country[1] <= 'Z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 2:
            return Locale(lang, country)
        variant = parts[2]
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)