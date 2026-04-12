@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        language = parts[0]
        if len(language) != 2 or not (language[0].islower() and language[1].islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = ''
        variant = ''
        if len(parts) >= 2:
            country = parts[1]
            if len(country) not in (0, 2) or (len(country) == 2 and not (country[0].isupper() and country[1].isupper())):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 3:
            variant = parts[2]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)