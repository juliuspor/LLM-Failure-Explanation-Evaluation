    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Convert to string in case it's not
        str_val = str(locale_str)
        length = len(str_val)
        if length == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Handle language only (2 or 3 characters)
        if '_' not in str_val:
            # Language code must be all letters, at least 2 chars
            if not str_val.isalpha() or len(str_val) < 2:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(str_val.lower(), "")
        
        # Split by underscore
        parts = str_val.split('_')
        if len(parts) > 3 or len(parts) < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if not language.isalpha() or len(language) < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = parts[1] if len(parts) > 1 else ""
        variant = parts[2] if len(parts) > 2 else ""
        
        # Validate country code (2 letters or 3 digits)
        if country:
            if not (len(country) == 2 and country.isalpha()) and not (len(country) == 3 and country.isdigit()):
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Convert to proper case: language lower, country upper
        language = language.lower()
        country = country.upper()
        
        return Locale(language, country, variant)