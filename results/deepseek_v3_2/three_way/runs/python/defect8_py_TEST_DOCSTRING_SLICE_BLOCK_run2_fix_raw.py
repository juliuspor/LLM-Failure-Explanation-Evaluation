    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_', 2)  # Split into max 3 parts
        language = parts[0]
        country = ''
        variant = ''
        
        if len(parts) >= 2:
            # Second part could be country or variant if country is empty
            if len(parts[1]) == 2 and parts[1].isalpha() and parts[1].isupper():
                country = parts[1]
                if len(parts) == 3:
                    variant = parts[2]
            else:
                # No country, second part is variant
                variant = parts[1]
                if len(parts) == 3:
                    variant = parts[1] + '_' + parts[2]  # variant may contain underscores
        
        # Validate language
        if len(language) == 0 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate country if present
        if country:
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Variant can be any string, no validation needed
        
        return Locale(language, country, variant)