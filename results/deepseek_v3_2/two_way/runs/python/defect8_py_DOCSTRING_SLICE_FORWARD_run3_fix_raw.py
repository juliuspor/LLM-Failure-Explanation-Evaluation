    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0].lower()
        if len(language) < 2 or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) > 1:
            country_part = parts[1]
            if len(country_part) == 2 and country_part.isalpha():
                country = country_part.upper()
            else:
                # If not a 2-letter country code, treat as variant
                variant = '_'.join(parts[1:])
                country = ""
            
            if len(parts) > 2 and country:
                variant = '_'.join(parts[2:])
        
        return Locale(language, country, variant)