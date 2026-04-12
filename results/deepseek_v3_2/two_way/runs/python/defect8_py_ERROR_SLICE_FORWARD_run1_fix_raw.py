    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) > 1:
            country_part = parts[1]
            if country_part:
                if len(country_part) != 2 or not country_part.isalpha() or not country_part.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = country_part
            
            if len(parts) > 2:
                variant = '_'.join(parts[2:])
        
        return Locale(language, country, variant)