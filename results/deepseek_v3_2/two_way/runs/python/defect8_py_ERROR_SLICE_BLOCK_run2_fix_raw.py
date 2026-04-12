    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_', 2)  # Split into max 3 parts
        if not parts or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            country_part = parts[1]
            if country_part:
                if len(country_part) != 2 or not country_part.isalpha() or not country_part.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = country_part
            # If country_part is empty (like "fr__POSIX"), we leave country as "" and proceed to variant
        
        if len(parts) == 3:
            variant = parts[2]
            # Variant can be any string, no validation needed
        
        return Locale(language, country, variant)