    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not (1 <= len(parts) <= 3):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid language code: {language}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            country = parts[1]
            if country:
                # Country can be uppercase letters (ISO 3166) or digits (UN M.49)
                if not (country.isalpha() and country.isupper()) and not country.isdigit():
                    raise ValueError(f"Invalid country code: {country}")
        
        if len(parts) == 3:
            variant = parts[2]
            # Variant can be any string, no validation needed
        
        return Locale(language, country, variant)