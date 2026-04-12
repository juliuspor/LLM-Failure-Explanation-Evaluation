    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 1:
            # Only language
            lang = parts[0]
            if len(lang) != 2 or not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, "")
        elif len(parts) == 2:
            # language and country, or language and variant (if country empty)
            lang = parts[0]
            second = parts[1]
            if len(lang) != 2 or not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(second) == 2 and second.isalpha() and second.isupper():
                # language_country
                return Locale(lang, second)
            else:
                # language__variant (two underscores) -> country is empty
                return Locale(lang, "", second)
        elif len(parts) == 3:
            # language_country_variant
            lang, country, variant = parts
            if len(lang) != 2 or not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country, variant)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")