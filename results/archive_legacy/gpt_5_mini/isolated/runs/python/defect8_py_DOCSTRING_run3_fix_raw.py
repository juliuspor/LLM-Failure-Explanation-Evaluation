@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        s = locale_str.replace('-', '_')
        if len(s) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        parts = s.split('_')
        if len(parts[0]) < 1:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0].lower()
        if not language.isalpha() or not (1 <= len(language) <= 3):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = ''
        variant = ''
        if len(parts) >= 2 and parts[1] != '':
            country = parts[1].upper()
            if not country.isalpha() or len(country) not in (2, 3):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) >= 3:
            variant = '_'.join(parts[2:])
        return Locale(language, country, variant)