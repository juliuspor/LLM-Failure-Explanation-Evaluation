    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts or len(parts[0]) != 2 or not parts[0].isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0].lower()
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            # Second part could be country or variant if empty country
            if len(parts[1]) == 2 and parts[1].isalpha():
                country = parts[1].upper()
                if len(parts) >= 3:
                    variant = '_'.join(parts[2:])
            else:
                # No country, second part is variant
                variant = '_'.join(parts[1:])
        
        return Locale(language, country, variant)