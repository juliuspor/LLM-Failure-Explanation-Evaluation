    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_', 2)  # Split into max 3 parts
        if not parts or not parts[0]:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0].lower()
        if len(language) != 2 and len(language) != 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) > 1:
            country_part = parts[1]
            if country_part:
                if len(country_part) == 2:
                    if not country_part.isalpha() or not country_part.isupper():
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    country = country_part.upper()
                elif len(country_part) == 3 and country_part.isdigit():
                    # UN M.49 numeric-3 area code
                    country = country_part
                else:
                    # If not a valid country code, treat as variant
                    variant = '_'.join(parts[1:])
                    country = ""
                    return Locale(language, country, variant)
            else:
                # Empty country part (double underscore)
                country = ""
                if len(parts) > 2:
                    variant = parts[2]
                else:
                    variant = ""
                return Locale(language, country, variant)
            
            if len(parts) > 2:
                variant = parts[2]
        
        return Locale(language, country, variant)