    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        locale_str = locale_str.strip()
        if not locale_str:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        parts = locale_str.split('_')
        if len(parts) == 1:
            language = parts[0]
            if len(language) == 2 or len(language) == 3:
                if language.isalpha() and language.islower():
                    return Locale(language, "")
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if len(parts) == 2:
            language, country = parts
            if (len(language) == 2 or len(language) == 3) and len(country) == 2:
                if language.isalpha() and language.islower() and country.isalpha() and country.isupper():
                    return Locale(language, country)
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if len(parts) == 3:
            language, country, variant = parts
            if (len(language) == 2 or len(language) == 3) and len(country) == 2:
                if language.isalpha() and language.islower() and country.isalpha() and country.isupper():
                    return Locale(language, country, variant)
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        raise ValueError(f"Invalid locale format: {locale_str}")