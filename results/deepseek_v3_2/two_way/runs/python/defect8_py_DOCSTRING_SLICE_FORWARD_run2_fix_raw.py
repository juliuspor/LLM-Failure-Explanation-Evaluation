    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Split by underscore
        parts = locale_str.split('_')
        if not parts or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if len(language) < 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            country = parts[1]
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        if len(parts) == 3:
            variant = parts[2]
            # variant can be any string, no validation
        
        return Locale(language, country, variant)