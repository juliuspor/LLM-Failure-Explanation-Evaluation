@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        language = parts[0] if len(parts) > 0 else ''
        country = ''
        variant = ''
        if len(parts) > 1:
            country = parts[1]
        if len(parts) > 2:
            variant = parts[2]
        if len(language) != 2 or not (language[0] >= 'a' and language[0] <= 'z') or not (language[1] >= 'a' and language[1] <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if country:
            if len(country) != 2 or not (country[0] >= 'A' and country[0] <= 'Z') or not (country[1] >= 'A' and country[1] <= 'Z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if variant and locale_str.find('_') == -1:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if country and variant:
            return Locale(language, country, variant)
        if country:
            return Locale(language, country)
        if variant:
            return Locale(language, '', variant)
        return Locale(language, '')