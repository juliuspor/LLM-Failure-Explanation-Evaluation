    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 0 or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid language code: {language}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            country_part = parts[1]
            if len(country_part) == 2 and country_part.isalpha() and country_part.isupper():
                country = country_part
            elif len(country_part) == 3 and country_part.isdigit():
                country = country_part
            else:
                # If the second part is not a valid country code, treat it as variant
                variant = country_part
                if len(parts) == 3:
                    variant += "_" + parts[2]
            
            if len(parts) == 3 and country:
                variant = parts[2]
        
        return Locale(language, country, variant)